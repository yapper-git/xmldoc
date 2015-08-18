import json
import os
import pygit2
import xml.etree.ElementTree as ET


class Document:

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.manifest = json.loads(self.get_file_content('manifest.json'))
        self.root = ET.fromstring(self.get_file_content('text.xml'))

    def get_file_content(self, filename):
        with open(os.path.join(self.repo_path, filename), 'r') as infile:
            return infile.read()
