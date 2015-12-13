jQuery.fn.searchbox = function(url, queryopts, delay) {
    return this.each(function() {
        if (queryopts == undefined) {
            queryopts = {};
        }
        if (delay == undefined) {
            delay = 100;
        }

        // Grab a jQuery reference to the textbox
        var textbox = $(this);
        // Create a div for the search results and append it to the body
        var resultsdiv = $('<div>').attr("class", "search-results");

        var catname = null;
        var resultcount = 0;
        var selected = 0;
        var latest = -1;
        var lastqstring = null;
        var timer = null;

        $("body").mouseup(function(e) {
            if (e.target !== textbox[0]
                && $(e.target).closest(resultsdiv).length == 0) {
                hideResults()
            }
        }).append(resultsdiv);

        textbox.focus(function() {
           update();
        }).blur(function() {
            //setTimeout(hideResults, 500);
        }).keydown(function(e) {
            var keycode = e.keyCode || window.event.keyCode;
			var rc = true;

			if (keycode == 13) {
				// Enter
				enterClick();
				return false;
			} else if (keycode == 27) {
				// Escape
				hideResults();
				return false;
			} else if (keycode == 38) {
				// Up key
				if (selected == 0 || selected == -1) {
					selected = resultcount - 1;
				} else {
					selected--;
				}
				updateCss();
				rc = false;
			} else if (keycode == 40) {
				// Down key
				if (selected == resultcount - 1) {
					selected = 0;
				} else {
					selected++;
				}
				updateCss();
				rc = false;
			} else {
				if (timer) {
					clearTimeout(timer);
				}
				selected = 0;
			}

			timer = setTimeout(update, delay);
			return rc;
        });

        function updateCss() {
			resultsdiv.find("li.hit").each(function(i) {
				if (i == selected) {
					$(this).addClass("selected");
				} else {
					$(this).removeClass("selected");
				}
			});
		}

        function enterClick(e) {
            e = $(e || resultsdiv.find("li.selected"));
            if (e.hasClass("more")) {
                catname = e.parent().attr("data-name");
                update(true);
            } else {
                window.location = e.find("a").attr("href");
            }
		}

        function showResults() {
            resultsdiv.fadeIn(200);
        }
        function hideResults() {
            resultsdiv.fadeOut(200);
        }

        function fillResults(html) {
            html = $(html);
            var sent = Number(html.attr("data-sent"));
            if (sent <= latest) return;
            latest = sent;

            resultsdiv.html(html);

            var hits = html.find("li.hit");
            resultcount = hits.size();
            selected = 0;

            hits.mouseover(function(e) {
                var target = $(e.target);
                while (!target.hasClass("hit")) {
                    target = target.parent();
                }
                hits.each(function(i) {
                    if (this === target[0]) {
                        selected = i;
                        $(this).addClass("selected");
                    } else {
                        $(this).removeClass("selected");
                    }
                });
            }).click(function(e) {
                enterClick(e.target);
            });

            updateCss();
        }

        function update(force) {
            var qstring = textbox.val();
            if (qstring === "") {
                catname = null;
            }
            showResults();
            if (force || qstring !== lastqstring) {
                //var startpos = getSelectionStart(box);
                //var endpos = getSelectionEnd(box);

                console.log("Running", qstring, catname);
                $.ajax("/_search", {
                    data: {
                        q: qstring,
                        category: catname,
                        //startpos: startpos,
                        //endpos: endpos,
                        template: "/templates/results.jinja2"
                    },
                    success: function (data) {
                        fillResults(data);
                    },
                    error: function (data) {
                        console.log("Search error");
                    }
                });
                lastqstring = qstring;
            }
        }
    });
};
