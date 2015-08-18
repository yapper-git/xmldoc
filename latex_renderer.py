from jinja2 import Environment, FileSystemLoader
import os

from renderer import Renderer


class LaTeXRenderer(Renderer):

    replacements = [  # order matters, 10 special characters
        ('\\', r'\\'),
        ('#', r'\#'),
        ('$', r'\$'),
        ('%', r'\%'),
        ('&', r'\&'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('^', r'\textasciicircum{}'),
        ('~', r'\textasciitilde{}'),
        (r'\\', r'\textbackslash{}'),
    ]

    def run(self):
        lang = self.document.manifest['lang']
        title = self.document.manifest['title']
        subtitle = self.document.manifest['subtitle']
        authors = ', '.join(self.document.manifest['authors'])

        self.packages = []

        templates_folder = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'templates'
        )
        env = Environment(loader=FileSystemLoader(templates_folder))
        template = env.get_template('latex_render.tex')
        return template.render(
            lang=lang,
            title=title,
            subtitle=subtitle,
            authors=authors,
            packages=self.packages,
            main_content=super(LaTeXRenderer, self).run().rstrip(),
        )

    def usepackage(self, pkg_name):
        if pkg_name not in self.packages:
            self.packages.append(pkg_name)

    @staticmethod
    def indent(text, level=1):
        text_indent = '    ' * level
        return (text_indent + text).replace('\n', '\n' + text_indent)

    def header(self, element):
        text = self.inline(element)
        level = int(element.tag[1])
        if level == 1:
            return '\\section{%s}\n\n' % text
        if level == 2:
            return '\\subsection{%s}\n\n' % text
        if level == 3:
            return '\\subsubsection{%s}\n\n' % text
        if level == 4:
            return '\\textbf{\\small %s}\n\n' % text
        raise NotImplementedError("Unexpected '{}' level attribute".format(level))

    def paragraph(self, element):
        text = self.inline(element)
        align = element.get('align', 'left')
        if align == 'left':
            return '%s\n\n' % text
        if align == 'right':
            return '\\begin{flushright}\n%s\n\\end{flushright}\n\n' % text
        if align == 'center':
            return '\\begin{center}\n%s\n\\end{center}\n\n' % text
        raise NotImplementedError("Unexpected '{}' align attribute".format(align))

    def blockquote(self, element):
        output = '\\begin{quotation}\n'
        for child_element in element:
            output += self.paragraph(child_element)
        output = output.rstrip()
        output += '\n\\end{quotation}\n\n'
        return output

    def unordered_list(self, element):
        output = '\\begin{itemize}'
        output += self.list(element)
        output += '\n\\end{itemize}\n\n'
        return output

    def ordered_list(self, element):
        output = '\\begin{enumerate}%s' % self.ordered_list_label(element)
        output += self.list(element)
        output += '\n\\end{enumerate}\n\n'
        return output

    def list(self, element):
        output = ''
        for li_element in element:
            output += '\n\\item'

            # text
            output_text = self.inline(li_element)
            if output_text:
                output += '\n    %s' % output_text

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
        return output

    def ordered_list_label(self, element):
        list_type = element.get('type', 'decimal')

        if list_type == 'decimal':
            return ''

        self.usepackage('enumitem')
        if list_type == 'lower-alpha':
            return r'[label=\alph*.]'
        if list_type == 'upper-alpha':
            return r'[label=\Alph*.]'
        if list_type == 'lower-roman':
            return r'[label=\roman*.]'
        if list_type == 'upper-roman':
            return r'[label=\Roman*.]'

        raise NotImplementedError("Unexpected {} type attribute".format(list_type))

    def table(self, element):
        self.usepackage('tabulary')
        num_cols = len(list(element[0]))
        param = '{' + ('|L' * num_cols) + '|}'  # FIXME align L? C? R?
        output = '\\begin{center}\n\\begin{tabulary}{\\textwidth}' + param + '\n'
        for i, row_element in enumerate(element):
            if i == 0:
                output += '\\hline\n'
            for j, cell_element in enumerate(row_element):
                output += '    ' if j == 0 else ' & '
                output += self.inline(cell_element)
            output += ' \\\\\n\\hline\n'
        output += '\\end{tabulary}\n\\end{center}\n\n'
        return output

    def text(self, text):
        for old, new in self.replacements:
            text = text.replace(old, new)
        return text

    def linebreak(self, text):
        return r'\\'  # or \newline

    def bold(self, text):
        return r'\textbf{%s}' % text

    def italic(self, text):
        return r'\textit{%s}' % text

    def superscript(self, text):
        return r'\textsuperscript{%s}' % text

    def subscript(self, text):
        self.usepackage('fixltx2e')
        return r'\textsubscript{%s}' % text

    def highlight(self, text):
        self.usepackage('color,soul')
        return r'\hl{%s}' % text

Renderer.register(LaTeXRenderer)
