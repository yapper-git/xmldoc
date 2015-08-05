class DocParser:

    def __init__(self, root, renderer):
        self.root = root
        self.renderer = renderer

    def run(self):
        text = ""
        for child in self.root:
            if child.tag in ['h1', 'h2', 'h3', 'h4']:
                text += self.header(child)
            elif child.tag == 'p':
                text += self.paragraph(child)
            elif child.tag == 'blockquote':
                text += self.blockquote(child)
            elif child.tag == 'ul':
                text += self.unordered_list(child)
            elif child.tag == 'ol':
                text += self.ordered_list(child)
            elif child.tag == 'table':
                text += self.table(child)
            else:
                raise NotImplementedError("Unexpected {} tag".format(child.tag))
        return text

    def header(self, element):
        level = int(element.tag[1])
        return self.renderer.header(self.renderer.text(element.text), level)

    def paragraph(self, element):
        align = element.get('align', 'left')
        return self.renderer.paragraph(self.inline(element), align)

    def blockquote(self, element):
        text = ""
        for child in element:
            text += self.paragraph(child)
        return self.renderer.blockquote(text)

    def unordered_list(self, element):
        text = ""
        for child in element:
            text += self.list_item(child)
        return self.renderer.unordered_list(text)

    def ordered_list(self, element):
        text = ""
        for child in element:
            text += self.list_item(child)
        list_type = element.get('type', 'decimal')
        return self.renderer.ordered_list(text, list_type)

    def list_item(self, element):
        return self.renderer.list_item(self.inline(element))

    def table(self, element):
        text = ""
        for row in element:
            text += self.table_row(row)
        return self.renderer.table(text, len(element[0]))  # FIXME

    def table_row(self, element):
        text = ""
        for cell in element:
            if cell.tag == 'th':
                text += self.table_cell_header(cell)
            else:
                text += self.table_cell(cell)
        return self.renderer.table_row(text)

    def table_cell(self, element):
        align = element.get('align', 'left')
        rowspan = int(element.get('rowspan', 1))
        colspan = int(element.get('colspan', 1))
        return self.renderer.table_cell(self.inline(element), align, rowspan, colspan)

    def table_cell_header(self, element):
        align = element.get('align', 'left')
        rowspan = int(element.get('rowspan', 1))
        colspan = int(element.get('colspan', 1))
        return self.renderer.table_cell_header(self.inline(element), align, rowspan, colspan)

    def inline(self, element):
        match = {
            'br':   self.linebreak,
            'b':    self.bold,
            'i':    self.italic,
            'sup':  self.superscript,
            'sub':  self.subscript,
            'mark': self.highlight,
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
