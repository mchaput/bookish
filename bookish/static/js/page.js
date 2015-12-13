window.sidebarClosed = true;
window.sidebarWidth = 320;


function getSelectionStart(o) {
	if (o.createTextRange) {
		var r = document.selection.createRange().duplicate();
		r.moveEnd('character', o.value.length);
		if (r.text == '') return o.value.length;
		return o.value.lastIndexOf(r.text);
	} else return o.selectionStart;
}

function getSelectionEnd(o) {
	if (o.createTextRange) {
		var r = document.selection.createRange().duplicate();
		r.moveStart('character', -o.value.length);
		return r.text.length;
	} else return o.selectionEnd;
}

function getVimeoThumbnail(vid, size, callback) {
    var url = "http://vimeo.com/api/v2/video/" + vid + ".json";
    $.getJSON('http://www.vimeo.com/api/v2/video/' + vid + '.json?callback=?',
        {format: "json"},
        function(data) {
            callback(data[0]["thumbnail_" + size]);
        }
    );
}


function setContentSize(el) {
    el = $(el);
    var em = parseFloat($("body").css("font-size"));

    var width = el.width() / em;
    var cls;
    if (width <= 30) {
        cls = "xsmall";
    } else if (width <= 40) {
        cls = "small";
    } else if (width <= 60) {
        cls = "medium";
    } else if (width <= 80) {
        cls = "large";
    } else {
        cls = "xlarge";
    }
    el.removeClass("xsmall small medium large xlarge");
    el.addClass(cls);
}

function setContentSizeClasses(spec) {
    spec = spec || "#main";
    var e = $(spec);
    var subs = e.find("div.sizing,div.column");
    subs.each(function() {
        setContentSize(this);
    });
}

function openSidebar() {
    window.sidebarClosed = false;
    setSidebarWidth(window.sidebarWidth);
    $("#menubtn").removeClass("closed").addClass("open");
    recordSidebarState();
    $(window).trigger("sidebaropen");
    if (window.shouldScroll) {
        window.shouldScroll = false;
        setTimeout(scrollToSidebarHere, 100);
    }
}

function closeSidebar() {
    window.sidebarClosed = true;
    $("#sidebar").attr("class", "closed"); //.width(6);
    $("#menubtn").removeClass("open").addClass("closed");
    $("#main").css("left", 0).css("width", "100%");
    recordSidebarState();
    $(window).trigger("sidebarclose");
    setContentSizeClasses();
}

function toggleSidebar() {
    if (window.sidebarClosed) {
        openSidebar();
    } else {
        closeSidebar();
    }
}

function resetSidebar() {
    var w = window.sidebarWidth;
    var win = $(window);
    var ww = win.width();

    var sidebar = $("#sidebar");
    var main = $("#main");
    var splitbar = $("#split-bar");

    var h = (win.height() - 32) + "px";
    sidebar.css("height", h);
    main.css("height", h).css("max-height", h);
    splitbar.css("height", h);

    if (!window.sidebarClosed) {
        if ((ww - w) < 320) {
            sidebar.attr("class", "open overlay").width(w);
            main.css("left", 0).css("width", "100%")
        } else {
            sidebar.attr("class", "open").width(w);
            main.css("left", w).css("width", (ww - w) + "px");
        }
    }
}

function setSidebarWidth(w) {
    window.sidebarWidth = w;
    resetSidebar();
    setContentSizeClasses();
}

function scrollToSidebarHere() {
    var sbc = $("#sidebar-content");
    var here = sbc.find(".here");
    if (here.size() > 0) {
        var wh = $(window).height();
        var y = here.offset().top;
        sbc.scrollTop(y - (wh / 4));
    }
}

function dragSidebar(e) {
    e.preventDefault();
    if (window.sidebarClosed) {
        openSidebar();
    } else {
        var sidebar = $('#sidebar');
        $(document).mousemove(function (e) {
            e.preventDefault();
            var x = e.pageX - sidebar.offset().left;
            if (x > min && x < max && e.pageX < ($(window).width() - mainmin)) {
                window.sidebarClosed = false;
                setSidebarWidth(x);
            }
        })
    }
}

function updateHash() {
    var e = $(location.hash);
	
    var y = e.position().top;
    $("#main").scrollTop(y);
	
    // If the element is collapsible and collapsed, open it
    if (e.hasClass("collapsed")) {
        e.removeClass("collapsed");
    }
}

function zoomImage(e) {
    e.preventDefault();
    var el = $(this);
    var src = el.find("img").attr("src");
    var lbox = $("#lightbox");
    if (lbox.length == 0) {
        lbox = $("<div id='lightbox'><img src='" + src + "'/></div>");
        $("body").append(lbox);
        lbox.click(function(e) {
           lbox.hide();
        });
    } else {
        lbox.find("img").attr("src", src);
    }

    lbox.show();
    lbox.offset({left: 0, top: el.offset().top});
}

function setUpFilters() {
    $(".filtered").each(function() {
        var e = $(this);
        var controls = e.children(".filter-controls");
        var title = controls.find(".filter-title");
        var menus = controls.find(".filter-menu");
        var body = e.children(".filtered-body");

        // Add "collapse all" and "expand all" buttons if there are collapsibles
        // in the filtered body
        var collapses = body.find(".collapsible");
        if (collapses.size() >= 2) {
            var collapseall = $('<button>Collapse All</button>');
            var expandall = $('<button>Expand All</button>');
            collapseall.click(function() {
                collapses.addClass("collapsed");
            });
            expandall.click(function() {
                collapses.removeClass("collapsed");
            });
            controls.append(collapseall);
            controls.append(expandall);
        }

        menus.each(function() {
            var select = $(this);
            var counts = {};
            var name = select.attr("data-name");
            var value;

            body.find(".item[data-" + name + "]").each(function() {
                var valstring = $(this).attr("data-" + name);
                if (valstring && valstring !== "") {
                    var vallist;
                    if (name == "this") {
                        vallist = valstring.split(" ");
                    } else {
                        vallist = [valstring]
                    }
                    for (var i = 0; i < vallist.length; i++) {
                        value = vallist[i];
                        if (counts.hasOwnProperty(value)) {
                            counts[value] += 1;
                        } else {
                            counts[value] = 1;
                        }
                    }
                }
            });

            var allvalues = Object.keys(counts);
            if (allvalues.length > 0) {
                allvalues.sort();
                for (var i = 0; i < allvalues.length; i++) {
                    value = allvalues[i];
                    select.append($('<option>', {
                        value: value,
                        text : value + " (" + counts[value] + ")"
                    }));
                }

                select.change(function() {
                    runFilter(title, menus, body, true)
                });
            } else {
                var selectid = select.attr("id");
                $("#" + selectid + "_control").hide();
            }
        });

        title.keyup(function() {runFilter(title, menus, body)});
    });
}

function runFilter(title, menus, body, clear) {
    // Build a CSS selector...
    var selector = "";
    // For each menu in the filter ui
    menus.each(function() {
        // Grab the select element
        var select = $(this);
        // Get the search field name associated with it
        var name = select.attr("data-name");
        // Get the currently selected menu item's value
        var value = select.val();
        // The first/blank entry in the menu has the value "*" meaning no filter
        if (value != "*") {
            if (clear) title.val("");
            if (name == "tags") {
                selector += "[data-tags~=\"" + value + "\"]";
            } else {
                selector += "[data-" + name + "=\"" + value + "\"]";
            }
        }
    });

    // Add the text search filter value to the selector
    var text = title.val().toLowerCase();
    if (text !== "") {
        selector += "[data-title*=\"" + text + "\"]";
    }

    body.find("section.heading").show();
    body.find(".item").show();
    if (selector !== "") {
        body.find(".item:not(" + selector + ")").hide();

        // Hide headings if all items inside are hidden
        body.find("section.heading").each(function() {
            var h = $(this);
            var items = h.find(".item");
            if (!items.is(':visible')) {
                h.hide();
            } else {
                h.show();
            }
        })
    }
}

function setUpCharts(spec) {
    spec = spec || "#main";
    $(spec + " .chart").each(function() {
        var e = $(this);
        try {
            var data = JSON.parse(e.attr("data-data"));

            var opts = {
                shadowSize: 0
            };
            var options = JSON.parse(e.attr("data-options"));
            for (var k in options) {
                opts[k] = options[k];
            }

            options.shadowSize = 0;
            e.plot(data, opts).data("plot");
        } catch (e) {
            //
        }
    })
}

function setUpTabs() {
    $(".tab-group").each(function() {
        var e = $(this);
        var tabs = e.find(".tab-heading > .label");
        var bodies = e.find(".tab-bodies > .content");

        tabs.click(function() {
            var e = $(this);
            tabs.each(function() {
                $(this).removeClass("selected");
            });
            bodies.each(function() {
                $(this).removeClass("selected");
            });
            e.addClass("selected");
            $("#" + e.attr("for")).addClass("selected");
        })
    })
}

function setUpThumbnails() {
    $(".vimeo-reference").each(function() {
        var e = $(this);
        var vid = e.attr("data-vid");
        getVimeoThumbnail(vid, "small", function(imgurl) {
            e.find(".thumbnail").append(
                $("<img src='" + imgurl + "'>")
            )
        })
    })
}

function recordSidebarState() {
    Cookies.set("sidebarstate", {
        width: window.sidebarWidth,
        closed: window.sidebarClosed,
        query: $("#q").val()
    }, {path: "/"});
}

var min = 140;
var max = 3600;
var mainmin = 200;

function setUpPage() {
    var istop = window.self === window.top;

    if (istop) {
        $('#split-bar').mousedown(dragSidebar);
        $(document).mouseup(function(e) {
            $(document).unbind('mousemove');
        });
        var sbstate = Cookies.getJSON("sidebarstate");

        var sbox = $("#q");
        sbox.searchbox();
        if (sbstate) {
            window.sidebarWidth = sbstate["width"];
            if (sbstate["closed"]) {
                closeSidebar();
            } else {
                openSidebar();
            }
            sbox.val(sbstate["query"] || "");
        } else {
            recordSidebarState();
        }

        $("#menubtn").click(function(e) {
            toggleSidebar();
        });

        $(window).on("hashchange", updateHash);
        if (location.hash) {
            setTimeout(updateHash, 50);
        }

        if (window.sidebarClosed) {
            window.shouldScroll = true;
        } else {
            scrollToSidebarHere();
        }
    }

    $("img.animated").each(function() {
        var img = $(this);
        img.click(function() {
            var anim = img.attr("data-anim");
            var stat = img.attr("data-static");

            if (img.hasClass("running")) {
                img.removeClass("running");
                img.attr("src", stat);
            } else {
                img.addClass("running");
                img.attr("src", anim);
            }
        })
    });
    $(".billboard.animated").each(function() {
        var bb = $(this);
        bb.click(function() {
            var src = bb.css("background-image");
            var anim = "url('" + bb.attr("data-anim") + "')";
            var stat = "url('" + bb.attr("data-static") + "')";

            if (bb.hasClass("running")) {
                bb.removeClass("running");
                bb.css("background-image", stat);
            } else {
                bb.addClass("running");
                bb.css("background-image", anim);
            }
        })
    });
    $(".collapsible").each(function() {
        var w = $(this);
        // var c = w.children(".content");
        w.children(".label").click(function() {
            if (w.hasClass("collapsed")) {
                w.removeClass("collapsed");
            } else {
                w.addClass("collapsed");
            }
        })
    });
    $(".load-example").each(function() {
        var btn = $(this);
        btn.click(function(e) {
            var path = btn.attr("data-path");
            var launch = btn.attr("data-launch") == "True";
            loadExample(path, launch);
        })
    });

    $(window).resize(function(e) {
        if (istop) {
            resetSidebar();
        }
        setContentSizeClasses();
    });

    resetSidebar();
    setContentSizeClasses();
    setUpCharts();
    setUpFilters();
    setUpTabs();
    setUpThumbnails();
    $("figure.unzoomed").click(zoomImage).attr("title", "Click to zoom")
}

$(document).ready(setUpPage);
$(window).unload(recordSidebarState);
