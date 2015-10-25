import re

from xmldoc.renderer import Renderer


tab = "  "


def htmlspecialchars(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    # text = text.replace('"', '&quot;').replace("'", '&apos;')
    return text


class DocumentParser:

    def __init__(self):
        self.max_depth = 3
        self._html_renderer = HtmlRenderer()

    def parse(self, root):
        self.navpoints = []
        pattern = re.compile("^h\d$")  # matches h1, h2, etc.
        self._counters = []
        self._previous_level = 0
        self._previous_navpoint = None
        for element in root:
            if pattern.search(element.tag):
                self.parse_header(element)

    def parse_header(self, element):
        self._level = int(element.tag[1])

        # update counters (e.g. [2, 3] or [2, 3, 1, 4])
        if self._level > self._previous_level:
            self._counters.append(0)
        elif self._level < self._previous_level:
            self._counters = self._counters[0:self._level]
        self._counters[-1] += 1
        self._anchor = "toc-{}".format(".".join([str(x) for x in self._counters]))

        # set header ID (e.g. id="toc-2.3")
        element.set('id', self._anchor)

        # add navpoint (only if it ) FIXME
        if self._level <= self.max_depth:
            self._parse_header_navpoint(element)

        self._previous_level = self._level

    def _parse_header_navpoint(self, element):
        navpoint = {}

        # set id (for instance "toc-2.3")
        navpoint['id'] = self._anchor

        # set title
        navpoint['title'] = self._html_renderer.inline(element)

        # set children
        navpoint['children'] = []

        # set parent
        previous_level = min(self._previous_level, self.max_depth)
        if self._level == 1:  # no parent
            navpoint['parent'] = None
        elif self._level == previous_level:  # same parent as previous navpoint
            navpoint['parent'] = self._previous_navpoint['parent']
        elif self._level > previous_level:  # parent is the previous navpoint
            navpoint['parent'] = self._previous_navpoint
        elif self._level < previous_level:  # must rewind to find the correct parent
            print(self._counters)
            print("{} → {}".format(self._level, previous_level))
            navpoint['parent'] = self._previous_navpoint
            for _ in range(previous_level - self._level + 1):
                navpoint['parent'] = navpoint['parent']['parent']

        # add navpoint either to root list or to its parent
        if navpoint['parent'] == None:
            self.navpoints.append(navpoint)
        else:
            navpoint['parent']['children'].append(navpoint)

        self._previous_navpoint = navpoint


class ContentsRenderer:

    @classmethod
    def render(cls, navpoints):
        return cls.render_recursive(navpoints, 0)

    @classmethod
    def render_recursive(cls, navpoints, level):
        output = (tab * level) + "<ul>\n"
        for navpoint in navpoints:
            title = '<a href="#{}">{}</a>'.format(navpoint['id'], navpoint['title'])
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
            return '<p class="align-{}">{}</p>\n'.format(align, text)

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
            output = '<ol style="list-style-type: {}">\n'.format(list_type)
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
        output = '<table class="ink-table alternating bordered">\n'
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
        docparser = DocumentParser()
        docparser.parse(document.root)
        navpoints = docparser.navpoints

        prefix = " " * 12
        output = prefix
        if len(navpoints) != 0:
            toc_title = self.contents_i18n[document.manifest['lang']]  # FIXME KeyError?
            output += '<h3 id="toc">' + toc_title + "</h3>\n"
            output += ContentsRenderer.render(navpoints) + "\n"
            output += "<hr/>\n"
        output += HtmlRenderer().run(document.root)

        return output.replace("\n", "\n" + prefix)
