class LaTeXRenderer:

    def __init__(self):
        self.packages = []

    def usepackage(self, pkg_name):
        if pkg_name not in self.packages:
            self.packages.append(pkg_name)

    def text(self, text):
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
        # can add \textless{} for < and \textgreater{} for >
        for old, new in replacements:
            text = text.replace(old, new)
        return text

    def header(self, text, level):
        if level == 1:
            return '\n\n\\section{%s}' % text
        if level == 2:
            return '\n\n\\subsection{%s}' % text
        if level == 3:
            return '\n\n\\subsubsection{%s}' % text
        if level == 4:
            return '\n\n\\textbf{\\small %s}' % text
        raise NotImplementedError

    def paragraph(self, text, align):
        if align == 'left':
            return '\n\n%s' % text
        if align == 'right':
            return '\n\n\\begin{flushright}\n%s\n\\end{flushright}' % text
        if align == 'center':
            return '\n\n\\begin{center}\n%s\n\\end{center}' % text
        raise NotImplementedError

    def blockquote(self, text):
        return '\n\n\\begin{quotation}\n%s\n\\end{quotation}' % text.strip()

    def ordered_list(self, text, listType):
        if listType == "decimal":
            label = ""
        else:
            self.usepackage("enumitem")
            if listType == "lower-alpha":
                label = r"[label=\alph*.]"
            elif listType == "upper-alpha":
                label = r"[label=\Alph*.]"
            elif listType == "lower-roman":
                label = r"[label=\roman*.]"
            elif listType == "upper-roman":
                label = r"[label=\Roman*.]"
            else:
                raise NotImplementedError
        return '\n\n\\begin{enumerate}' + label + text + '\n\\end{enumerate}'

    def unordered_list(self, text):
        return '\n\n\\begin{itemize}%s\n\\end{itemize}' % text

    def list_item(self, text):
        return '\n\\item\n    %s' % text

    def table(self, text, num_cols):
        param = '{' + ('|l' * num_cols) + '|}'
        return "\n\n\\begin{center}\n\\begin{tabular}" + param + "%s\n\hline\n\\end{tabular}\\end{center}" % text

    def table_row(self, text):
        return "\n\\hline\n   %s \\\\" % text[3:]

    def table_cell(self, text, align, colspan, rowspan):
        return " & %s" % text

    def table_cell_header(self, text, align, colspan, rowspan):
        return " & %s" % text

    def linebreak(self):
        return r'\\'  # or \newline

    def bold(self, text):
        return r'\textbf{%s}' % text

    def italic(self, text):
        return r'\textit{%s}' % text

    def superscript(self, text):
        return r'\textsuperscript{%s}' % text

    def subscript(self, text):
        self.usepackage("fixltx2e")
        return r'\textsubscript{%s}' % text

    def highlight(self, text):
        self.usepackage("color,soul")
        return r'\hl{%s}' % text
