jQuery.fn.searchbox = function(url, queryopts, delay) {
	return this.each(function(){
		if (queryopts == undefined) {
			queryopts = {};
		}
		if (delay == undefined) {
			delay = 200;
		}
		
		var textbox = $(this);
		
		var resultcount = 0;
		var selected = 0;
		var resultsdivid = textbox.attr("id") + "results";
		var timer = null;
		
		var lastsearch = textbox.val();
		
		// Create the results div
        var resultsdiv = $('<div id="' + resultsdivid + '"> </div>');
        resultsdiv.attr("class", "searchboxresults");
        $("body").append(resultsdiv);

		// Get the field position and size
		var position = textbox.offset();
		var top = position.top;
		var left = position.left;
		var width = textbox.width();
		var height = textbox.height();
		
		var latest = 0;
		
		resultsdiv.css("position", "absolute");
		resultsdiv.css("left", left + "px");
		resultsdiv.css("top", (top + height) + "px");
		//resultsdiv.css("width", width);
		
		textbox.blur(function() {
			setTimeout(clearResults, 100);
		});
		
		textbox.focus(function() {
			if (resultcount > 0) {
				showResults();
			}
		});
		
		function updateCss() {
			resultsdiv.find("div").each(function(i) {
				if (i == selected) {
					$(this).addClass("selected");
				} else {
					$(this).removeClass("selected");
				}
			});
		};
		
		function enterClick() {
			var value = url + "?q=" + escape(textbox.value());
			var selecteddiv = resultsdiv.find("div.selected");
			if (selecteddiv) {
				var sdiv = $(selecteddiv).find("input");
				if (sdiv) {
					value = sdiv.val();
				}
			}
			window.location = value;
		}
		
		function fillResults(html) {
			html = $(html);
			var sentat = Number(html.find("#sentat").val());
			if (sentat <= latest) {
				return;
			}
			latest = sentat;
			
			var divs = html.find("div");
			resultsdiv.html("");
			resultsdiv.append(html);
			resultcount = 0;
			
			if (divs.size()) {
				//resultsdiv.append(divs);
				//resultsdiv.highlight(lastsearch);
				resultsdiv.css("display", "block");
				resultcount = divs.size();
				
				divs.mouseover(function() {
					var me = this;
					var count = 0;
					divs.each(function() {
						if (me === this) {
							selected = count;
						}
						$(this).removeClass("selected");
						count++;
					});
					$(me).addClass("selected")
				});
				
				divs.click(function() {
					window.location = $(this).find("input").val();
				});
				
				updateCss();
			} else {
				clearResults();
			}
		}
		
		function updateResults() {
			var query = textbox.val();
			if (query == "") {
				clearResults();
				return;
			}
			
			if (lastsearch == query) {
				return;
			}
			lastsearch = query;
			
			$.ajax({
				"type": "GET",
				"url": url,
				"data": jQuery.extend(queryopts, {"q": query, "sentat": new Date().getTime()}),
				"cache": false,
				"success": fillResults,
				"dataType": "html"
			});
		}
		
		function clearResults() {
			resultsdiv.css("display", "none");
		}
		
		function showResults() {
			resultsdiv.css("display", "block");
		}
		
		textbox.keydown(function(e) {
			var keycode = e.keyCode || window.event.keyCode;
			var rc = true;
			
			if (keycode == 13) {
				// Enter
				enterClick();
				return false;
			} else if (keycode == 27) {
				// Escape
				clearResults();
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
			
			timer = setTimeout(updateResults, delay);
			return rc;
		});
	});
};
