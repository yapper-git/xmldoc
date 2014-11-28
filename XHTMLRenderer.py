class XHTMLRenderer:
    
    def text(self, text):
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        return text
    
    def header(self, text, level):
        return "<h{0}>{1}</h{0}>".format(level, text)
    
    def paragraph(self, text, align):
        if align == "left":
            return "<p>{}</p>".format(text)
        else:
            return '<p style="text-align: {}">{}</p>'.format(align, text)
    
    def blockquote(self, text):
        return "<blockquote>{}</blockquote>".format(text)
    
    def orderedList(self, text, listType):
        return '<ol style="list-style-type: {}">{}</ol>'.format(listType, text)
    
    def unorderedList(self, text):
        return "<ul>{}</ul>".format(text)
    
    def listItem(self, text):
        return "<li>{}</li>".format(text)
    
    def table(self, text):
        return "<table>{}</table>".format(text)
    
    def tableRow(self, text):
        return "<tr>{}</tr>".format(text)
    
    def tableCell(self, text, align, colspan, rowspan):
        # TODO colspan, rowspan, align support
        return '<td>{}</td>'.format(text)
    
    def tableCellHeader(self, text, align, colspan, rowspan):
        # TODO colspan, rowspan, align support
        return '<th>{}</th>'.format(text)
    
    def linebreak(self):
        return "<br />"
    
    def bold(self, text):
        return "<strong>{}</strong>".format(text)
    
    def italic(self, text):
        return "<em>{}</em>".format(text)
    
    def superscript(self, text):
        return "<sup>{}</sup>".format(text)
    
    def subscript(self, text):
        return "<sub>{}</sub>".format(text)
    
    def highlight(self, text):
        return "<mark>{}</mark>".format(text)
