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

    def ordered_list(self, text, listType):
        return '<ol style="list-style-type: {}">{}</ol>'.format(listType, text)

    def unordered_list(self, text):
        return "<ul>{}</ul>".format(text)

    def list_item(self, text):
        return "<li>{}</li>".format(text)

    def table(self, text, num_cols):
        return "<table>{}</table>".format(text)

    def table_row(self, text):
        return "<tr>{}</tr>".format(text)

    def _table_cell(self, name, text, align, colspan, rowspan):
        attribs = {}
        if align:
            attribs["style"] = "text-align: {}".format(align)
        if colspan != 1:
            attribs["colspan"] = colspan
        if rowspan != 1:
            attribs["rowspan"] = rowspan
        return "<{tag}{attribs}>{text}</{tag}>".format(
            tag=name,
            attribs="".join([
                ' {}="{}"'.format(key, value)
                for (key, value) in attribs.items()]),
            text=text)

    def table_cell(self, text, align, colspan, rowspan):
        return self._table_cell("td", text, align, colspan, rowspan)

    def table_cell_header(self, text, align, colspan, rowspan):
        return self._table_cell("th", text, align, colspan, rowspan)

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
