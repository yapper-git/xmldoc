class XHTMLRenderer:
    
    def header(self, text, level):
        return "<h{0}>{1}</h{0}>".format(level, text)
    
    def paragraph(self, text, align):
        if align == "left":
            return "<p>" + text + "</p>"
        else:
            return '<p style="text-align: ' + align + '">' + text + "</p>"
    
    def blockquote(self, text):
        return "<blockquote>" + text + "</blockquote>"
    
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
        return "<strong>" + text + "</strong>"
    
    def italic(self, text):
        return "<em>" + text + "</em>"
    
    def superscript(self, text):
        return "<sup>" + text + "</sup>"
    
    def subscript(self, text):
        return "<sub>" + text + "</sub>"
    
    def highlight(self, text):
        return "<mark>" + text + "</mark>"
