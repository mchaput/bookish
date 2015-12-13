This is the initial commit of existing code for the Bookish wiki documentation server. Bookish is the server included with Side Effect Software's Houdini 3D animation and effects software. It features a system for parsing wiki markup into JSON (including the ability to use different markup grammars easily), middleware for transforming JSON documents, a system for rendering JSON to HTML using XSLT-like stylesheets, and a server based on Flask and Whoosh for viewing and searching documentation.

Currently the code itself is not particularly useful because it doesn't include the Houdini documentation, and has Houdini-specific configuration.

The easiest way to try out the server is actually to install the free "Apprentice" version of Houdini. (These instructions are for the Mac).

1. Go to ``sidefx.com/download`` and choose the platform to download for (Mac, Windows, or Linux). Make sure to click Latest Daily Build. Then click Download Houdini.

2. When the package finishes downloading, open it and run the installer, accepting the defaults.

3. When intallation is finished, go to the install location (e.g. /Applications/Houdini X.Y.Z/ on Mac).

4. Open "Houdini Apprentice".

   When the Houdini License Adminstrator window appears, click "Install my free Houdini Apprentice license" and click Next, then accept the license agreement. When a dialog appears saying the license is installed, click Run.

5. In Houdini, choose Help > Contents.

6. After the browser window appears, close it. (The embedded browser is a very old version of Webkit, so it's better to use an external browser. We just needed to force Houdini to start the help server.)

7. In Safari or Chrome, go to ``localhost:48626``.






