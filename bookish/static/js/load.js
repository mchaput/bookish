function tellHoudiniToLoad(file, launch, callback) {
    // Use XHR to communicate with an app on the help server,
    // which will then tell Houdini to load the example file.
    
    if (window.location.hostname == "www.sidefx.com") {
        alert(
            "Cannot load example files from the online Houdini help"
            + " documentation.  You can load example files from"
            + " the local help documentation that is in Houdini."
        );
    }

    try {
		$.ajax("/_load_example", {
			method: "POST",
			data: {
				url: file,
				launch: launch
			},
			error: function(xhr, status, err) {
				alert("Error loading example: " + err);
			},
			success: function(data, status, xhr) {
				// TODO: do something to the load UI to indicate success
			}
		})
    } catch(e) {
        alert("tellHoudiniToLoad: " + e);
    }
}

function loadExample(file, launch) {
    try {
        file = getExamplePrefix() + file;
        if (window.Python) {
            // This is an embedded browser, so we can use
            // RunPythonCommand to tell Houdini to load the file.
            launch = launch ? "True" : "False";
            var exp = "__import__('houdinihelp').load_example(\"" + file + "\", launch=" + launch + ")";
            Python.runStringExpression(exp, function(result) {
                if (result != "None") {
                    alert(result);
                }
            });
        } else {
            // This is an external browser, so use XHR to send
            // a request to the help server to load the file.
            
            //alert("tellHoudiniToLoad("+file+", "+launch+")")
            tellHoudiniToLoad(file, launch);
        }
    } catch(e) {
        alert("loadExample: " + e);
    }
}

function getExamplePrefix() {
    var pre = window.examplePrefix;
    if (pre) {
        if (pre.substr(pre.length-1, 1) == "/") {
            return pre.substr(0, pre.length-1);
        } else {
            return pre;
        }
    } else {
        return "$HFS/houdini/help";
    }
}
