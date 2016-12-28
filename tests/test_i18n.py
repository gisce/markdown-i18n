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

    def test_create_pot_file(self):
        with TempDir() as d:
            pot_file = os.path.join(d.dir, 'messages.pot')

            text = "this is a simple text"
            markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={'markdown_i18n': {'i18n_dir': d.dir}}
            )
            self.assertTrue(os.path.exists(pot_file))

            with open(pot_file, 'r') as f:
                catalog = pofile.read_po(f)
                self.assertIn(text, catalog)
                self.assertEqual(len(catalog), 1)

    def test_basic_text(self):
        text = "this is a simple text"
        expected = '<p>esto es un simple test</p>'
        with TempDir() as d:

            c = catalog.Catalog(locale='es_ES')
            c.add("this is a simple text", "esto es un simple test")
            os.mkdir(os.path.join(d.dir, 'es_ES'))
            lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
            os.mkdir(lc_messages)
            mo_file = os.path.join(lc_messages, 'messages.mo')
            with open(mo_file, 'w') as f:
                mofile.write_mo(f, c)

            result = markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(expected, result)

    def test_newline_text(self):
        text = "this is a simple\ntext"
        expected = '<p>esto es un simple\ntest</p>'
        with TempDir() as d:
            c = catalog.Catalog(locale='es_ES')
            c.add("this is a simple\ntext", "esto es un simple\ntest")
            os.mkdir(os.path.join(d.dir, 'es_ES'))
            lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
            os.mkdir(lc_messages)
            mo_file = os.path.join(lc_messages, 'messages.mo')
            with open(mo_file, 'w') as f:
                mofile.write_mo(f, c)

            result = markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(expected, result)

    def test_quoted_text(self):
        text = 'this is a simple "text"'
        expected = '<p>esto es un simple "test"</p>'
        with TempDir() as d:
            c = catalog.Catalog(locale='es_ES')
            c.add('this is a simple "text"', 'esto es un simple "test"')
            os.mkdir(os.path.join(d.dir, 'es_ES'))
            lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
            os.mkdir(lc_messages)
            mo_file = os.path.join(lc_messages, 'messages.mo')
            with open(mo_file, 'w') as f:
                mofile.write_mo(f, c)

            result = markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(expected, result)

    def test_multi_paragraph(self):
        text = "paragraph 1\n\nparagraph 2"
        expected = '<p>parrafo 1</p>'
        expected += '<p>parrafo 2</p>'
        with TempDir() as d:
            c = catalog.Catalog(locale='es_ES')
            c.add('paragraph 1', 'parrafo 1')
            c.add('paragraph 2', 'parrafo 2')
            os.mkdir(os.path.join(d.dir, 'es_ES'))
            lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
            os.mkdir(lc_messages)
            mo_file = os.path.join(lc_messages, 'messages.mo')
            with open(mo_file, 'w') as f:
                mofile.write_mo(f, c)

            result = markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(expected, result)

    def test_headers(self):
        for x in range(1, 7):
            text = "{0} This is a h{1}".format('#' * x, x)
            expected = '<h{0}>Esto es un h{0}</h{0}>'.format(x)
            with TempDir() as d:
                c = catalog.Catalog(locale='es_ES')
                c.add('This is a h{0}'.format(x), 'Esto es un h{0}'.format(x))
                os.mkdir(os.path.join(d.dir, 'es_ES'))
                lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
                os.mkdir(lc_messages)
                mo_file = os.path.join(lc_messages, 'messages.mo')
                with open(mo_file, 'w') as f:
                    mofile.write_mo(f, c)

                result = markdown(
                    text,
                    extensions=['markdown_i18n'],
                    extension_configs={
                        'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                    }
                )
            self.assertEqual(expected, result)

    def test_ulists(self):
        text = "* First element.\n * Second element.\n"
        expected = """<ul>
<li>Primer elemento.</li>

<li>Segundo elemento.</li>
</ul>"""
        with TempDir() as d:
            c = catalog.Catalog(locale='es_ES')
            c.add(
                """
<li>First element.</li>

<li>Second element.</li>
""", """
<li>Primer elemento.</li>

<li>Segundo elemento.</li>
"""
            )
            os.mkdir(os.path.join(d.dir, 'es_ES'))
            lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
            os.mkdir(lc_messages)
            mo_file = os.path.join(lc_messages, 'messages.mo')
            with open(mo_file, 'w') as f:
                mofile.write_mo(f, c)

            result = markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(expected, result)

    def test_nlists(self):
        text = "1. First element.\n 2. Second element.\n"
        expected = """<ol>
<li>Primer elemento.</li>

<li>Segundo elemento.</li>
</ol>"""
        with TempDir() as d:
            c = catalog.Catalog(locale='es_ES')
            c.add(
                """
<li>First element.</li>

<li>Second element.</li>
""", """
<li>Primer elemento.</li>

<li>Segundo elemento.</li>
"""
            )
            os.mkdir(os.path.join(d.dir, 'es_ES'))
            lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
            os.mkdir(lc_messages)
            mo_file = os.path.join(lc_messages, 'messages.mo')
            with open(mo_file, 'w') as f:
                mofile.write_mo(f, c)

            result = markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir,
                                      'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(expected, result)

    def test_merge_existing_pot(self):
        with TempDir() as d:
            pot_file = os.path.join(d.dir, 'messages.pot')

            text1 = "this is a simple text"
            markdown(
                text1,
                extensions=['markdown_i18n'],
                extension_configs={'markdown_i18n': {'i18n_dir': d.dir}}
            )

            self.assertTrue(os.path.exists(pot_file))

            text2 = "another text"
            markdown(
                text2,
                extensions=['markdown_i18n'],
                extension_configs={'markdown_i18n': {'i18n_dir': d.dir}}
            )

            with open(pot_file, 'r') as f:
                catalog = pofile.read_po(f)
                self.assertEqual(len(catalog), 2)
                self.assertIn(text1, catalog)
                self.assertIn(text2, catalog)

    @unittest.skip('working on it')
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
        with TempDir() as d:
            result = markdown(
                text,
                extensions=['markdown_i18n'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(expected, result)

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
        with TempDir() as d:

            c = catalog.Catalog(locale='es_ES')
            c.add("First Header", "Encabezamiento primero")
            c.add("Second Header", "Encabezamiento segundo")
            c.add("Content 1", "Contenido 1")
            c.add("Content 2", "Contenido 2")
            os.mkdir(os.path.join(d.dir, 'es_ES'))
            lc_messages = os.path.join(d.dir, 'es_ES', 'LC_MESSAGES')
            os.mkdir(lc_messages)
            mo_file = os.path.join(lc_messages, 'messages.mo')
            with open(mo_file, 'w') as f:
                mofile.write_mo(f, c)

            result = markdown(
                text,
                extensions=['markdown_i18n', 'markdown.extensions.tables'],
                extension_configs={
                    'markdown_i18n': {'i18n_dir': d.dir, 'i18n_lang': 'es_ES'}
                }
            )
        self.assertEqual(clean_xml(expected), clean_xml(result))
