import json
import os
import pygit2
import xml.etree.ElementTree as ET

from xmldoc.export_epub import EpubExporter
from xmldoc.export_html import HtmlExporter
from xmldoc.export_latex import LatexExporter


# revparse_single raises:
# - KeyError if invalid SHA
# - ValueError if OID prefix is too short for instance.


class VersionedDocument:

    @staticmethod
    def init_repo(repo_path, bare=False):
        pygit2.init_repository(repo_path)

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = pygit2.Repository(repo_path)

    def snapshot(self, version):
        return DocumentSnapshot(self.repo, self.get_commit(version))

    def get_commit(self, version):
        try:
            return self.repo.revparse_single(version)
        except (KeyError, ValueError):
            raise KeyError("Invalid version '{}'".format(version))

    def set_file_content(self, filename, content):
        with open(os.path.join(self.repo_path, filename), 'w') as myfile:
            myfile.write(content)

    def get_file_content(self, filename):
        with open(os.path.join(self.repo_path, filename), 'r') as myfile:
            return myfile.read()

    def set_manifest(self, manifest):
        self.set_file_content(
            'manifest.json',
            json.dumps(manifest, indent=4, sort_keys=True, ensure_ascii=False)
        )

    def get_manifest(self):
        return json.loads(self.get_file_content('manifest.json'))

    def set_text(self, content):
        return self.set_file_content('text.xml', content)

    def get_text(self):
        return self.get_file_content('text.xml')

    def git_log(self):  # FIXME if empty?
        last = self.repo[self.repo.head.target]
        return self.repo.walk(last.id, pygit2.GIT_SORT_TOPOLOGICAL)

    def git_diff(self, commit1, commit2):
        return self.repo.diff(commit1, commit2)

    def commit(self, user_name, user_email, message):
        index = self.repo.index
        index.add_all()  # FIXME remove?
        index.write()
        treeid = index.write_tree()
        return self.repo.create_commit(
            'refs/heads/master',  # reference_name
            pygit2.Signature(user_name, user_email),  # author
            pygit2.Signature(user_name, user_email),  # commiter
            message,
            treeid,
            [] if self.repo.head_is_unborn else [self.repo.head.target]
        )


class DocumentMixin:

    def export_epub(self, filename):
        EpubExporter().run(self, filename)

    def export_html(self):
        return HtmlExporter().run(self)

    def export_latex(self, url_href='http://www.example.com', url_title='www.example.com'):
        return LatexExporter().run(self, url_href, url_title)


class DocumentSnapshot(DocumentMixin):

    def __init__(self, repo, commit):
        self.repo = repo
        self.commit = commit
        self.tree = self.commit.tree
        self._load_manifest()
        self._load_text()

    def get_file_content(self, filename):
        entry = self.tree[filename]
        blob = self.repo[entry.id]
        return blob.data.decode()

    def _load_manifest(self):
        self.manifest = json.loads(self.get_file_content('manifest.json'))

    def _load_text(self):
        self.text = self.get_file_content('text.xml')
        self.root = ET.fromstring(self.text)


class DocumentDir(DocumentMixin):

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.manifest = json.loads(self.get_file_content('manifest.json'))
        self.root = ET.fromstring(self.get_file_content('text.xml'))

    def get_file_content(self, filename):
        with open(os.path.join(self.repo_path, filename), 'r') as infile:
            return infile.read()
