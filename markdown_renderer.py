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
        text = self.wrap(text)
        if align == "right":
            lines = text.split("\n")
            lines = ["{0:>{1}}".format(line, self.width) for line in lines]
            return "\n".join(lines) + "\n\n"
        elif align == "center":
            lines = text.split("\n")
            lines = [line.center(self.width) for line in lines]
            return "\n".join(lines) + "\n\n"
        else:
            return text + "\n\n"

    def blockquote(self, text):
        return "> " + textwrap.fill(text, self.width-2).replace("\n", "\n> ") + "\n\n"

    def ordered_list(self, text, listType):
        return text + "\n"

    def unordered_list(self, text):
        return text + "\n"

    def list_item(self, text):
        return "* {}".format(text)+"\n"

    def table(self, text):
        return ""

    def table_row(self, text):
        return ""

    def table_cell(self, text, align, colspan, rowspan):
        return ""

    def table_cell_header(self, text, align, colspan, rowspan):
        return ""

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
