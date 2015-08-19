import json
from lxml import etree
import os


class Validator:

    XML_SCHEMA = "extract.xsd"

    def __init__(self, path):
        self.path = path

    def run(self):
        self.manifest_validation()
        self.text_validation()

    def manifest_validation(self):
        manifest_path = os.path.join(self.path, 'manifest.json')
        manifest_dict = json.load(open(manifest_path, 'r'))
        for key, value in manifest_dict.items():
            assert key in ['lang', 'title', 'subtitle', 'authors']

    def text_validation(self):
        xsd_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.XML_SCHEMA)
        text_path = os.path.join(self.path, 'text.xml')
        xsd_tree = etree.parse(xsd_path)

        xml_tree = etree.parse(text_path)
        xmlschema = etree.XMLSchema(xsd_tree)
        xmlschema.assertValid(xml_tree)

        # for instance <b> in <b> is invalid
        elements = ['b', 'i', 'sup', 'sub', 'mark']
        for element in elements:
            if len(xml_tree.xpath('.//{0}//{0}'.format(element))) != 0:
                raise SyntaxError("<{}> nesting not allowed".format(element))

        # level headers must start at level 1 and increase by 1 max
        previous_level = 0
        headers = xml_tree.xpath('.//h1|.//h2|.//h3|.//h4')
        for header in headers:
            level = int(header.tag[1])
            if level > previous_level and level != previous_level + 1:
                raise SyntaxError("Headers must start at level 1 and increase by 1 max")
            previous_level = level
