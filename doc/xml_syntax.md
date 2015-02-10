# XML Syntax

## Blocks

### Header: `h1`, `h2`, `h3`, `h4`

Headers must only contain text (no inline formatting).

### Paragraph: `p`

By default, the text is left align.
To *center*, set `align` attribute to `center`.
To *align right*, set `align` attribute to `right`.

### Blockquote

`blockquote` element must contains at least one paragraph.

### List: `ul`, `ol`

* `ul`: unordered list
* `ol`: ordered list, optional attribute: `type` with value:
    + `default` (1, 2, 3, 4 etc.)
    + `lower-alpha` (a, b, c, d etc.)
    + `upper-alpha` (A, B, C, D etc.)
    + `lower-roman` (i, ii, iii, iv etc.)
    + `upper-roman` (I, II, III, IV etc.)
* `li`: list item

No nesting support for now

### Table

A table is a block, centered in the middle of the page.

* `table`: table
* `tr`: table row
* `td`: table cell (optional attributes: `align`, `rowspan`, `colspan`)
* `th`: table cell header (optional attributes: `align`, `rowspan`, `colspan`)

`align` attribute must be `center` or `right`.

`rowspan`, `colspan` must be an integer, greater than 1.

## Inline

* `br` : line break (empty tag)
* `b` : bold
* `i` : italic
* `sup` : superscript
* `sub` : subscript
* `mark` : highlight
