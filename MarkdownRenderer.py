import textwrap

class MarkdownRenderer:
    
    def __init__(self):
        self.width = 80
    
    def text(self, text):
        return text.replace("*", "\\*")
    
    def wrap(self, text):
        return textwrap.fill(text, self.width)
    
    def header(self, text, level):
        return self.wrap(("#" * level) + " " + text) + "\n\n"
    
    def paragraph(self, text, align):
        if align == "right":
            return "{0:>{1}}".format(self.wrap(text), self.width) + "\n\n"
        elif align == "center":
            return self.wrap(text).center(self.width) + "\n\n"
        else:
            return self.wrap(text) + "\n\n"
    
    def blockquote(self, text):
        return "> " + textwrap.fill(text, self.width-2).replace("\n", "\n> ")
    
    def orderedList(self, text, listType):
        return '<ol style="list-style-type: {}">{}</ol>'.format(listType, text)
    
    def unorderedList(self, text):
        return "\n".format(text)
    
    def listItem(self, text):
        return "* {}".format(text)
    
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
        return "**{}**".format(text)
    
    def italic(self, text):
        return "*{}*".format(text)
    
    def superscript(self, text):
        return "^({})".format(text)
    
    def subscript(self, text):
        return "_({})".format(text)
    
    def highlight(self, text):
        return "<mark>{}</mark>".format(text)
