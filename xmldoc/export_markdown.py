import textwrap

from xmldoc.renderer import Renderer


class MarkdownRenderer(Renderer):

    width = 80

    def wrap(self, text):
        return textwrap.fill(text, self.width)

    def header(self, element):
        level = int(element.tag[1]) + 1
        title = self.inline(element)
        return self.wrap(("#" * level) + " " + title) + "\n\n"

    def paragraph_wrap(self, element, width):
        text = textwrap.fill(self.inline(element), width)
        align = element.get("align", "left")
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

    def paragraph(self, element):
        return self.paragraph_wrap(element, self.width) + "\n\n"

    def blockquote(self, element):
        output = ""
        for child_element in element:
            output += self.paragraph(child_element) + "\n\n"
        output = output.rstrip()
        return "> " + output.replace("\n", "\n> ") + "\n\n"

    def ordered_list(self, element):
        return "[<ol> not supported]\n\n"

    def unordered_list(self, element):
        return "[<ul> not supported]\n\n"

    def table(self, element):
        return "[<table> not supported]\n\n"

    def text(self, text):
        return text.replace("*", "\\*")

    def linebreak(self, text):
        return "<br/>"

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

Renderer.register(MarkdownRenderer)


class MarkdownExporter:

    @staticmethod
    def run(document):
        output = document.manifest['title'] + "\n"
        output += "=" * max(5, len(document.manifest['title'])) + "\n\n"

        renderer = MarkdownRenderer()
        output += renderer.run(document.root)

        return output
