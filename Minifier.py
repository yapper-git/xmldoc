import re

class Minifier:

    def __init__(self, tree):
        self._tree = tree
        self._root = tree.getroot()
        self._regex = re.compile(r"\s+")

    def run(self):
        tagList = ["blockquote", "ul", "ol", "table", "tr"]
        for element in self._root.findall("."):
            self.removeText(element)
        for tag in tagList:
            for element in self._root.findall(".//" + tag):
                self.removeText(element)

        tagList = ["h1", "h2", "h3", "h4", "p", "li", "td", "th"]
        for tag in tagList:
            for element in self._root.findall(".//" + tag):
                self.strip(element)
                self.mergeWhiteSpaces(element)

        return self._tree

    def strip(self, element):
        element.text = element.text.lstrip()
        children = list(element)
        if len(children) == 0:
            element.text = element.text.rstrip()
        elif children[len(children)-1].tail:
            children[len(children)-1].tail = children[len(children)-1].tail.rstrip()

    def mergeWhiteSpaces(self, element):
        element.text = self._regex.sub(" ", element.text)
        for subelement in element:
            if subelement.tail:
                subelement.tail = self._regex.sub(" ", subelement.tail)

    def removeText(self, element):
        element.text = None
        for subelement in element:
            subelement.tail = None

