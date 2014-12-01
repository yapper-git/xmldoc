#!/usr/bin/env python3

import xml.etree.ElementTree as ET

from DocParser import *
from XHTMLRenderer import *
import epub2

OUTPUT = "extracts.epub"
IDENTIFIER = "helloworld"
TITLE = "en_US"
LANGUAGE = "en-US"
EXTRACTS = [
    {"id": "extract1", "file": "extract1.xml", "title": "Extract N°1"},
    {"id": "extract2", "file": "extract2.xml", "title": "Extract N°2"},
]

epub = epub2.Epub(OUTPUT)
epub.open()

epub.identifier = IDENTIFIER
epub.title = TITLE
epub.language = LANGUAGE

for extract in EXTRACTS:
    root = ET.parse(extract["file"]).getroot()
    parser = DocParser(root, XHTMLRenderer())
    html_content = parser.run()

    epub.contents.addNavPoint(epub2.NavPoint(extract["id"], extract["id"],
                                             extract["id"]+".xhtml"))
    epub.addTextFromString(id=extract["id"], localname=extract["id"]+".xhtml", content="""<?xml version="1.0" encoding="UTF-8" ?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
          <head>
            <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
            <title>{title}</title>
            <!--<link rel="stylesheet" href="main.css" type="text/css" />-->
          </head>
          <body>
            <h1>{title}</h1>
            {body}
          </body>
        </html>""".format(body=html_content, title=extract['title'], lang=LANGUAGE))

epub.close()
