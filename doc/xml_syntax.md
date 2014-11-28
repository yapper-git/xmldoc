# XML Syntax

## Blocks

### Header: `h1`, `h2`, `h3`, `h4`

Headers must only contain text (no inline formatting).

### Paragraph: `p`

By default, the text is left align.
To *center*, set `align` attribute  to `center`.
To *align right*, set `align` attribute to `right`.

### Blockquote: `blockquote`

`blockquote` element must contains at least one paragraph.

### List: `ul`, `ol`

* `ul` : unordered list
* `ol[type]` : ordered list
    + `default` (1, 2, 3, 4 etc.)
    + `lower-alpha` (a, b, c, d etc.)
    + `upper-alpha` (A, B, C, D etc.)
    + `lower-roman` (i, ii, iii, iv etc.)
    + `upper-roman` (I, II, III, IV etc.)
* `li` : list item

No nesting support for now

### Table: `table`

Tables are block, center in the middle of the page (like `margin:auto` in CSS).

Table row: `tr`

Table cell (header): `td`, `th` (`align[center|right]`, `rowspan`, `colspan`)

## Inline

* `br` : line break (empty tag)
* `b` : bold
* `i` : italic
* `sup` : superscript
* `sub` : subscript
* `mark` : highlight
