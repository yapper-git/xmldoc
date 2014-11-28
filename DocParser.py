class DocParser:
    
    def __init__(self, root, renderer):
        self.root = root
        self.renderer = renderer
    
    def run(self):
        match = {
            "h1":          self.header,
            "h2":          self.header,
            "h3":          self.header,
            "h4":          self.header,
            "p":           self.paragraph,
            "blockquote":  self.blockquote,
            "ul":          self.unorderedList,
            "ol":          self.orderedList,
            "table":       self.table
        }
        text = ""
        for child in self.root:
            if child.tag in match:
                text += match[child.tag](child)
            else:
                assert False, "Unsupported tag name: " + child.tag
        return text
    
    def header(self, element):
        level = int(element.tag[1])
        return self.renderer.header(self.renderer.text(element.text), level)
    
    def paragraph(self, element):
        align = element.get("align", "left")
        return self.renderer.paragraph(self.inline(element), align)
    
    def blockquote(self, element):
        text = ""
        for child in element:
            assert child.tag == "p"
            text += self.paragraph(child)
        return self.renderer.blockquote(text)
    
    def unorderedList(self, element):
        text = ""
        for child in element:
            text += self.listItem(child)
        return self.renderer.unorderedList(text)
    
    def orderedList(self, element):
        text = ""
        for child in element:
            text += self.listItem(child)
        listType = element.get("type", "decimal")
        return self.renderer.orderedList(text, listType)
    
    def listItem(self, element):
        return self.renderer.listItem(self.inline(element))
    
    def table(self, element):
        text = ""
        for row in element:
            text += self.tableRow(row)
        return self.renderer.table(text)
    
    def tableRow(self, element):
        text = ""
        for cell in element:
            if cell.tag == "th":
                text += self.tableCellHeader(cell)
            else:
                text += self.tableCell(cell)
        return self.renderer.tableRow(text)
    
    def tableCell(self, element):
        align   = element.get("align", "left")
        rowspan = int(element.get("rowspan", "1"))
        colspan = int(element.get("colspan", "1"))
        return self.renderer.tableCell(self.inline(element), align, rowspan, colspan)
    
    def tableCellHeader(self, element):
        align   = element.get("align", "left")
        rowspan = int(element.get("rowspan", "1"))
        colspan = int(element.get("colspan", "1"))
        return self.renderer.tableCellHeader(self.inline(element), align, rowspan, colspan)
    
    def inline(self, element):
        match = {
            "br":   self.linebreak,
            "b":    self.bold,
            "i":    self.italic,
            "sup":  self.superscript,
            "sub":  self.subscript,
            "mark": self.highlight
        }
        text = self.renderer.text(element.text) if element.text else ""
        for child in element:
            text += match[child.tag](child)
            text += self.renderer.text(child.tail) if child.tail else ""
        return text
    
    def linebreak(self, element):
        return self.renderer.linebreak()
    
    def bold(self, element):
        return self.renderer.bold(self.inline(element))
    
    def italic(self, element):
        return self.renderer.italic(self.inline(element))
    
    def superscript(self, element):
        return self.renderer.superscript(self.inline(element))
    
    def subscript(self, element):
        return self.renderer.subscript(self.inline(element))
    
    def highlight(self, element):
        return self.renderer.highlight(self.inline(element))
