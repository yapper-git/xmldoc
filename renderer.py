import abc
import re
import xml.etree.ElementTree as ET


class Renderer(metaclass=abc.ABCMeta):

    regex = re.compile(r'\s+')

    def __init__(self, document):
        self.document = document

    def run(self):
        output = ""
        for child in self.document.root:
            if child.tag in ['h1', 'h2', 'h3', 'h4']:
                output += self.header(child)
            elif child.tag == 'p':
                output += self.paragraph(child)
            elif child.tag == 'blockquote':
                output += self.blockquote(child)
            elif child.tag == 'ul':
                output += self.unordered_list(child)
            elif child.tag == 'ol':
                output += self.ordered_list(child)
            elif child.tag == 'table':
                output += self.table(child)
            else:
                raise KeyError("Unexpected {} tag".format(child.tag))
        return output

    def inline(self, element, strip=True):
        match = {
            'br': self.linebreak,
            'b': self.bold,
            'i': self.italic,
            'sup': self.superscript,
            'sub': self.subscript,
            'mark': self.highlight,
        }

        text = ''
        if element.text:
            text += self.text(self.regex.sub(' ', element.text))
        for child in element:
            try:
                if child.tag not in ['ul', 'ol']:  # ignore ul and ol elements
                    text += match[child.tag](self.inline(child, False))
            except KeyError:
                raise KeyError("Unexpected {} tag".format(child.tag))
            if child.tail:
                text += self.text(self.regex.sub(' ', child.tail))
        return text.strip() if strip else text

    @abc.abstractmethod
    def header(self, element):
        return

    @abc.abstractmethod
    def paragraph(self, element):
        return

    @abc.abstractmethod
    def blockquote(self, element):
        return

    @abc.abstractmethod
    def ordered_list(self, element):
        return

    @abc.abstractmethod
    def unordered_list(self, element):
        return

    @abc.abstractmethod
    def table(self, element):
        return

    @abc.abstractmethod
    def text(self, text):
        return

    @abc.abstractmethod
    def linebreak(self, text):
        return

    @abc.abstractmethod
    def bold(self, text):
        return

    @abc.abstractmethod
    def italic(self, text):
        return

    @abc.abstractmethod
    def superscript(self, text):
        return

    @abc.abstractmethod
    def subscript(self, text):
        return

    @abc.abstractmethod
    def highlight(self, text):
        return
