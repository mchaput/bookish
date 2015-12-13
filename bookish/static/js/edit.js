$(document).ready(function() {
    var autosave = true;
    var textarea = document.getElementById("source");

    var getPath = function() {
        return $("#editpath").val()
    };

    var smartBs = function(cm) {
        var tab = cm.getOption("indentUnit");
        var start = cm.getCursor("start");
        var end = cm.getCursor("end");
        if (start.line == end.line && start.ch == end.ch && start.ch > 0) {
            var point = start.ch - 1;
            var line = cm.getLine(start.line);
            var count = 0;
            while (count < tab && point >= 0 && line.charAt(point) === " ") {
                cm.execCommand("delCharBefore");
                count += 1;
                point -= 1;
            }
            if (count == 0) {
                cm.execCommand("delCharBefore");
            }
        } else {
            cm.execCommand("delCharBefore");
        }
    };

    window.previewing = false;
    window.needsPreview = false;

    window.preview = function() {
        if (window.previewing) {
            window.needsPreview = true;
            return;
        } else {
            window.previewing = true;
            window.needsPreview = false;
        }

        $.ajax("/_preview/", {
            type: "POST",
            data: {
                path: getPath(),
                source: editor.getValue(),
                scrollTop: $("#preview").contents().scrollTop(),
                autosave: autosave
            },
            success: function(data, status) {
                var frame = window.frames[0];
                var doc = frame.document;

                doc.open();
                doc.write(data.html);
                doc.close();
                $(frame).scrollTop(data.scrollTop);

                window.previewing = false;
                if (window.needsPreview) {
                    window.needsPreview = false;
                    window.preview();
                }
            },
            complete: function(data, status) {
                window.previewing = false;
            }
        })
    };

    window.saveEdits = function(instance)  {
        $("#preview").addClass("saving");
        $.ajax("/_save/", {
            type: "POST",
            data: {
                path: getPath(),
                source: editor.getValue()
            },
            success: function(data, status) {
                //alert("Saved!");
            },
            error: function(data, status) {
                alert("Saving failed!");
            },
            complete: function(data, status) {
                $("#preview").removeClass("saving");
            }
        });
    };
    CodeMirror.commands.save = window.saveEdits;

    var editor = CodeMirror.fromTextArea(textarea, {
        mode: "bookish",
        lineWrapping: true,
        theme: "monokai",
        tabSize: 4,
        indentUnit: 4,
        undoDepth: 1000,
        lineNumbers: true,
        extraKeys: {
            "Tab": "indentMore",
            "Shift-Tab": "indentLess",
            "Backspace": smartBs
        }
    });

    editor.on("change", function(cm, chobj) {
        if (window.previewTimer) {
            clearTimeout(window.previewTimer);
        }
        window.previewTimer = setTimeout(window.preview, 200)
    });

    function doResize() {
        var winHeight = $(window).height();
        var main = $("#main");
        var mainWidth = main.width();

        // Find the top position of the editor and preview divs
        var top = $("header").height();
        var preview = $("#preview");
        var editPane = $("#editpane");
        var prevPane = $("#previewpane");
        var half;

        main.height(winHeight - top);
        if (mainWidth <= 900) {
            // Single-column "top-bottom" mode
            half = Math.floor((winHeight - top) / 2);
            editPane.css("width", "100%").offset({top: top, left: 0});
            editPane.height(half);
            prevPane.css("width", "100%").offset({top: top + half, left: 0});
            prevPane.height(half);
            editor.setSize(null, half);
            preview.height(half);
        } else {
            // Two-column "side-by-side" mode
            half = Math.floor(mainWidth / 2);
            editPane.width(half).offset({top: top, left: 0});
            editPane.height(winHeight - top);
            prevPane.width(half).offset({top: top, left: half});
            prevPane.height(winHeight - top);
            editor.setSize(null, (winHeight - top));
            preview.css("height", (winHeight - top) + "px");
        }
    }
    $(window).resize(doResize);
    $(window).on("sidebaropen", doResize).on("sidebarclose", doResize);
    doResize();

    var charWidth = editor.defaultCharWidth();
    var basePadding = 4;
    editor.on("renderLine", function(cm, line, elt) {
        var off = CodeMirror.countColumn(line.text, null, cm.getOption("tabSize")) * charWidth;
        elt.style.textIndent = "-" + off + "px";
        elt.style.paddingLeft = (basePadding + off) + "px";
    });
    editor.refresh();
    window.preview();
});
