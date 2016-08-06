import os
import re

from jinja2 import Environment, FileSystemLoader
from epub2 import EpubBuilder, EpubNavPoint

from xmldoc.renderer import Renderer

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


class EpubRenderer(Renderer):

    def header(self, element):
        text = self.inline(element)
        level = int(element.tag[1])
        if 'id' in element.attrib:
            return '<h{0} id="{2}">{1}</h{0}>\n'.format(level, text, element.attrib['id'])
        else:
            return '<h{0}>{1}</h{0}>\n'.format(level, text)

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
            output += '    <li>'

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
                output_child = output_child.replace('\n', '\n    ')
                output += output_child

            output += '</li>\n'

        return output

    def table(self, element):
        output = '<table>\n'
        for row_element in element:
            output += '    <tr>\n'
            for cell_element in row_element:
                tag = cell_element.tag
                text = self.inline(cell_element)
                align = cell_element.get('align', 'left')
                output += '    ' * 2
                if align == 'left':
                    output += '<{0}>{1}</{0}>\n'.format(tag, text)
                else:
                    output += '<{0} class="{1}">{2}</{0}>\n'.format(tag, align, text)
            output += '    </tr>\n'
        output += '</table>\n'
        return output

    def text(self, text):
        for old, new in replacements:
            text = text.replace(old, new)
        return text

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
        return '<span class="mark">{}</span>'.format(text)

Renderer.register(EpubRenderer)


class DocumentParser:

    def __init__(self):
        self.max_depth = 3
        self._pattern = re.compile("^h\d$")  # matches h1, h2, etc.

    def parse(self, root):
        self._parse_setup_sections(root)
        self._parse_setup_navpoints()
        for element in root:
            if self._pattern.search(element.tag):
                level = int(element.tag[1])
                if level == 1:
                    self._parse_header_sections(element)
                if level <= self.max_depth:
                    self._parse_header_navpoints(element, level)
            self.section_list[-1]['nodes'].append(element)

    def _parse_setup_sections(self, root):
        self.section_list = []
        self._section_number = 0
        first_node = root.find('*')
        if first_node is None or first_node.tag != 'h1':
            self.section_list.append({
                'id': 'section-0',
                'title': 'Introduction',  # FIXME i18n FIXME suitable expression?
                'nodes': []
            })

    def _parse_setup_navpoints(self):
        self.navpoints = []
        self._section_number = 0
        self._counters = []
        self._previous_level = 0
        self._previous_navpoint = None

    def _parse_header_sections(self, element):
        self._section_number += 1
        self.section_list.append({
            'id': 'section-{}'.format(self._section_number),
            'title': element.text,  # FIXME self.inline does no longer exists
            'nodes': []
        })

    def _parse_header_navpoints(self, element, level):
        navpoint = EpubNavPoint()
        navpoint.parent = None  # FIXME hack undefined…

        # id (e.g. "section-2.3") and source (e.g. "texts/section-2.xhtml#toc-3"
        if level > self._previous_level:
            self._counters.append(0)
        elif level < self._previous_level:
            self._counters = self._counters[0:level]
        self._counters[-1] += 1
        navpoint.id = "section-{}".format(".".join([str(x) for x in self._counters]))
        if level != 1:
            element.set('id', "toc-{}".format(".".join([str(x) for x in self._counters[1:]])))

        # source
        navpoint.source = "texts/section-{}.xhtml".format(self._section_number)
        if level != 1:
            navpoint.source += "#{}".format(element.get("id"))

        # title
        navpoint.label = htmlspecialchars(Renderer.strip(element))  # FIXME OK?

        # children
        navpoint.children = []

        # parent
        if level == 1:  # no parent
            navpoint.parent = None
        elif level == self._previous_level:  # same parent as previous navpoint
            navpoint.parent = self._previous_navpoint.parent
        elif level > self._previous_level:  # parent is the previous navpoint
            navpoint.parent = self._previous_navpoint
        elif level < self._previous_level:  # must rewind to find the correct parent
            navpoint.parent = self._previous_navpoint
            for _ in range(self._previous_level - level + 1):
                navpoint.parent = navpoint.parent.parent

        if navpoint.parent is None:
            self.navpoints.append(navpoint)
        else:
            navpoint.parent.children.append(navpoint)

        self._previous_level = level
        self._previous_navpoint = navpoint


class EpubExporter:

    contents_i18n = {
        'en': 'Table of Contents',
        'fr': 'Table des matières',
        'de': 'Inhaltsverzeichnis',
    }

    def run(self, document, filename):
        docparser = DocumentParser()
        docparser.parse(document.root)

        identifier = 'uuid'  # FIXME
        lang = document.manifest['lang']
        title = document.manifest['title']
        subtitle = document.manifest['subtitle']
        authors = document.manifest['authors']

        templates_folder = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'templates'
        )
        env = Environment(loader=FileSystemLoader(templates_folder))

        self.epub = EpubBuilder(filename)
        self.epub.identifier = identifier
        self.epub.title = title
        self.epub.metadata.add_language(lang)
        self.epub.open()

        # add navpoints
        for navpoint in docparser.navpoints:
            self.epub.add_navpoint(navpoint)

        # titlepage
        template = env.get_template('epub_titlepage.xhtml')
        self.epub.add_text_from_string(
            'texts/titlepage.xhtml',
            template.render(lang=lang, title=title, subtitle=subtitle, authors=', '.join(authors)),
            'titlepage'
        )
        template = env.get_template('epub_titlepage_style.css')
        self.epub.add_style_from_string('styles/titlepage.css', template.render(), 'style_titlepage')
        self.epub.add_guide("title-page", "Title page", "texts/titlepage.xhtml")

        # contents
        if docparser.navpoints:
            contents_title = self.contents_i18n[lang]
            template = env.get_template('epub_contents.xhtml')
            self.epub.add_text_from_string(
                'texts/contents.xhtml',
                template.render(lang=lang, title=contents_title, navpoints=self.epub.navpoints),
                'contents'
            )
            self.epub.add_guide("contents", contents_title, "texts/contents.xhtml")

        # add pages
        renderer = EpubRenderer()
        template = env.get_template('epub_main.xhtml')
        for section in docparser.section_list:
            self.epub.add_text_from_string(
                'texts/{}.xhtml'.format(section['id']),
                template.render(
                    lang=lang,
                    title=section['title'],
                    content=renderer.run(section['nodes']).rstrip().replace("\n", "\n    ")  # FIXME indent?
                ),
                section['id']
            )

        # add main.css
        template = env.get_template('epub_style.css')
        self.epub.add_style_from_string('styles/main.css', template.render(), 'style_main')

        self.epub.close()
