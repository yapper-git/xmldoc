#!/usr/bin/env python3

import argparse
from jinja2 import Template
import xml.etree.ElementTree as ET

import docparser
import latex_renderer

parser = argparse.ArgumentParser(description="Converts XML extract to LaTeX.")
parser.add_argument("input", help="path to input file")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

root = ET.parse(args.input).getroot()

renderer = latex_renderer.LaTeXRenderer()
parser = docparser.DocParser(root, renderer)

main_content = parser.run()

tmpl = Template(r"""\documentclass[11pt]{article}

%%% Required packages %%%
\usepackage[T1]{fontenc}
\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm,headheight=110pt]{geometry}
\usepackage{tocloft}
\usepackage{fancyhdr}
{% for pkg_name in packages %}
\usepackage{{ '{' }}{{ pkg_name }}{{ '}' }}
{% endfor %}
\usepackage[hidelinks]{hyperref} % load last

%%% Table of contents %%%
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
\setcounter{secnumdepth}{0}

%%% Page headers and footers %%%
\pagestyle{fancy}
\renewcommand{\headrulewidth}{1pt}
\fancyhead[L]{Document Title}
\fancyhead[C]{}
\fancyhead[R]{Author Name}
\renewcommand{\footrulewidth}{1pt}
\fancyfoot[L]{{ '{' }}{\small\copyright} \href{http://www.example.com}{www.example.com}{{ '}' }}
\fancyfoot[C]{}
\fancyfoot[R]{\thepage}

%%% Paragraph %%%
\setlength{\parindent}{0cm}
\setlength{\parskip}{0.6em}

%%% Tables %%%
\renewcommand{\arraystretch}{1.4}

%%% Document properties %%%
\title{
    \textbf{\Huge Document Title}
    \\
    Subtitle
}
\author{Author Name}
\date{}

\begin{document}

\maketitle
\newpage
\tableofcontents
{{ main_content }}

\end{document}""")

tmpl_render = tmpl.render(
    title='Document Title',
    subtitle='Subtitle of the document',
    author_name='Author Name',
    packages=renderer.packages,
    main_content=main_content,
)


with open(args.output, "w") as output_file:
    output_file.write(tmpl_render)
