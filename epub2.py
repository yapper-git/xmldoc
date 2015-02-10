import zipfile


class Metadata:
    """Metadata represents the metadata element in .opf file"""

    def __init__(self):
        self._titles = []
        self._creators = []
        self._subjects = []
        self._description = None
        self._publisher = None
        self._contributors = []
        self._dates = []
        self._type = None
        self._format = None
        self._identifiers = []
        self._source = None
        self._languages = []
        self._relation = None
        self._coverage = None
        self._rights = None
        self._metas = []

    def add_title(self, title):
        self._titles.append(title)

    def add_creator(self, name, role=None, file_as=None):
        self._creators.append({
            "name": name,
            "role": role,
            "fileAs": file_as
        })

    def add_subject(self, subject):
        self._subjects.append(subject)

    def set_description(self, description):
        self._description = description

    def set_publisher(self, publisher):
        self._publisher = publisher

    def add_contributor(self, name, role=None, file_as=None):
        self._contributors.append({
            "name": name,
            "role": role,
            "fileAs": file_as
        })

    def add_date(self, date, event=None):
        self._dates.append({"date": date, "event": event})

    def set_type(self, type):
        self._type = type

    def set_format(self, format):
        self._format = format

    def add_identifier(self, content, id=None, scheme=None):
        self._identifiers.append({
            "content": content,
            "id": id,
            "scheme": scheme
        })

    def set_source(self, source):
        self._source = source

    def add_language(self, language):
        self._languages.append(language)

    def set_relation(self, relation):
        self._relation = relation

    def set_coverage(self, coverage):
        self._coverage = coverage

    def set_rights(self, rights):
        self._rights = rights

    def add_meta(self, name, content):
        self._metas.append({"name": name, "content": content})


class Manifest:
    """Manifest represents the manifest element in .opf file"""

    def __init__(self):
        self._items = []

    def __iter__(self):
        return iter(self._items)

    def add_item(self, id, href, media_type):
        self._items.append({
            "id": id,
            "href": href,
            "mediaType": media_type
        })


class Spine:
    """Spine represents the spine element in .opf file"""

    def __init__(self):
        self._itemrefs = []

    def __iter__(self):
        return iter(self._itemrefs)

    def add_itemref(self, idref, linear=True):
        self._itemrefs.append({"idref": idref, "linear": linear})


class Guide:
    """Guide represents the guide element in .opf file"""

    def __init__(self):
        self._references = []

    def __iter__(self):
        return iter(self._references)

    def add_reference(self, type, title, href):
        self._references.append({
            "type": type,
            "title": title,
            "href": href
        })


class Contents:

    def __init__(self):
        self._navpoints = []

    def add_navpoint(self, navpoint):
        self._navpoints.append(navpoint)


class NavPoint:
    """NavPoint represents a NavPoint element for contents"""

    # _playOrder = 0

    def __init__(self, id, label, source, navpoints=[]):
        self._id = id
        self._label = label
        self._source = source
        self._navpoints = navpoints
        # self._playOrder = NavPoint.

    def append(self, navpoint):
        self._navpoints.append(navpoint)


class Epub:

    encoding = "UTF-8"
    tab = "\t"
    end = "\n"

    def __init__(self, file_path):
        self.identifier = None
        self.title = None
        self.language = None
        self.metadata = Metadata()
        self.manifest = Manifest()
        self.spine = Spine()
        self.guide = Guide()
        self.contents = Contents()

        self._file_path = file_path
        self.manifest.add_item("ncx", "toc.ncx", "application/x-dtbncx+xml")

    def open(self):
        self._zip = zipfile.ZipFile(self._file_path, "w")
        self._write_mimetype_file()
        self._write_container_file()

    def close(self):
        if not self.identifier:
            raise ValueError("identifier required")
        if not self.title:
            raise ValueError("title required")
        if not self.title:
            raise ValueError("language required")
        if len(self.contents._navpoints) == 0:
            raise ValueError("navpoint required")
        self._write_opf_file()
        self._write_ncx_file()
        self._zip.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def add_file_from_file(self, localname, filename, id, media_type):
        self._zip.write(filename, "OEBPS/" + localname)
        self.manifest.add_item(id, localname, media_type)

    def add_file_from_string(self, localname, content, id, media_type):
        self._zip.writestr("OEBPS/" + localname, content)
        self.manifest.add_item(id, localname, media_type)

    def add_text_from_file(self, localname, filename, id):
        self.add_file_from_file(localname, filename, id, "application/xhtml+xml")
        self.spine.add_itemref(id)

    def add_text_from_string(self, localname, content, id):
        self.add_file_from_string(localname, content, id, "application/xhtml+xml")
        self.spine.add_itemref(id)

    def add_style_from_file(self, localname, filename, id):
        self.add_file_from_file(localname, filename, id, "text/css")

    def add_style_from_string(self, localname, content, id):
        self.add_file_from_string(localname, content, id, "text/css")

    def _write_mimetype_file(self):
        self._zip.writestr("mimetype", "application/epub+zip")

    def _write_container_file(self):
        self._zip.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0" encoding="{encoding}"?>{end}'
            '<container version="1.0" xmlns="{xmlns}">{end}'
            '{tab}<rootfiles>{end}'
            '{tab}{tab}<rootfile full-path="OEBPS/content.opf"'
            ' media-type="application/oebps-package+xml"/>{end}'
            '{tab}</rootfiles>{end}'
            '</container>'.format(
                xmlns="urn:oasis:names:tc:opendocument:xmlns:container",
                encoding=Epub.encoding, tab=Epub.tab, end=Epub.end))

    def _write_opf_file(self):
        self._zip.writestr(
            "OEBPS/content.opf",
            '<?xml version="1.0" encoding="{encoding}"?>{end}'
            '<package xmlns="{xmlns_opf}" version="2.0" unique-identifier="BookId">{end}'
            '{tab}<metadata xmlns:dc="{xmlns_dc}" xmlns:opf="{xmlns_opf}">{end}'
            '{tab}{tab}{metadata}{end}'
            '{tab}</metadata>{end}'
            '{tab}<manifest>{end}'
            '{tab}{tab}{manifest}{end}'
            '{tab}</manifest>{end}'
            '{tab}<spine toc="ncx">{end}'
            '{tab}{tab}{spine}{end}'
            '{tab}</spine>{end}'
            '</package>'.format(
                xmlns_opf="http://www.idpf.org/2007/opf",
                xmlns_dc="http://purl.org/dc/elements/1.1/",
                encoding=Epub.encoding,
                tab=Epub.tab,
                end=Epub.end,
                metadata="\n\t\t".join(self._metadata_tags()),
                manifest="\n\t\t".join(self._manifest_tags()),
                spine="\n\t\t".join(self._spine_tags())))

    def _write_ncx_file(self):
        self._zip.writestr(
            "OEBPS/toc.ncx",
            '<?xml version="1.0" encoding="{encoding}"?>{end}'
            '<!DOCTYPE ncx PUBLIC "{dtd_name}" "{dtd_location}">{end}'
            '<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">{end}'
            '{tab}<head>{end}'
            '{tab}{tab}<meta name="dtb:uid" content="{identifier}"/>{end}'
            '{tab}{tab}<meta name="dtb:depth" content="{depth}"/>{end}'
            '{tab}{tab}<meta name="dtb:totalPageCount" content="0"/>{end}'
            '{tab}<meta name="dtb:maxPageNumber" content="0"/>{end}'
            '{tab}</head>{end}'
            '{tab}<docTitle><text>SIC</text></docTitle>'
            '<navMap>{end}'
            '{tab}{tab}{navmap}{end}'
            '{tab}</navMap>{end}'
            '</ncx>'.format(
                dtd_name="-//NISO//DTD ncx 2005-1//EN",
                dtd_location="http://www.daisy.org/z3986/2005/ncx-2005-1.dtd",
                encoding=Epub.encoding,
                tab=Epub.tab,
                end=Epub.end,
                identifier=self.identifier,
                depth=self.depth(),
                navmap=self.render_navmap()))

    def _manifest_tags(self):
        tags = []
        for item in self.manifest:
            tags.append('<item id="{}" href="{}" media-type="{}"/>'
                        .format(item["id"], item["href"], item["mediaType"]))
        return tags

    def _spine_tags(self):
        tags = []
        for itemref in self.spine:  # FIXME ugly
            tag = '<itemref idref="{}"'.format(itemref["idref"])
            if not itemref["linear"]:
                tag += ' linear="no"'
            tag += '/>'
            tags.append(tag)
        return tags

    def _guide_tags(self):
        tags = []
        for type, title, href in self.guide:
            tags.append('<reference type="{}" title="{}" href="{}"/>'
                        .format(type, title, href))
        return tags

    def _metadata_tags(self):
        metadata = self.metadata
        tags = []

        # titles
        tags.append('<dc:title>{}</dc:title>'.format(self.title))
        for title in metadata._titles:
            tags.append('<dc:title>{}</dc:title>'.format(title))

        # creators
        for creator in metadata._creators:
            tag = '<dc:creator'
            if creator["role"]:
                tag += ' opf:role="{}"'.format(creator["role"])
            if creator["fileAs"]:
                tag += ' opf:file-as="{}"'.format(creator["fileAs"])
            tag += '>{}</dc:creator>'.format(creator["name"])
            tags.append(tag)

        # subjects
        for subject in metadata._subjects:
            tags.append('<dc:subject>{}</dc:subject>'.format(subject))

        # description
        if metadata._description:
            tags.append('<dc:description>{}</dc:description>'.format(metadata._description))

        # publisher
        if metadata._publisher:
            tags.append('<dc:publisher>{}</dc:publisher>'.format(metadata._publisher))

        # contributors
        for contributor in metadata._contributors:
            tag = '<dc:contributor'
            if contributor["role"]:
                tag += ' opf:role="{}"'.format(contributor["role"])
            if contributor["fileAs"]:
                tag += ' opf:file-as="{}"'.format(contributor["fileAs"])
            tag += '>{}</dc:contributor>'.format(contributor["name"])
            tags.append(tag)

        # dates
        for date in metadata._dates:
            tag = '<dc:date'
            if date["event"]:
                tag += ' opf:event="{}"'.format(date["event"])
            tag += '>{}</dc:date>'.format(date["date"])
            tags.append(tag)

        # type
        if metadata._type:
            tags.append('<dc:type>{}</dc:type>'.format(metadata._type))

        # format
        if metadata._format:
            tags.append('<dc:format>{}</dc:format>'.format(metadata._format))

        # identifiers
        tags.append('<dc:identifier id="BookId">{}</dc:identifier>'.format(self.identifier))
        for identifier in metadata._identifiers:
            tag = '<dc:identifier'
            if identifier["id"]:
                tag += ' id="{}"'.format(identifier["id"])
            if identifier["scheme"]:
                tag += ' opf:scheme="{}"'.format(identifier["scheme"])
            tag += '>{}</dc:identifier>'.format(identifier["content"])
            tags.append(tag)

        # source
        if metadata._source:
            tags.append('<dc:source>{}</dc:source>'.format(metadata._source))

        # languages
        tags.append('<dc:language>{}</dc:language>'.format(self.language))
        for language in metadata._languages:
            tags.append('<dc:language>{}</dc:language>'.format(language))

        # relation
        if metadata._relation:
            tags.append('<dc:relation>{}</dc:relation>'.format(metadata._relation))

        # coverage
        if metadata._coverage:
            tags.append('<dc:coverage>{}</dc:coverage>'.format(metadata._coverage))

        # rights
        if metadata._rights:
            tags.append('<dc:rights>{}</dc:rights>'.format(metadata._rights))

        # metas
        for name, content in metadata._metas:
            tags.append('<meta name="{}" content="{}"/>'.format(name, content))

        return tags

    def render_navmap(self):
        buf = ""
        for navpoint in self.contents._navpoints:
            buf += self.render_navpoint(navpoint, 2)
        return buf

    def render_navpoint(self, navpoint, level):
        # FIXME ugly
        # TODO implement playOrder

        tab = Epub.tab
        end = Epub.end

        buffer = ""

        # <navPoint id="..." playOrder="...">
        buffer += (tab * level) + '<navPoint id="{}">'.format(navpoint._id) + end

        # <navLabel><text>...</text></navLabel>
        buffer += (tab * (level+1)) + '<navLabel>' + end
        buffer += (tab * (level+2)) + '<text>' + navpoint._label + '</text>' + end
        buffer += (tab * (level+1)) + '</navLabel>' + end

        # <content src="..."/>
        buffer += (tab * (level+1)) + '<content src="' + navpoint._source + '"/>' + end

        # <navPoint>...</navPoint> if children
        for child_navpoint in navpoint._navpoints:
            buffer += self.render_navpoint(child_navpoint, level+1)

        # </navPoint>
        buffer += (tab * level) + '</navPoint>' + end

        return buffer

    def depth(self):
        max_depth = 0
        for navpoint in self.contents._navpoints:
            depth = self.depth_rec(navpoint, 1)
            if depth > max_depth:
                max_depth = depth
        return max_depth

    def depth_rec(self, navpoint, current_depth):
        navpoints = navpoint._navpoints

        if len(navpoints) == 0:
            return current_depth
        else:
            max_depth = current_depth
            for child_navpoint in navpoints:
                depth = self.depth_rec(child_navpoint, current_depth+1)
                if depth > max_depth:
                    max_depth = depth
            return max_depth
