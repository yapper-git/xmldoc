import zipfile

class Metadata:
    """Metadata represents the metadata element in .opf file"""
    
    def __init__(self):
        self._titles       = []
        self._creators     = []
        self._subjects     = []
        self._description  = None
        self._publisher    = None
        self._contributors = []
        self._dates        = []
        self._type         = None
        self._format       = None
        self._identifiers  = []
        self._source       = None
        self._languages    = []
        self._relation     = None
        self._coverage     = None
        self._rights       = None
        self._metas        = []
    
    def addTitle(self, title):
        self._titles.append(title)
    
    def addCreator(self, name, role=None, fileAs=None):
        self._creators.append({
            "name": name,
            "role": role,
            "fileAs": fileAs
        })
    
    def addSubject(self, subject):
        self._subjects.append(subject)
    
    def setDescription(self, description):
        self._description = description
    
    def setPublisher(self, publisher):
        self._publisher = publisher
    
    def addContributor(self, name, role=None, fileAs=None):
        self._contributors.append({
            "name": name,
            "role": role,
            "fileAs": fileAs
        })
    
    def addDate(self, date, event=None):
        self._dates.append({"date": date, "event": event})
    
    def setType(self, type):
        self._type = type
    
    def setFormat(self, format):
        self._format = format
    
    def addIdentifier(self, content, id=None, scheme=None):
        self._identifiers.append({
            "content": content,
            "id": id,
            "scheme": scheme
        })
    
    def setSource(self, source):
        self._source = source
    
    def addLanguage(self, language):
        self._languages.append(language)
    
    def setRelation(self, relation):
        self._relation = relation
    
    def setCoverage(self, coverage):
        self._coverage = coverage
    
    def setRights(self, rights):
        self._rights = rights
    
    def addMeta(self, name, content):
        self._metas.append({"name": name, "content": content})


class Manifest:
    """Manifest represents the manifest element in .opf file"""
    
    def __init__(self):
        self._items = []
    
    def __iter__(self):
        return iter(self._items)
    
    def addItem(self, id, href, mediaType):
        self._items.append({
            "id": id,
            "href": href,
            "mediaType": mediaType
        })


class Spine:
    """Spine represents the spine element in .opf file"""
    
    def __init__(self):
        self._itemrefs = []
    
    def __iter__(self):
        return iter(self._itemrefs)
    
    def addItemref(self, idref, linear=True):
        self._itemrefs.append({"idref": idref, "linear": linear})


class Guide:
    """Guide represents the guide element in .opf file"""
    
    def __init__(self):
        self._references = []
    
    def __iter__(self):
        return iter(self._references)
    
    def addReference(self, type, title, href):
        self._references.append({
            "type": type,
            "title": title,
            "href": href
        })


class Contents:
    
    def __init__(self):
        self._navPoints = []
    
    def addNavPoint(self, navPoint):
        self._navPoints.append(navPoint)


class NavPoint:
    """NavPoint represents a NavPoint element for contents"""
    
    #_playOrder = 0
    
    def __init__(self, id, label, source, navPoints=[]):
        self._id = id
        self._label = label
        self._source = source
        self._navPoints = navPoints
        #self._playOrder = NavPoint.
    
    def append(navPoint):
        self._navPoints.append(navPoint)


class Epub:
    
    encoding = "UTF-8"
    tab = "\t"
    end = "\n"
    
    def __init__(self, filePath):
        self.identifier = None
        self.title = None
        self.language = None
        self.metadata = Metadata()
        self.manifest = Manifest()
        self.spine = Spine()
        self.guide = Guide()
        self.contents = Contents()
        
        self._filePath = filePath
        self.manifest.addItem("ncx", "toc.ncx", "application/x-dtbncx+xml")

    def open(self):
        self._zip = zipfile.ZipFile(self._filePath, "w")
        self._writeMimetypeFile()
        self._writeContainerFile()

    def close(self):
        if not self.identifier:
            raise ValueError("identifier required")
        if not self.title:
            raise ValueError("title required")
        if not self.title:
            raise ValueError("language required")
        if len(self.contents._navPoints) == 0:
            raise ValueError("navPoint required")
        self._writeOpfFile()
        self._writeNcxFile()
        self._zip.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def addFileFromFile(self, localname, filename, id, mediaType):
        self._zip.write(filename, "OEBPS/" + localname)
        self.manifest.addItem(id, localname, mediaType)
    
    def addFileFromString(self, localname, content, id, mediaType):
        self._zip.writestr("OEBPS/" + localname, content)
        self.manifest.addItem(id, localname, mediaType)
    
    def addTextFromFile(self, localname, filename, id):
        self.addFileFromFile(localname, filename, id, "application/xhtml+xml")
        self.spine.addItemref(id)
    
    def addTextFromString(self, localname, content, id):
        self.addFileFromString(localname, content, id, "application/xhtml+xml")
        self.spine.addItemref(id)
    
    def addStyleFromFile(self, localname, filename, id):
        self.addFileFromFile(localname, filename, id, "text/css")
    
    def addStyleFromString(self, localname, content, id):
        self.addFileFromString(localname, content, id, "text/css")
    
    def _writeMimetypeFile(self):
        self._zip.writestr("mimetype", "application/epub+zip")
    
    def _writeContainerFile(self):
        self._zip.writestr("META-INF/container.xml",
            '<?xml version="1.0" encoding="{encoding}"?>{end}'
            '<container version="1.0" xmlns="{xmlns}">{end}'
            '{tab}<rootfiles>{end}'
            '{tab}{tab}<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>{end}'
            '{tab}</rootfiles>{end}'
            '</container>'.format(
                xmlns="urn:oasis:names:tc:opendocument:xmlns:container",
                encoding=Epub.encoding, tab=Epub.tab, end=Epub.end))
    
    def _writeOpfFile(self):
        self._zip.writestr("OEBPS/content.opf",
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
                metadata="\n\t\t".join(self._metadataTags()),
                manifest="\n\t\t".join(self._manifestTags()),
                spine="\n\t\t".join(self._spineTags())
            ))
    
    def _writeNcxFile(self):
        self._zip.writestr("OEBPS/toc.ncx",
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
                navmap=self.renderNavMap()
            ))
    
    def _manifestTags(self):
        tags = []
        for item in self.manifest:
            tags.append('<item id="{}" href="{}" media-type="{}"/>'
                        .format(item["id"], item["href"], item["mediaType"]))
        return tags
    
    def _spineTags(self):
        tags = []
        for itemref in self.spine:# FIXME ugly
            tag = '<itemref idref="{}"'.format(itemref["idref"])
            if not itemref["linear"]: tag += ' linear="no"'
            tag += '/>'
            tags.append(tag)
        return tags
    
    def _guideTags(self):
        tags = []
        for type, title, href in self.guide:
            tags.append('<reference type="{}" title="{}" href="{}"/>'
                        .format(type, title, href))
        return tags

    def _metadataTags(self):
        metadata = self.metadata
        tags = []

        # titles
        tags.append('<dc:title>{}</dc:title>'.format(self.title))
        for title in metadata._titles:
            tags.append('<dc:title>{}</dc:title>'.format(title))

        # creators
        for creator in metadata._creators:
            tag = '<dc:creator'
            if creator["role"]: tag += ' opf:role="{}"'.format(creator["role"])
            if creator["fileAs"]: tag += ' opf:file-as="{}"'.format(creator["fileAs"])
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
            if contributor["role"]: tag += ' opf:role="{}"'.format(contributor["role"])
            if contributor["fileAs"]: tag += ' opf:file-as="{}"'.format(contributor["fileAs"])
            tag += '>{}</dc:contributor>'.format(contributor["name"])
            tags.append(tag)

        # dates
        for date in metadata._dates:
            tag = '<dc:date'
            if date["event"]: tag += ' opf:event="{}"'.format(date["event"])
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
            if identifier["id"]: tag += ' id="{}"'.format(identifier["id"])
            if identifier["scheme"]: tag += ' opf:scheme="{}"'.format(identifier["scheme"])
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
    
    def renderNavMap(self):
        buf = ""
        for navPoint in self.contents._navPoints:
            buf += self.renderNavPoint(navPoint, 2)
        return buf
    
    def renderNavPoint(self, navPoint, level):
        # FIXME ugly
        # TODO implement playOrder
        
        tab = Epub.tab
        end = Epub.end
        
        buffer = ""
        
        # <navPoint id="..." playOrder="...">
        buffer += (tab * level) + '<navPoint id="{}">'.format(navPoint._id) + end
        
        # <navLabel><text>...</text></navLabel>
        buffer += (tab * (level+1)) + '<navLabel>' + end
        buffer += (tab * (level+2)) + '<text>' + navPoint._label + '</text>' + end
        buffer += (tab * (level+1)) + '</navLabel>' + end
        
        # <content src="..."/>
        buffer += (tab * (level+1)) + '<content src="' + navPoint._source + '"/>' + end
        
        # <navPoint>...</navPoint> if children
        for childNavPoint in navPoint._navPoints:
            buffer += self.renderNavPoint(childNavPoint, level+1)
        
        # </navPoint>
        buffer += (tab * level) + '</navPoint>' + end
        
        return buffer


    def depth(self):
        maxDepth = 0;
        for navPoint in self.contents._navPoints:
            depth = self.depthRec(navPoint, 1)
            if depth > maxDepth:
                maxDepth = depth
        return maxDepth;
    
    def depthRec(self, navPoint, currentDepth):
        navPoints = navPoint._navPoints
        
        if len(navPoints) == 0:
            return currentDepth
        else:
            max = currentDepth;
            for childNavPoint in navPoints:
                depth = self.depthRec(childNavPoint, currentDepth+1)
                if depth > max:
                    max = depth;
            return max;
