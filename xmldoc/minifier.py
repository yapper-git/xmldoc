import re


class Minifier:

    INLINE_ELEMENTS = ["h1", "h2", "h3", "h4", "p", "li", "td", "th", "b",
                       "i", "sup", "sub", "mark"]

    NO_TEXT_ELEMENTS = ["extract", "blockquote", "ul", "ol", "table", "tr"]

    REGEX = re.compile(r"\s+")

    @classmethod
    def run(cls, root):
        cls.remove_text_between_blocks(root)
        cls.strip_all(root)
        cls.merge_whitespace(root)

    @classmethod
    def remove_text_between_blocks(cls, root):
        for tag_name in cls.NO_TEXT_ELEMENTS:
            for element in root.iter(tag_name):
                element.text = None
                for subelement in element:
                    subelement.tail = None

    @classmethod
    def strip_all(cls, root):
        for tag_name in cls.INLINE_ELEMENTS:
            for element in root.iter(tag_name):
                if element.text:
                    element.text = element.text.lstrip()
                last_child = element.find('*[last()]')
                if last_child and last_child.tail:
                    last_child.tail = last_child.tail.rstrip()
                if last_child is None and element.text:
                    element.text = element.text.rstrip()

    @classmethod
    def merge_whitespace(cls, root):
        for tag_name in cls.INLINE_ELEMENTS:
            for element in root.iter(tag_name):
                if element.text:
                    element.text = cls.REGEX.sub(" ", element.text)
                for subelement in element:
                    if subelement.tail:
                        subelement.tail = cls.REGEX.sub(" ", subelement.tail)
