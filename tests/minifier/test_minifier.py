import unittest
import xml.etree.ElementTree as ET

import minifier


class MinifierTest(unittest.TestCase):

    """Test case to test methods of the module 'Minifier'."""

    def _assertFileEqual(self, input_file, method_name, output_file):
        with open(output_file, "rb") as ostream:
            input_root = ET.parse(input_file).getroot()
            getattr(minifier.Minifier, method_name)(input_root)
            content = ET.tostring(input_root)
            output_content = ostream.read()
            print("-" * 40)
            self.assertEqual(content, output_content)

    def test_remove_text_between_blocks(self):
        self._assertFileEqual(
            "test_remove_text_between_blocks.xml",
            "remove_text_between_blocks",
            "test_remove_text_between_blocks.min.xml")
