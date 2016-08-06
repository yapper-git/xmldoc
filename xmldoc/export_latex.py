from jinja2 import Environment, FileSystemLoader
import os

from xmldoc.renderer import Renderer


class LatexRenderer(Renderer):

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

    def run(self, root):
        self.packages = []
        return super(LatexRenderer, self).run(root).rstrip()

    def usepackage(self, pkg_name):
        if pkg_name not in self.packages:
            self.packages.append(pkg_name)

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
        output = output.rstrip() + '\n'
        output += '\\end{quotation}\n\n'
        return output

    def unordered_list(self, element):
        output = '\\begin{itemize}'
        output += self.list(element) + '\n'
        output += '\\end{itemize}\n\n'
        return output

    def ordered_list(self, element):
        output = '\\begin{enumerate}%s' % self.ordered_list_label(element)
        output += self.list(element) + '\n'
        output += '\\end{enumerate}\n\n'
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
        param = '{' + ('|L' * num_cols) + '|}'
        output = '\\begin{center}\n\\begin{tabulary}{\\textwidth}' + param + '\n'
        for i, row_element in enumerate(element):
            if i == 0:
                output += '\\hline\n'
            for j, cell_element in enumerate(row_element):

                # add bold for cell headers
                text = self.inline(cell_element)
                if cell_element.tag == 'th':
                    text = '\\textbf{%s}' % text

                # change left alignemnt if needed
                align = cell_element.get('align', 'left')
                if align == 'center':
                    text = r'\centering\arraybackslash %s' % text
                elif align == 'right':
                    text = r'\raggedleft\arraybackslash %s' % text

                output += '    ' if j == 0 else ' & '
                output += text

            output += ' \\\\\n\\hline\n'
        output += '\\end{tabulary}\n\\end{center}\n\n'
        return output

    def text(self, text):
        for old, new in self.replacements:
            text = text.replace(old, new)
        return text

    def linebreak(self, text):
        return r'\newline '  # avoid confusion with \\ in table cells

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

Renderer.register(LatexRenderer)


class LatexExporter:

    @staticmethod
    def run(document, url_href, url_title):
        renderer = LatexRenderer()
        main_content = renderer.run(document.root)
        packages = renderer.packages

        templates_folder = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'templates'
        )
        env = Environment(loader=FileSystemLoader(templates_folder))
        template = env.get_template('latex_render.tex')
        return template.render(
            lang=document.manifest['lang'],
            title=document.manifest['title'],
            subtitle=document.manifest['subtitle'],
            authors=', '.join(document.manifest['authors']),
            packages=packages,
            contents=document.root.find('h1') is not None,
            main_content=main_content,
            url_href=url_href,
            url_title=url_title,
        )
