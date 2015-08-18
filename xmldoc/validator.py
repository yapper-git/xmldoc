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

        elements = ['b', 'i', 'sup', 'sub', 'mark']
        for element in elements:
            assert len(xml_tree.xpath('.//{0}//{0}'.format(element))) == 0
