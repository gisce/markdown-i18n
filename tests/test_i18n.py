from __future__ import unicode_literals
import unittest
import os
import tempfile
import shutil

from markdown import markdown

from babel.messages import pofile, mofile, catalog


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
