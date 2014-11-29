import epub2

epub = epub2.Epub("sample.epub")
epub.open()

epub.identifier = "sample"
epub.title = "Sample ePUB file"
epub.language = "en-GB"

epub.metadata.addTitle("Title N°2")
epub.metadata.addTitle("Title N°3")
epub.metadata.addCreator("Creator N°1")
epub.metadata.addCreator("Creator N°2", role="aut")
epub.metadata.addCreator("Creator N°3", fileAs="Creator 3", role="oth")
epub.metadata.addSubject("Subject N°1")
epub.metadata.addSubject("Subject N°2")
epub.metadata.setDescription("Description")
epub.metadata.addContributor("Contributor N°1")
epub.metadata.addContributor("Contributor N°2", role="aut")
epub.metadata.addContributor("Contributor N°3", fileAs="Contributor 3", role="oth")
epub.metadata.addDate("2014")
epub.metadata.addDate("2014-12", event="modification")
epub.metadata.addDate("2014-12-25", event="publication")
epub.metadata.setType("type")
epub.metadata.setFormat("format")
epub.metadata.addIdentifier("uuid002")
epub.metadata.addIdentifier("uuid003", "myid", "scheme")
epub.metadata.setSource("source")
epub.metadata.addLanguage("en-US")
epub.metadata.addLanguage("fr-fr")
epub.metadata.addLanguage("de")
epub.metadata.setRelation("relation")
epub.metadata.setCoverage("coverage")
epub.metadata.setRights("rights")
epub.metadata.addMeta("name1", "content1")
epub.metadata.addMeta("name2", "content2")

epub.guide.addReference(type="title-page", title="Title page", href="titlepage.xhtml")
epub.guide.addReference(type="toc", title="Table of Contents", href="contents.xhtml")

epub.contents.addNavPoint(epub2.NavPoint("chap1", "Chapter 1", "chapter1.xhtml"))
epub.contents.addNavPoint(epub2.NavPoint("chap2", "Chapter 2", "chapter2.xhtml"))

epub.addTextFromString(id="titlepage", localname="titlepage.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <title>Sample ePUB file</title>
  </head>
  <body>
    <h1>Sample ePUB file</h1>
  </body>
</html>""")

epub.addTextFromString(id="contents", localname="contents.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <title>Tables of Contents</title>
    <link rel="stylesheet" href="main.css" type="text/css" />
  </head>
  <body>
    <h1>Table of Contents</h1>
    <ol>
      <li><a href="chapter1.xhtml">Chapter 1</a></li>
      <li><a href="chapter2.xhtml">Chapter 2</a></li>
    </ol>
  </body>
</html>""")

epub.addTextFromString(id="chap1", localname="chapter1.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <title>Chapiter 1</title>
    <link rel="stylesheet" href="main.css" type="text/css" />
  </head>
  <body>
    <h1>Chapter 1</h1>
    <p>Et eodem impetu Domitianum praecipitem per scalas itidem funibus constrinxerunt, eosque coniunctos per ampla spatia civitatis acri raptavere discursu. iamque artuum et membrorum divulsa conpage superscandentes corpora mortuorum ad ultimam truncata deformitatem velut exsaturati mox abiecerunt in flumen.</p>
    <p>Ideoque fertur neminem aliquando ob haec vel similia poenae addictum oblato de more elogio revocari iussisse, quod inexorabiles quoque principes factitarunt. et exitiale hoc vitium, quod in aliis non numquam intepescit, in illo aetatis progressu effervescebat, obstinatum eius propositum accendente adulatorum cohorte.</p>
    <p>Eo adducta re per Isauriam, rege Persarum bellis finitimis inligato repellenteque a conlimitiis suis ferocissimas gentes, quae mente quadam versabili hostiliter eum saepe incessunt et in nos arma moventem aliquotiens iuvant, Nohodares quidam nomine e numero optimatum, incursare Mesopotamiam quotiens copia dederit ordinatus, explorabat nostra sollicite, si repperisset usquam locum vi subita perrupturus.</p>
  </body>
</html>""")

epub.addTextFromString(id="chap2", localname="chapter2.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <title>Chapter 2</title>
    <link rel="stylesheet" href="main.css" type="text/css" />
  </head>
  <body>
    <h1>Chapter 2</h1>
    <p>Quam ob rem cave Catoni anteponas ne istum quidem ipsum, quem Apollo, ut ais, sapientissimum iudicavit; huius enim facta, illius dicta laudantur. De me autem, ut iam cum utroque vestrum loquar, sic habetote.</p>
    <p>Quanta autem vis amicitiae sit, ex hoc intellegi maxime potest, quod ex infinita societate generis humani, quam conciliavit ipsa natura, ita contracta res est et adducta in angustum ut omnis caritas aut inter duos aut inter paucos iungeretur.</p>
  </body>
</html>""")

epub.addStyleFromString("main.css", """h1 {
    border-bottom: 1px solid black;
}""", "style")

epub.addFileFromFile("tux.png", "face.png", "tux", "image/png")

epub.close()
