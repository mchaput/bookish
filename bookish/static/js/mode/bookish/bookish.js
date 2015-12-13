(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("../../lib/codemirror", require("../xml/xml")));
  else if (typeof define == "function" && define.amd) // AMD
    define(["../../lib/codemirror", "../xml/xml"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
    "use strict";

    CodeMirror.defineMode("bookish", function(cmCfg, modeCfg) {
        if (modeCfg.highlightFormatting == undefined) {
            modeCfg.highlightFormatting = false;
        }

        var aliases = {
            html: "htmlmixed",
            js: "javascript",
            json: "application/json",
            c: "text/x-csrc",
            "c++": "text/x-c++src",
            java: "text/x-java",
            csharp: "text/x-csharp",
            "c#": "text/x-csharp",
            scala: "text/x-scala"
        };

        var getMode = (function () {
            var i, modes = {}, mimes = {}, mime;

            var list = [];
            for (var m in CodeMirror.modes)
                if (CodeMirror.modes.propertyIsEnumerable(m)) list.push(m);
            for (i = 0; i < list.length; i++) {
                modes[list[i]] = list[i];
            }
            var mimesList = [];
            for (var m in CodeMirror.mimeModes) {
                if (CodeMirror.mimeModes.propertyIsEnumerable(m)) {
                    mimesList.push({mime: m, mode: CodeMirror.mimeModes[m]});
                }
            }

            for (i = 0; i < mimesList.length; i++) {
                mime = mimesList[i].mime;
                mimes[mime] = mimesList[i].mime;
            }

            for (var a in aliases) {
                if (aliases[a] in modes || aliases[a] in mimes)
                    modes[a] = aliases[a];
            }

            return function (lang) {
                return modes[lang] ? CodeMirror.getMode(cmCfg, modes[lang]) : null;
            };
        }());

        //var header = "header",
        //    quote = "quote",
        //    keyword = "keyword",
        //    image = "tag",
        //    summary = "number",
        //    link = "link",
        //    strong = "strong",
        //    propValue = "string",
        //    ui = "ui"
        //;

        function start() {
            return {
                f: inText,
                startOfLine: false,
                indented: 0,
                strong: false,
                styles: [],
                ends: [],
                flag: -1,
                localMode: null,
                localState: null
            };
        }

        function blank(state) {
            if (state.f !== inPre) {
                state.f = inText;
                state.styles = [];
                state.ends = [];
                state.endPattern = null;
                state.indented = 0;
                state.wasSpace = true;
                state.flag = -1;
            }
        }

        function addStyle(state, style, end) {
            if (state.styles.length > 0) {
                var last = state.styles[state.styles.length - 1];
                if (last === code && style !== vars) {
                    return null;
                } else if (last === comment) {
                    return null;
                }
            }

            state.f = inStyle;
            state.styles.push(style);
            state.ends.push(end);
            return style;
        }

        function inText(stream, state) {
            var style;

            if (state.startOfLine && stream.match("//")) {
                stream.skipToEnd();
                style = "comment";
            } else if (stream.match(/\|+$/)) {
                // table cell marker at end of line
                style = "marker";
            } else if (state.wasSpace && stream.match(/\*(?=\S)/)) {
                // strong
                style = addStyle(state, "strong", /\*(?=\W)/);
            } else if (state.wasSpace && stream.match(/__(?=\S)/, true)) {
                // ui
                style = addStyle(state, "ui", /__(?=\W)/);
            } else if (state.wasSpace && stream.match(/_((?=\S)|$)/)) {
                // emphasis
                style = addStyle(state, "em", /_(?=\W)/);
            } else if (stream.eat("`")) {
                // code
                style = addStyle(state, "atom", "`");
            } else if (stream.match("<!--")) {
                // HTML-style comment
                style = addStyle(state, "comment", "-->");
            } else if (stream.match('"""')) {
                // summary
                style = addStyle(state, "summary", '"""');
            } else if (stream.match(/<<(.*?)>>/, true)) {
                // var
                style = "variable-2";
            } else if (stream.match(/\[[^\]]*\|/, false)) {
                // start of link with text
                stream.next();
                state.f = inLink;
                state.flag = 0;
                style = "bracket";
            } else if (stream.eat("[")) {
                // start of link without text
                state.f = inLink;
                state.flag = 1;
                style = "bracket";
            } else if (state.startOfLine && stream.match(/#[A-Za-z0-9_]+:/, false)) {
                // property
                stream.next();
                state.f = inProp;
                state.flag = 0;
                style = "tag";
            } else if (state.startOfLine && stream.match(/\s*(={1,5})\s+/)) {
                // heading
                stream.skipToEnd();
                state.styles = [];
                style = "header header-" + RegExp.$1.length;
            } else if (state.startOfLine && stream.eat("@")) {
                // section
                stream.skipToEnd();
                style = "header header-2 section";
                state.styles = [];
            } else if (stream.eatSpace()) {
                state.wasSpace = true;
            } else {
                stream.next();
                state.wasSpace = false;
                style = null;
            }
            return style;
        }

        function inStyle(stream, state) {
            var end = state.ends.length > 0 ? state.ends[state.ends.length - 1] : null;
            var style = state.styles.join(" ");

            if (end !== null && stream.match(end, true)) {
                state.ends.pop();
                state.styles.pop();
                if (state.styles.length == 0) {
                    state.f = inText;
                }
            } else {
                stream.next();
            }
            return style;
        }

        function inProp(stream, state) {
            var style;
            if (stream.eol()) {
                state.f = inText;
                state.flag = -1;
            } else if (state.flag == 0 && stream.eat(":")) {
                style = "bracket";
                state.flag = 1;
            } else if (state.flag == 1) {
                stream.skipToEnd();
                style = "value";
                state.f = inText;
            } else {
                stream.next();
                style = "tag";
            }
            return style
        }

        function inPre(stream, state) {
            var style = "atom";

            if (stream.match("}}}")) {
                state.f = inText;
                state.styles = [];
                style = "atom";
            } else if (state.flag == 0 && state.startOfLine && stream.match(/#!(.*?)$/)) {
                var modeName = RegExp.$1;
                style = "comment";
                state.flag = 1;
                state.localMode = getMode(modeName);
                if (state.localMode) {
                    state.localState = state.localMode.startState();
                }
            } else if (state.localMode) {
                style = state.localMode.token(stream, state.localState);
            } else {
                stream.skipToEnd();
                state.flag = 1;
            }
            return style;
        }

        function inLink(stream, state) {
            var style;
            if (stream.eat("]")) {
                state.f = inText;
                state.flag = -1;
                style = "bracket";
            } else if (stream.eat("|")) {
                state.flag = 1;
                style = "bracket";
            } else if (state.flag == 1 && stream.match(/[A-Z][A-Za-z0-9_]*:[^\]]*\]/, false)) {
                stream.match(/[A-Z][A-Za-z0-9_]*:/);
                style = "tag";
            } else {
                stream.next();
                style = state.flag == 1 ? "link" : "special";
            }
            return style;
        }

        function inPxml(stream, state) {
            var style;
            if (stream.match(">>")) {
                state.f = inText;
                state.flag = -1;
                style = "bracket";
            } else if (state.flag == 0) {
                if (stream.eatSpace()) {
                    state.flag = 1;
                } else {
                    stream.next();
                    style = "tag";
                }
            } else if (state.flag == 1) {
                style = "attribute";
                if (stream.eat("=")) {
                    state.flag = 2;
                } else {
                    stream.next()
                }
            } else if (state.flag == 2) {
                if (stream.eatSpace()) {
                    state.flag = 1;
                } else {
                    stream.next();
                    style = "string";
                }
            } else {
                stream.next();
            }
            return style;
        }

        function tokenizer(stream, state) {
            if (stream.sol()) {
                var lastIndent = state.indented;
                state.startOfLine = true;
                state.wasSpace = true;
                state.indented = stream.indentation();
                if (state.indent > lastIndent + 4 || state.indent < lastIndent - 4) {
                    blank(state);
                }
            }
            if (state.startOfLine) {
                stream.eatSpace();
            }
            if (state.startOfLine && stream.eol()) {
                blank(state);
                return null;
            }

            var style = null;
            if (state.startOfLine && stream.match(/[-*#]+(?=\s)/)) {
                blank(state);
                style = "marker";
            } else if (state.startOfLine && stream.match(/~~+/)) {
                stream.skipToEnd();
                style = "hr";
            } else if (state.startOfLine && stream.match(/[-A-Za-z0-9]+(\s+[-A-Za-z0-9]+=['"].*?['"])*\s*>>/, false)) {
                state.f = inPxml;
                state.flag = 0;
                style = state.f(stream, state);
            } else if (state.startOfLine && stream.eat(":") && stream.skipTo(":")) {
                stream.eat(":");
                style = "marker";
                state.styles = [];
            } else if (state.startOfLine && stream.match("{{{")) {
                state.f = inPre;
                state.flag = 0;
                state.localMode = null;
                state.localState = null;
                style = "atom";
            } else {
                style = state.f(stream, state);
            }
            state.startOfLine = false;
            return style;
        }

        return {
            startState: start,
            token: tokenizer,
            blankLine: blank
        };
    });
    CodeMirror.defineMIME("text/x-bookish", "bookish");
});
