import epub2

with epub2.Epub("hello.epub"):
    epub.identifier = "helloworld"
    epub.title = "Hello world!"
    epub.language = "en-US"
    
    epub.contents.addNavPoint(epub2.NavPoint("hello", "hello", "hello.xhtml"))
    
    epub.addTextFromString(id="hello", localname="hello.xhtml", content="""<?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
      <head>
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <title>Hello world!</title>
        <link rel="stylesheet" href="main.css" type="text/css" />
      </head>
      <body>
        <h1>Hello world!</h1>
      </body>
    </html>""")
    
    epub.addStyleFromString("main.css", """h1 {
        color: red
    }""", "style")
