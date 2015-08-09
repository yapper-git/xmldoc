import epub2

epub = epub2.Epub("sample.epub")
epub.open()

epub.identifier = "sample"
epub.title = "Sample ePUB file"
epub.language = "en-GB"

epub.metadata.add_title("Title N°2")
epub.metadata.add_title("Title N°3")
epub.metadata.add_creator("Creator N°1")
epub.metadata.add_creator("Creator N°2", role="aut")
epub.metadata.add_creator("Creator N°3", file_as="Creator 3", role="oth")
epub.metadata.add_subject("Subject N°1")
epub.metadata.add_subject("Subject N°2")
epub.metadata.set_description("Description")
epub.metadata.add_contributor("Contributor N°1")
epub.metadata.add_contributor("Contributor N°2", role="aut")
epub.metadata.add_contributor("Contributor N°3", file_as="Contributor 3", role="oth")
epub.metadata.add_date("2014")
epub.metadata.add_date("2014-12", event="modification")
epub.metadata.add_date("2014-12-25", event="publication")
epub.metadata.set_type("type")
epub.metadata.set_format("format")
epub.metadata.add_identifier("uuid002")
epub.metadata.add_identifier("uuid003", "myid", "scheme")
epub.metadata.set_source("source")
epub.metadata.add_language("en-US")
epub.metadata.add_language("fr-fr")
epub.metadata.add_language("de")
epub.metadata.set_relation("relation")
epub.metadata.set_coverage("coverage")
epub.metadata.set_rights("rights")
epub.metadata.add_meta("name1", "content1")
epub.metadata.add_meta("name2", "content2")

epub.guide.add_reference(type="title-page", title="Title page", href="titlepage.xhtml")
epub.guide.add_reference(type="toc", title="Table of Contents", href="contents.xhtml")

epub.contents.add_navpoint(epub2.NavPoint("chap1", "Chapter 1", "chapter1.xhtml"))
epub.contents.add_navpoint(epub2.NavPoint("chap2", "Chapter 2", "chapter2.xhtml"))

epub.add_text_from_string(id="titlepage", localname="titlepage.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
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

epub.add_text_from_string(id="contents", localname="contents.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
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

epub.add_text_from_string(id="chap1", localname="chapter1.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <title>Chapiter 1</title>
    <link rel="stylesheet" href="main.css" type="text/css" />
  </head>
  <body>
    <h1>Chapter 1</h1>
    <p>Et eodem impetu Domitianum praecipitem per scalas itidem funibus
    constrinxerunt, eosque coniunctos per ampla spatia civitatis acri raptavere
    discursu. iamque artuum et membrorum divulsa conpage superscandentes corpora
    mortuorum ad ultimam truncata deformitatem velut exsaturati mox abiecerunt
    in flumen.</p>
    <p>Ideoque fertur neminem aliquando ob haec vel similia poenae addictum
    oblato de more elogio revocari iussisse, quod inexorabiles quoque principes
    factitarunt. et exitiale hoc vitium, quod in aliis non numquam intepescit,
    in illo aetatis progressu effervescebat, obstinatum eius propositum
    accendente adulatorum cohorte.</p>
    <p>Eo adducta re per Isauriam, rege Persarum bellis finitimis inligato
    repellenteque a conlimitiis suis ferocissimas gentes, quae mente quadam
    versabili hostiliter eum saepe incessunt et in nos arma moventem aliquotiens
    iuvant, Nohodares quidam nomine e numero optimatum, incursare Mesopotamiam
    quotiens copia dederit ordinatus, explorabat nostra sollicite, si
    repperisset usquam locum vi subita perrupturus.</p>
  </body>
</html>""")

epub.add_text_from_string(id="chap2", localname="chapter2.xhtml", content="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <title>Chapter 2</title>
    <link rel="stylesheet" href="main.css" type="text/css" />
  </head>
  <body>
    <h1>Chapter 2</h1>
    <p>Quam ob rem cave Catoni anteponas ne istum quidem ipsum, quem Apollo, ut
    ais, sapientissimum iudicavit; huius enim facta, illius dicta laudantur. De
    me autem, ut iam cum utroque vestrum loquar, sic habetote.</p>
    <p>Quanta autem vis amicitiae sit, ex hoc intellegi maxime potest, quod ex
    infinita societate generis humani, quam conciliavit ipsa natura, ita
    contracta res est et adducta in angustum ut omnis caritas aut inter duos aut
    inter paucos iungeretur.</p>
  </body>
</html>""")

epub.add_style_from_string("main.css", """h1 {
    border-bottom: 1px solid black;
}""", "style")

epub.add_file_from_file("tux.png", "face.png", "tux", "image/png")

epub.close()
