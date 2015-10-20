import re

from xmldoc.renderer import Renderer


tab = "  "

replacements = [
    ('&', '&amp;'),  # order matters
    ('<', '&lt;'),
    ('>', '&gt;'),
    # ('"', '&quot;'),
    # ("'", '&apos;'),
]


def htmlspecialchars(text):
    for old, new in replacements:
        text = text.replace(old, new)
    return text


class HeadersParser:

    def __init__(self):
        self.max_depth = 3

    def parse(self, root):
        pattern = re.compile("^h\d$")  # matches h1, h2, etc.
        self.counters = []
        self.previous_level = 0
        self.previous_navpoint = None
        self.navpoints = []
        for element in root:
            if pattern.search(element.tag):
                self.parse_header(element)

    def parse_header(self, element):
        level = int(element.tag[1])

        if level > self.max_depth:
            return

        navpoint = {}

        # id (for instance "toc-2.3")
        if level > self.previous_level:
            self.counters.append(0)
        elif level < self.previous_level:
            self.counters = self.counters[0:level]
        self.counters[-1] += 1
        navpoint['id'] = "toc-{}".format(".".join([str(x) for x in self.counters]))
        element.set('id', navpoint['id'])

        # title
        navpoint['title'] = Renderer.strip(element)

        # children
        navpoint['children'] = []

        # parent
        if level == 1:  # no parent
            navpoint['parent'] = None
        elif level == self.previous_level:  # same parent as previous navpoint
            navpoint['parent'] = self.previous_navpoint['parent']
        elif level > self.previous_level:  # parent is the previous navpoint
            navpoint['parent'] = self.previous_navpoint
        elif level < self.previous_level:  # must rewind to find the correct parent
            raise Exception('TODO')
            navpoint['parent'] = self.previous_navpoint
            for _ in range(self.previous_level - level + 1):
                navpoint['parent'] = navpoint['parent']['parent']

        if navpoint['parent'] == None:
            self.navpoints.append(navpoint)
        else:
            navpoint['parent']['children'].append(navpoint)

        self.previous_level = level
        self.previous_navpoint = navpoint


class ContentsRenderer:

    @classmethod
    def render(cls, navpoints):
        return cls.render_recursive(navpoints, 0)

    @classmethod
    def render_recursive(cls, navpoints, level):
        output = (tab * level) + "<ul>\n"
        for navpoint in navpoints:
            title = '<a href="#{}">{}</a>'.format(navpoint['id'], htmlspecialchars(navpoint['title']))
            if len(navpoint['children']) == 0:
                output += (tab * (level + 1)) + "<li>" + title + "</li>\n"
            else:
                output += (tab * (level + 1)) + "<li>\n"
                output += (tab * (level + 2)) + title + "\n"
                output += cls.render_recursive(navpoint['children'], level + 2) + "\n"
                output += (tab * (level + 1)) + "</li>\n"
        output += (tab * level) + "</ul>"
        return output


class HtmlRenderer(Renderer):

    def __init__(self):
        self.headers_offset = 0

    def header(self, element):
        text = self.inline(element)
        level = int(element.tag[1])
        if 'id' in element.attrib:
            return '<h{0} id="{2}">{1}</h{0}>\n'.format(level + self.headers_offset, text, element.attrib['id'])
        else:
            return '<h{0}>{1}</h{0}>\n'.format(level + self.headers_offset, text)

    def paragraph(self, element):
        text = self.inline(element)
        align = element.get('align', 'left')
        if align == 'left':
            return '<p>{}</p>\n'.format(text)
        else:
            return '<p class="{}">{}</p>\n'.format(align, text)

    def blockquote(self, element):
        output = '<blockquote>\n'
        for child_element in element:
            output += self.paragraph(child_element)
        output += '</blockquote>\n'
        return output

    def unordered_list(self, element):
        output = '<ul>\n'
        output += self.list(element)
        output += '</ul>\n'
        return output

    def ordered_list(self, element):
        list_type = element.get('type', 'decimal')
        if list_type == 'decimal':
            output = '<ol>\n'
        else:
            output = '<ol class="{}">\n'.format(list_type)
        output += self.list(element)
        output += '</ol>\n'
        return output

    def list(self, element):
        output = ''
        for li_element in element:
            output += tab + '<li>'

            # text
            output_text = self.inline(li_element)
            if output_text:
                output += output_text

            # child ul or ol
            child_ul, child_ol = li_element.find('ul'), li_element.find('ol')
            if child_ul or child_ol:
                output_child = '\n'
                if child_ul:
                    output_child += self.unordered_list(child_ul).rstrip()
                if child_ol:
                    output_child += self.ordered_list(child_ol).rstrip()
                output_child = output_child.replace('\n', '\n' + tab * 2)
                output += output_child
                output += "\n" + tab

            output += '</li>\n'

        return output

    def table(self, element):
        output = '<table>\n'
        for row_element in element:
            output += tab + '<tr>\n'
            for cell_element in row_element:
                tag = cell_element.tag
                text = self.inline(cell_element)
                align = cell_element.get('align', 'left')
                output += tab * 2
                if align == 'left':
                    output += '<{0}>{1}</{0}>\n'.format(tag, text)
                else:
                    output += '<{0} class="{1}">{2}</{0}>\n'.format(tag, align, text)
            output += tab + '</tr>\n'
        output += '</table>\n'
        return output

    def text(self, text):
        return htmlspecialchars(text)

    def linebreak(self, text):
        return '<br/>'

    def bold(self, text):
        return '<strong>{}</strong>'.format(text)

    def italic(self, text):
        return '<em>{}</em>'.format(text)

    def superscript(self, text):
        return '<sup>{}</sup>'.format(text)

    def subscript(self, text):
        return '<sub>{}</sub>'.format(text)

    def highlight(self, text):
        return '<mark>{}</mark>'.format(text)

Renderer.register(HtmlRenderer)


class HtmlExporter:

    contents_i18n = {
        'en': 'Table of Contents',
        'fr': 'Table des matières',
        'de': 'Inhaltsverzeichnis',
    }

    def run(self, document):
        toc_title = self.contents_i18n[document.manifest['lang']]  # FIXME

        headers_parser = HeadersParser()
        headers_parser.parse(document.root)
        toc_render = ContentsRenderer().render(headers_parser.navpoints)

        body_render = HtmlRenderer().run(document.root)

        return toc_title + '\n\n' + toc_render + '\n\n' + body_render
