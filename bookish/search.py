from __future__ import print_function
import logging
import os.path
import re

from whoosh import analysis, columns, fields, index, qparser, query, sorting
from bookish import compat, paths, functions


default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
default_logger.addHandler(sh)


text_ana = (
    analysis.RegexTokenizer(expression=r"\w+")
    | analysis.IntraWordFilter(mergewords=True, mergenums=True)
    | analysis.LowercaseFilter()
    | analysis.StemFilter(lang="en")
)


default_fields = {
    "path": fields.ID(stored=True, unique=True),
    "parent": fields.KEYWORD,
    "content": fields.TEXT(analyzer=text_ana),
    "title": fields.TEXT(analyzer=text_ana, stored=True, sortable=True),
    "category": fields.ID(sortable=columns.RefBytesColumn()),
    "subject": fields.STORED,
    "icon": fields.STORED,
    "sortkey": fields.ID(sortable=True),
    "grams": fields.NGRAMWORDS,
    "type": fields.KEYWORD(stored=True),
    "tags": fields.KEYWORD(stored=True),
    "modified": fields.DATETIME(stored=True),
    "links": fields.KEYWORD,
    "container": fields.STORED,
    "bestbet": fields.TEXT(analyzer=text_ana),
}


class LockError(Exception):
    pass


def index_mode(block):
    attrs = block.get("attrs")
    return attrs.get("index") if attrs else None


def combine_readers(readers):
    from whoosh import reading

    rs = []
    for r in readers:
        if r.is_atomic():
            rs.append(r)
        else:
            rs.extend(r.readers)

    if rs:
        if len(rs) == 1:
            return rs[0]
        else:
            return reading.MultiReader(rs)

    raise index.EmptyIndexError


class Searchables(object):
    @staticmethod
    def _get_block_text(body, typename):
        for block in body:
            if block.get("type") == typename:
                return functions.string(block.get("text"))
        return ""

    @staticmethod
    def _get_path_attr(root, path, attrs, name):
        value = attrs.get(name)
        if value:
            return paths.join(path, value)

    def schema(self):
        return fields.Schema(**default_fields)

    def _should_index_document(self, pages, path, root, block):
        mode = index_mode(block)
        if mode != "no":
            return block.get("type") == "root" or mode == "document"

    def _should_index_block(self, block):
        return index_mode(block) != "no"

    def documents(self, pages, path, root, options):
        docs = []
        if self._should_index_document(pages, path, root, root):
            self._block_to_doc(pages, path, root, root, docs)
        return docs

    def _block_to_doc(self, pages, path, root, block, docs, recurse=True):
        if recurse:
            gen = self._flatten_with_docs(pages, path, root, block, docs)
        else:
            gen = self._flatten(block)
        text = " ".join(gen)
        docs.append(self._make_doc(pages, path, root, block, text))

    def _flatten(self, block):
        if not self._should_index_block(block):
            return

        if "text" in block:
            yield functions.string(block["text"])

        if "body" in block:
            for subblock in block["body"]:
                for text in self._flatten(subblock):
                    yield text

    def _flatten_with_docs(self, pages, path, root, block, docs):
        if not self._should_index_block(block):
            return

        if "text" in block:
            yield functions.string(block["text"])

        if "body" in block:
            for subblock in block["body"]:
                if self._should_index_document(pages, path, root, subblock):
                    self._block_to_doc(pages, path, root, subblock, docs,
                                       recurse=False)
                else:
                    for text in self._flatten_with_docs(pages, path, root,
                                                        subblock, docs):
                        yield text

    def _get_title(self, block):
        if block.get("type") == "root":
            return functions.string(block.get("title")).strip()
        else:
            return functions.string(block.get("text")).strip()

    def _make_doc(self, pages, path, root, block, text):
        attrs = block.get("attrs", {})
        blocktype = block.get("type")
        body = block.get("body")
        is_root = blocktype == "root"

        # If a title was not passed in: if this is the root, look for a title
        # block, otherwise use the block text
        title = self._get_title(block) or paths.basename(path)

        container = False
        path = paths.basepath(path)
        if is_root:
            # Store a boolean if this page has subtopics
            subtopics = functions.subblock_by_id(block, "subtopics")
            container = subtopics and bool(subtopics.get("body"))
        else:
            blockid = functions.block_id(block)
            path = "%s#%s" % (path, blockid)

        # Look for a summary block
        summary = self._get_block_text(body, "summary")

        # Look for tags in the page attributes
        tags = attrs.get("tags", "").strip().replace(",", "")

        # Find outgoing links
        outgoing = []
        for link in functions.find_links(block):
            val = link.get("value")
            if val:
                outgoing.append(pages.full_path(path, val))
        outgoing = " ".join(outgoing)

        doctype = attrs.get("type")

        d = {
            "path": path,
            "status": attrs.get("status"),
            "category": "_",
            "content": functions.string(text),
            "title": title,
            "sortkey": attrs.get("sortkey") or title.lower(),
            "summary": summary,
            "grams": title,
            "type": doctype,
            "tags": tags,
            "icon": attrs.get("icon"),
            "links": outgoing,
            "container": container,
            "parent": self._get_path_attr(block, path, attrs, "parent"),
            "bestbet": attrs.get("bestbet"),
        }
        return d


class Indexer(object):
    def __init__(self):
        self.options = {}

    @staticmethod
    def _sanitize_doc(doc):
        for key, value in doc.items():
            if isinstance(value, compat.bytes_type):
                doc[key] = value.decode("ascii")

    def set_option(self, name, value):
        self.options[name] = value

    def searcher(self):
        raise NotImplementedError

    def query(self):
        raise NotImplementedError

    def documents(self, pages, path):
        raise NotImplementedError

    def update(self, pages, prefix="", clean=False):
        raise NotImplementedError

    def close(self):
        pass


class WhooshIndexer(Indexer):
    def __init__(self, indexdir, searchables, options=None, create=True,
                 indexname=None, logger=None, staticdir=None):
        self.indexdir = indexdir
        self.staticdir = staticdir
        self.searchables = searchables
        self.options = options or {}
        self.logger = logger or default_logger

        schema = self.searchables.schema()
        if not index.exists_in(indexdir, indexname=indexname) and create:
            if not os.path.exists(indexdir):
                os.makedirs(indexdir)
            self.index = index.create_in(indexdir, schema=schema,
                                         indexname=indexname)
        else:
            self.index = index.open_dir(indexdir, schema=schema,
                                        indexname=indexname)

    def searcher(self):
        if self.staticdir:
            from whoosh import searching

            six = index.open_dir(self.staticdir)
            r1 = six.reader()
            r2 = self.index.reader()
            r = combine_readers([r1, r2])
            s = searching.Searcher(r, fromindex=self.index)
        else:
            s = self.index.searcher()

        return WhooshSearcher(s)

    def query(self):
        return self.searcher().query()

    def _find_files(self, pages, prefix, reader, clean):
        store = pages.store
        existing = set(paths.basepath(p) for p in store.list_all()
                       if pages.is_wiki(p))

#        if prefix:
#            print("prefix=", prefix)
#            raise Exception
#            changed = set()
#            new = set()
#            for p in existing:
#                if not p.startswith(prefix):
#                    continue
#                if ("path", p.encode("utf8")) in reader:
#                    print("!!!!!!!!!!!!")
#                    changed.add(p)
#                else:
#                    new.add(p)
#            return new, changed, ()

        if clean:
            new = existing
            changed = set()
            deleted = set()
        else:
            # Read all the stored field dicts from the index and build a
            # dictionary mapping paths to their last indexed mod time
            modtimes = {}
            for fs in reader.all_stored_fields():
                p = fs["path"]
                if "#" in p:
                    continue

                modtime = fs["modified"]
                modtimes[p] = modtime

            indexedpaths = set(modtimes)

            new = existing - indexedpaths
            deleted = indexedpaths - existing
            both = existing - new - deleted

            changed = set()
            for path in both:
                ix_mod = modtimes[path]
                store_mod = store.last_modified(pages.source_path(path))
                if store_mod > ix_mod:
                    self.logger.debug("%s changed: %s > %s", path, store_mod,
                                      ix_mod)
                    changed.add(path)

        return new, changed, deleted

    def dump(self, pages):
        idx = self.index

        def print_set(s):
            for path in sorted(s):
                print("    ", path)

        with idx.reader() as r:
            new, changed, deleted = self._find_files(pages, "", r, False)
            print("NEW", len(new))
            print_set(new)
            print("CHANGED", len(changed))
            print_set(changed)
            print("DELETED", len(deleted))
            print_set(deleted)

    def documents(self, pages, path):
        if not pages.exists(path):
            return

        modtime = pages.last_modified(path)
        try:
            jsondata = pages.json(path, postprocess=False)
        except:
            self.logger.error("Error parsing %r", path)
            raise

        attrs = jsondata.get("attrs")
        if attrs:
            if "type" in attrs:
                if attrs["type"].strip() == "include":
                    return
            if "index" in attrs:
                if attrs["index"].lower().strip() == "no":
                    return

        docs = self.searchables.documents(pages, path, jsondata, self.options)
        for doc in docs:
            if doc.get("path") == path:
                doc["modified"] = modtime
            yield doc

    def create(self):
        if not os.path.exists(self.indexdir):
            os.mkdir(self.indexdir)

    def update(self, pages, prefix="", clean=False):
        if clean:
            schema = self.searchables.schema()
            self.index = index.create_in(self.indexdir, schema=schema)
        idx = self.index

        # self.logger.info("Indexing %s files to %s",
        #                  ("all" if clean else "changed"), self.indexdir)
        doccount = 0
        pagecount = 0

        t = compat.perf_counter()
        try:
            w = idx.writer()
        except index.LockError:
            raise LockError
        new, changed, deleted = self._find_files(pages, prefix, w.reader(),
                                                 clean)
        didsomething = False
        if new or changed or deleted:
            if deleted:
                didsomething = True
                for delpath in sorted(changed | deleted):
                    delpath = paths.basepath(delpath)
                    self.logger.info("Deleting %s from index", delpath)
                    # w.delete_unique("path", delpath)
                    w.delete_by_query(query.Term("path", delpath))
                    w.delete_by_query(query.Prefix("path",
                                                   delpath + "#"))

            for addpath in sorted(new | changed):
                addpath = paths.basepath(addpath)
                added = False

                if addpath in changed:
                    self.logger.info("Removing %s from index", addpath)
                    w.delete_by_query(query.Term("path", addpath))
                    w.delete_by_query(query.Prefix("path", addpath + "#"))
                    didsomething = True

                for doc in self.documents(pages, addpath):
                    self._sanitize_doc(doc)

                    self.logger.debug("Indexing %s", doc["path"])
                    try:
                        if clean or "#" in doc["path"]:
                            w.add_document(**doc)
                        else:
                            w.update_document(**doc)
                    except ValueError:
                        self.logger.error("Error indexing %r", doc)
                        raise

                    added = True
                    doccount += 1

                if added:
                    pagecount += 1
                    didsomething = True

        if didsomething:
            self.logger.info("Committing index changes")
            w.commit()
            self.logger.info("Indexed %d docs from %d pages in %.06f seconds",
                             doccount, pagecount, compat.perf_counter() - t)
        else:
            # self.logger.info("No changes to commit")
            w.cancel()

        return didsomething

    def close(self):
        self.index.close()


class WhooshSearcher(object):
    def __init__(self, searcher):
        self.searcher = searcher
        self.limit = None
        self.sortedby = None
        self._lookup_cache = {}

    @staticmethod
    def _to_key(fields):
        return tuple(sorted(fields.items()))

    def up_to_date(self):
        return self.searcher.up_to_date()

    def has_field(self, fieldname):
        return fieldname in self.searcher.schema

    def lexicon(self, fieldname):
        searcher = self.searcher
        field = searcher.schema[fieldname]
        return (field.from_bytes(btext)
                for btext in searcher.lexicon(fieldname))

    def tag_cloud(self, fieldname="tags", divisions=20, max_df=30):
        searcher = self.searcher
        field = searcher.schema[fieldname]
        reader = searcher.reader()
        for btext, terminfo in reader.iter_field(fieldname):
            df = terminfo.doc_frequency()
            div = (min(df, max_df) / max_df) * divisions
            yield field.from_bytes(btext), div

    def query(self):
        return WhooshQuery(self.searcher)

    def document(self, **fields):
        key = self._to_key(fields)
        try:
            return self._lookup_cache[key]
        except KeyError:
            doc = self.searcher.document(**fields)
            self._lookup_cache[key] = doc
            return doc

    def documents(self, **fields):
        return self.searcher.documents(**fields)

    def search(self, *args, **kwargs):
        return self.searcher.search(*args, **kwargs)

    def all_stored_fields(self):
        return self.searcher.all_stored_fields()

    def group_hits(self, docnums):
        s = self.searcher
        return [s.stored_fields(docnum) for docnum in docnums]


class WhooshQuery(object):
    shortcut_exp = re.compile(r"(^|\s)!([A-Za-z0-9]+)($|\s)")

    def __init__(self, searcher):
        self.searcher = searcher
        self.q = None
        self.limit = None
        self.sortedby = None
        self.groupedby = None

    def __repr__(self):
        return "<%s %r>" % (type(self).__name__, self.q)

    def parse(self, qstring, field=None):
        schema = self.searcher.schema
        if field:
            qp = qparser.QueryParser(field, schema)
        else:
            qp = qparser.MultifieldParser(["title", "content"], schema)
        return qp.parse(qstring)

    def _make_kw_query(self, fields):
        terms = []
        for fieldname, value in fields.items():
            terms.append(query.Term(fieldname, value))
        if len(terms) == 1:
            return terms[0]
        else:
            return query.And(terms)

    def make_query(self, qstring=None, field=None, **fields):
        if qstring is not None:
            q = self.parse(qstring, field)
        elif fields:
            q = self._make_kw_query(fields)
        else:
            raise Exception("Must give a query string or use keyword args")
        return q

    def set(self, qstring, field=None, **fields):
        self.q = self.make_query(qstring, **fields)

    def and_(self, qstring=None, field=None, **fields):
        newq = self.make_query(qstring, field, **fields)
        if self.q is None:
            self.q = newq
        else:
            self.q = query.And([self.q, newq])

    def or_(self, qstring=None, field=None, **fields):
        newq = self.make_query(qstring, field, **fields)
        if self.q is None:
            self.q = newq
        else:
            self.q = query.Or([self.q, newq])

    def and_not(self, qstring=None, field=None, **fields):
        self.q = query.AndNot(self.q, self.make_query(qstring, field, **fields))

    def set_limit(self, limit):
        self.limit = limit

    def add_sort_field(self, fieldname, reverse=False):
        if self.sortedby is None:
            self.sortedby = sorting.MultiFacet()
        self.sortedby.add_field(fieldname, reverse)

    def set_group_field(self, fieldname, overlap):
        self.groupedby = sorting.FieldFacet(fieldname, allow_overlap=overlap)

    def search(self):
        q = self.q.normalize()
        hits = self.searcher.search(q, limit=self.limit, sortedby=self.sortedby,
                                    groupedby=self.groupedby)
        return hits

    @staticmethod
    def expand_shortcuts(qstring, shortcuts):
        changed = False
        for shortcut in shortcuts:
            code = "!%s" % shortcut["shortcut"]
            if code in qstring:
                qstring = qstring.replace(code, shortcut["query"])
                changed = True
        return qstring, changed

    def results(self, qstring, cat_order, category=None, shortcuts=None,
                limit=None, cat_limit=5):
        from whoosh.util import now

        t = now()
        s = self.searcher
        limit = limit or self.limit
        showall = False

        if shortcuts:
            qstring, showall = self.expand_shortcuts(qstring, shortcuts)

        if category:
            filter = query.Term("category", category)
        else:
            filter = None

        all_q = self.make_query(qstring, "content")

        show_best = (not category and
                     all(isinstance(lq, query.Term) and lq.field() == "content"
                         for lq in all_q.leaves()))
        if show_best:
            best_q = self.make_query(qstring, "bestbet")
            best_r = s.search(best_q, limit=10)
        else:
            best_r = None

        grams_groups = None
        grams_q = self.make_query(qstring, "grams")
        if any(fn == "grams" for fn, _ in grams_q.iter_all_terms()):
            try:
                grams_r = s.search(grams_q, limit=limit, groupedby="category",
                                   filter=filter)
            except query.QueryError:
                pass
            else:
                grams_groups = grams_r.groups()

        all_r = s.search(all_q, limit=limit, groupedby="category",
                         filter=filter)
        all_groups = all_r.groups()

        # OK, this is complicated... we want to present the categories in the
        # order defined in cat_order, BUT we want categories that have grams
        # matches to come before categories that only have content matches
        final_order = []
        if grams_groups:
            # Add categories in grams_groups in the order defined by cat_order
            for cat in cat_order:
                if cat in grams_groups:
                    final_order.append(cat)
            # Add any categories in grams_groups that aren't in cat_order
            final_order.extend(cat for cat in sorted(grams_groups)
                               if cat not in cat_order)

        seen = set(final_order)
        # Add categories in all_groups in the order defined by cat_order, IF
        # they weren't already added in the previous step
        for cat in cat_order:
            if cat in all_groups and cat not in seen:
                final_order.append(cat)
        # Add any categories in all_groups that weren't added in the previous
        # steps
        final_order.extend(cat for cat in sorted(all_groups)
                           if cat not in cat_order and cat not in seen)

        # If there's only one category, there's no point in cutting it off,
        # just show all hits
        showall = showall or len(final_order) == 1

        # For each category, pull out the docnums and get their stored fields
        length = 0
        categories = []
        for cat in final_order:
            # Combine the docnums for this category from grams and all
            docnums = []
            seen = set()
            if grams_groups:
                for docnum in grams_groups.get(cat, ()):
                    docnums.append(docnum)
                    seen.add(docnum)

            for docnum in all_groups.get(cat, ()):
                if docnum not in seen:
                    docnums.append(docnum)
                    seen.add(docnum)

            # If the number of hits is exactly the limit + 1, then there's no
            # point showing a "show more" line instead of that one extra hit,
            # so just increase the limit in that case
            if len(docnums) == cat_limit + 1:
                cutoff = len(docnums)
            else:
                cutoff = cat_limit

            if not showall and len(docnums) > cutoff:
                docnums = docnums[:cutoff]

            length += len(seen)
            docs = [s.stored_fields(docnum) for docnum in docnums]
            categories.append((cat, docs, len(seen)))

        sent = now()
        runtime_ms = (sent - t) * 1000
        return {
            "qstring": qstring,
            "best": best_r,
            "category": category,
            "categories": categories,
            "length": length,
            "limit": limit,
            "hits": all_r,
            "sent": sent,
            "runtime": runtime_ms,
        }
