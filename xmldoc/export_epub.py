from jinja2 import Environment, FileSystemLoader
import os

from epub2 import EpubBuilder, EpubNavPoint

from xmldoc.renderer import Renderer


class EpubRenderer(Renderer):

    replacements = [
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        # ('"', '&quot;'),
        # ("'", '&apos;'),
    ]

    def header(self, element):
        text = self.inline(element)
        level = int(element.tag[1])
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
        for old, new in self.replacements:
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


class EpubExporter:

    contents_i18n = {
        'en': 'Table of Contents',
        'fr': 'Table des matières',
        'de': 'Inhaltsverzeichnis',
    }

    def run(self, document, filename):
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

        epub = EpubBuilder(filename)
        epub.identifier = identifier
        epub.title = title
        epub.metadata.add_language(lang)
        epub.open()

        # titlepage
        template = env.get_template('epub_titlepage.xhtml')
        epub.add_text_from_string(
            'texts/titlepage.xhtml',
            template.render(lang=lang, title=title, subtitle=subtitle, authors=', '.join(authors)),
            'titlepage'
        )
        template = env.get_template('epub_titlepage_style.css')
        epub.add_style_from_string('styles/titlepage.css', template.render(), 'style_titlepage')
        epub.add_guide("title-page", "Title page", "texts/titlepage.xhtml")

        # add navpoints for h1
        number = 1
        for element in document.root:
            if element.tag == 'h1':
                navpoint = EpubNavPoint()
                navpoint.id = 'section-{}'.format(number)
                navpoint.label = Renderer.strip(element)
                navpoint.source = 'texts/section-{}.xhtml'.format(number)
                epub.add_navpoint(navpoint)
                number += 1

        # contents
        contents_title = self.contents_i18n[lang]
        template = env.get_template('epub_contents.xhtml')
        epub.add_text_from_string(
            'texts/contents.xhtml',
            template.render(lang=lang, title=contents_title, navpoints=epub.navpoints),
            'contents'
        )
        epub.add_guide("contents", contents_title, "texts/contents.xhtml")

        # main pages
        renderer = EpubRenderer()
        template = env.get_template('epub_main.xhtml')
        section_list = self.split_pages(document)
        for section in section_list:
            epub.add_text_from_string(
                'texts/{}.xhtml'.format(section['id']),
                template.render(
                    lang=lang,
                    title=section['title'],
                    content=renderer.run(section['nodes'])  # FIXME indent?
                ),
                section['id']
            )

        # add main.css
        template = env.get_template('epub_style.css')
        epub.add_style_from_string('styles/main.css', template.render(), 'style_main')

        epub.close()

    def split_pages(self, document):
        section_number = 0
        section_list = []

        # add section-0 if document does not start with <h1>
        first_node = document.root.find('*')
        if first_node.tag != 'h1':
            section_list.append({
                'id': 'section-0',
                'title': 'Introduction',  # FIXME i18n FIXME exact expression
                'nodes': []
            })

        for element in document.root:
            # create new section
            if element.tag == 'h1':
                section_number += 1
                section_list.append({
                    'id': 'section-{}'.format(section_number),
                    'title': element.text,  # FIXME self.inline does no longer exists
                    'nodes': []
                })

            # add element in the current section
            section_list[-1]['nodes'].append(element)

        return section_list
