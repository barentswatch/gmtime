Gmaps - wmstime
===============

Example on how to parse getCapabilities from a WMS server, extract time attribute and show on a Google maps page


Usage
-----

1. create a virtualenv
2. source it
3. install requirements (pip install -r requirements.txt)
4. run: python app.py
5. navigate your browser to localhost:5000

Known issues
------------
- Requests WMS as tiles.. not optimal for performance
- slow and inefficient, meant as an example

Code from
---------
The WMS-to gmaps code is based on google-maps-api-with-wms-overlay from http://code.google.com/p/google-maps-api-with-wms-overlay/, which is BSD-3-clause lisenced.