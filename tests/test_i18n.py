from __future__ import unicode_literals
import unittest
import os
import tempfile
import shutil
import re

from markdown import markdown

from babel.messages import pofile, mofile, catalog


def clean_xml(xml_string):
    return re.sub('\s+<', '<', xml_string)


class TempDir(object):
    def __init__(self):
        self.dir = tempfile.mkdtemp()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dir)


class I18nTest(unittest.TestCase):
    """Basic test for i18n jinja
    """

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        locale = 'es_ES'
        self.catalog = catalog.Catalog(locale=locale)
        os.mkdir(os.path.join(self.dir, locale))
        lc_messages = os.path.join(self.dir, locale, 'LC_MESSAGES')
        os.mkdir(lc_messages)
        self.mo_file = os.path.join(lc_messages, 'messages.mo')

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write_mo(self):
        with open(self.mo_file, 'w') as f:
            mofile.write_mo(f, self.catalog)

    def markdown(self, text, extensions=None, extension_configs=None):
        if extensions is None:
            extensions = []
        extensions.append('markdown_i18n')

        if extension_configs is None:
            extension_configs = {}

        if 'markdown_i18n' not in extension_configs:
            extension_configs['markdown_i18n'] = {
                'i18n_dir': self.dir,
                'i18n_lang': 'es_ES'
            }

        return markdown(
            text,
            extensions=extensions,
            extension_configs=extension_configs
        )

    def test_create_pot_file(self):

        pot_file = os.path.join(self.dir, 'messages.pot')

        text = "this is a simple text"
        self.markdown(text)
        self.assertTrue(os.path.exists(pot_file))

        with open(pot_file, 'r') as f:
            catalog = pofile.read_po(f)
            self.assertIn(text, catalog)
            self.assertEqual(len(catalog), 1)

    def test_basic_text(self):
        text = "this is a simple text"
        expected = '<p>esto es un simple test</p>'

        self.catalog.add("this is a simple text", "esto es un simple test")
        self.write_mo()

        result = self.markdown(text)
        self.assertEqual(expected, result)

    def test_newline_text(self):
        text = "this is a simple\ntext"
        expected = '<p>esto es un simple\ntest</p>'

        self.catalog.add("this is a simple\ntext", "esto es un simple\ntest")
        self.write_mo()

        result = self.markdown(text)
        self.assertEqual(expected, result)

    def test_quoted_text(self):
        text = 'this is a simple "text"'
        expected = '<p>esto es un simple "test"</p>'

        self.catalog.add('this is a simple "text"', 'esto es un simple "test"')
        self.write_mo()

        result = self.markdown(text)
        self.assertEqual(expected, result)

    def test_multi_paragraph(self):
        text = "paragraph 1\n\nparagraph 2"
        expected = '<p>parrafo 1</p>'
        expected += '<p>parrafo 2</p>'

        self.catalog.add('paragraph 1', 'parrafo 1')
        self.catalog.add('paragraph 2', 'parrafo 2')
        self.write_mo()

        result = self.markdown(text)
        self.assertEqual(expected, result)

    def test_headers(self):
        for x in range(1, 7):
            text = "{0} This is a h{1}".format('#' * x, x)
            expected = '<h{0} id="this-is-a-h{0}">Esto es un h{0}</h{0}>'.format(x)

            with TempDir() as d:

                c = catalog.Catalog(locale='es_ES')
                c.add('This is a h{0}'.format(x), 'Esto es un h{0}'.format(x))
                os.mkdir(os.path.join(d.dir, 'es_ES'))
                lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
                os.mkdir(lc_messages)
                mo_file = os.path.join(lc_messages, 'messages.mo')
                with open(mo_file, 'w') as f:
                    mofile.write_mo(f, c)

                result = self.markdown(
                    text,
                    extensions=['markdown.extensions.toc'],
                    extension_configs={
                        'markdown_i18n': {
                            'i18n_dir': d.dir,
                            'i18n_lang': 'es_ES'
                        }
                    }
                )
                self.assertEqual(expected, result)

    def test_ulists(self):
        text = "* First element.\n * Second element.\n"
        expected = """<ul>
<li>Primer elemento.</li>

<li>Segundo elemento.</li>
</ul>"""

        self.catalog.add("First element.", "Primer elemento.")
        self.catalog.add("Second element.", "Segundo elemento.")
        self.write_mo()

        result = self.markdown(text)
        self.assertEqual(clean_xml(expected), clean_xml(result))

    def test_nlists(self):
        text = "1. First element.\n 2. Second element.\n"
        expected = """<ol>
<li>Primer elemento.</li>

<li>Segundo elemento.</li>
</ol>"""

        self.catalog.add("First element.", "Primer elemento.")
        self.catalog.add("Second element.", "Segundo elemento.")
        self.write_mo()

        result = self.markdown(text)
        self.assertEqual(clean_xml(expected), clean_xml(result))

    def test_merge_existing_pot(self):

        pot_file = os.path.join(self.dir, 'messages.pot')

        text1 = "this is a simple text"
        self.markdown(text1)

        self.assertTrue(os.path.exists(pot_file))

        text2 = "another text"
        self.markdown(text2)

        with open(pot_file, 'r') as f:
            po_file = pofile.read_po(f)
            self.assertEqual(len(po_file), 2)
            self.assertIn(text1, po_file)
            self.assertIn(text2, po_file)

    def test_no_translate_code(self):
        text = ('```bash\n'
                '$ python --version\n'
                'Python 2.7.2\n'
                '$ pip --version\n'
                'pip 1.5.2\n'
                '```')
        expected = ('<pre><code class="bash">$ python --version\n'
                    'Python 2.7.2\n'
                    '$ pip --version\n'
                    'pip 1.5.2\n'
                    '</code></pre>')

        result = self.markdown(
            text,
            extensions=['markdown.extensions.fenced_code']
        )
        self.assertEqual(clean_xml(expected), clean_xml(result))

    def test_tables(self):
        text = """
First Header  | Second Header
------------- | -------------
Content 1     | Content 2
        """
        expected = """<table>
<thead>
<tr>
<th>Encabezamiento primero</th>
<th>Encabezamiento segundo</th>
</tr>
</thead>
<tbody>
<tr>
<td>Contenido 1</td>
<td>Contenido 2</td>
</tr>
</tbody>
</table>"""

        self.catalog.add("First Header", "Encabezamiento primero")
        self.catalog.add("Second Header", "Encabezamiento segundo")
        self.catalog.add("Content 1", "Contenido 1")
        self.catalog.add("Content 2", "Contenido 2")
        self.write_mo()

        result = self.markdown(
            text,
            extensions=['markdown.extensions.tables']
        )
        self.assertEqual(clean_xml(expected), clean_xml(result))

    def test_admonition(self):

        text = (
            "!!!note\n"
            "    This is a note."
        )

        expected = (
            '<div class="admonition note">'
            '    <p class="admonition-title">Note</p>'
            '    <p>Esto es una nota.</p>'
            '</div>'
        )

        self.catalog.add("This is a note.", "Esto es una nota.")
        self.write_mo()

        result = self.markdown(
            text,
            extensions=['markdown.extensions.admonition'],
        )

        self.assertEqual(clean_xml(expected), clean_xml(result))

    def test_code_tag(self):
        text = 'ports like: `"com1", "com2"`'
        expected = '<p>puertos como: <code>"com1", "com2"</code></p>'

        self.catalog.add(
            'ports like: <code>"com1", "com2"</code>',
            'puertos como:<code>"com1", "com2"</code>'
        )
        self.write_mo()

        result = self.markdown(text)
        self.assertEqual(clean_xml(result), clean_xml(expected))
