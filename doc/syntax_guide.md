Syntax guide
===========

A document is a folder which contains these two files:
- `manifest.json`: metadata
- `text.xml`: main content

# manifest.json

**manifest.json** must be a JSON valid file, with `lang`, `title`, `subtitle` and
`authors` keys.

# text.xml

## Headers

```xml
<h1>This is heading 1 (most important)</h1>
<h2>This is heading 2</h2>
<h3>This is heading 3</h3>
<h4>This is heading 4 (least important)</h4>
```

## Paragraphs

```xml
<p>This paragraph is left-aligned or justified.</p>
<p align="center">This paragraph is centered.</p>
<p align="right">This paragraph is right-aligned.</p>
```

## Blockquotes

```xml
<blockquote>
    <p>Here is a long quotation.</p>
</blockquote>
```

`blockquote` element must contains at least one paragraph.

## Lists

### Unordered

```xml
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>
        Item 3
        <ul>
            <li>Item 3a</li>
            <li>Item 3b</li>
        </ul>
    </li>
</ul>
```

### Ordered

```xml
<ol>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>
        Item 3
        <ol>
            <li>Item 3a</li>
            <li>Item 3b</li>
        </ol>
    </li>
</ol>
```

Optional attribute `type` with value:
- `decimal` (1, 2, 3, 4 etc.)
- `lower-alpha` (a, b, c, d etc.)
- `upper-alpha` (A, B, C, D etc.)
- `lower-roman` (i, ii, iii, iv etc.)
- `upper-roman` (I, II, III, IV etc.)

## Tables

A table is a block, centered in the middle of the page.

```xml
<table>
    <tr>
      <th>First Name</th>
      <th>Last Name</th>
    </tr>
    <tr>
      <td>Jill</td>
      <td>Smith</td>
    </tr>
    <tr>
      <td>John</td>
      <td>Doe</td>
    </tr>
</table>
```

## Inline

```xml
<i>This text will be italic</i><br/>
<b>This text will be bold</b><br/>
<mark>This text will be highlighed</mark><br/>
<i>You <b>can</b> combine <mark>them</mark></i>
```

- `br`: line break (empty tag)
- `b`: bold
- `i`: italic
- `sup`: superscript
- `sub`: subscript
- `mark`: highlight

These inline elements are allowed in headers, paragraphs, lists and table cells.
