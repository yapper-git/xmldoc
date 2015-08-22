import json
from lxml import etree
import os


class Validator:

    REQUIRED_FIELDS = ['lang', 'title', 'subtitle', 'authors']
    XML_SCHEMA = "extract.xsd"

    @classmethod
    def document_validation(cls, path):
        manifest_path = os.path.join(path, 'manifest.json')
        text_path = os.path.join(path, 'text.xml')

        cls.manifest_validation(open(manifest_path, 'r').read())
        cls.text_validation(open(text_path, 'r').read())

    @classmethod
    def manifest_validation(cls, content):
        manifest_dict = json.loads(content)
        for key, value in manifest_dict.items():
            if key not in cls.REQUIRED_FIELDS:
                raise SyntaxError("{} required".format(key))

    @classmethod
    def text_validation(cls, content):
        xsd_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), cls.XML_SCHEMA)
        xsd_tree = etree.parse(xsd_path)

        xml_tree = etree.fromstring(content.encode())
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
