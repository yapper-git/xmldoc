import re

class Minifier:

    INLINE_ELEMENTS = ["h1", "h2", "h3", "h4", "p", "li", "td", "th", "b",
                       "i", "sup", "sub", "mark"]

    @classmethod
    def run(cls, root):
        cls.remove_text_between_blocks(root)
        cls.strip_all(root)
        cls.merge_whitespace(root)

    @classmethod
    def remove_text_between_blocks(cls, root):
        for element in root.findall("."):
            cls.remove_text_element(element)
        for tag in ["blockquote", "ul", "ol", "table", "tr"]:
            for element in root.findall(".//" + tag):
                cls.remove_text_element(element)

    @staticmethod
    def remove_text_element(element):
        assert element.text.strip() == ""
        element.text = None
        for subelement in element:
            assert subelement.tail.strip() == ""
            subelement.tail = None

    @classmethod
    def strip_all(cls, root):
        for tag in cls.INLINE_ELEMENTS:
            for element in root.findall(".//" + tag):
                cls.strip_element(element)

    @staticmethod
    def strip_element(element):
        element.text = element.text.lstrip()
        children = list(element)
        if len(children) == 0:
            element.text = element.text.rstrip()
        elif children[len(children)-1].tail:
            children[len(children)-1].tail = children[len(children)-1].tail.rstrip()

    @classmethod
    def merge_whitespace(cls, root):
        for tag in cls.INLINE_ELEMENTS:
            for element in root.findall(".//" + tag):
                cls.merge_whitespace_in_element(element)

    @staticmethod
    def merge_whitespace_in_element(element):
        regex = re.compile(r"\s+")
        element.text = regex.sub(" ", element.text)
        for subelement in element:
            if subelement.tail:
                subelement.tail = regex.sub(" ", subelement.tail)

