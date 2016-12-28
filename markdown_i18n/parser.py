from __future__ import unicode_literals
import os
import re

from markdown.treeprocessors import Treeprocessor
from markdown.util import etree

from babel.messages.catalog import Catalog
from babel.messages import pofile
from babel.support import Translations

TRANSLATE_TAGS_RE = re.compile('^(li|p|h[1-6]|th|td)$')


class I18NTreeProcessor(Treeprocessor):

    def __init__(self, md, extension):
        self.extension = extension
        super(I18NTreeProcessor, self).__init__(md)

    def translate(self, catalog, translations, root):
        children = root.getchildren()
        for idx, child in enumerate(children):
            if re.match(TRANSLATE_TAGS_RE, child.tag):
                translatable = child.text or ''
                translatable += '\n'.join([
                    etree.tostring(c) for c in
                        child.getchildren() if
                            c.tag != 'code'
                ])
                if translatable:
                    catalog.add(translatable)
                    attrs = ' '.join((
                        '{}="{}"'.format(k, v) for k, v in child.attrib.items()
                    ))
                    content = '<{0} {2}>{1}</{0}>'.format(
                        child.tag, translations.gettext(translatable), attrs
                    )
                    try:
                        new_node = etree.fromstring(content.encode('utf-8'))
                        root.remove(child)
                        root.insert(idx, new_node)
                    except etree.ParseError:
                        pass
            else:
                self.translate(catalog, translations, child)

    def run(self, root):

        i18n_dir = self.extension.getConfig('i18n_dir')
        pot_path = os.path.join(i18n_dir, 'messages.pot')

        if os.path.exists(pot_path):
            with open(pot_path, 'r') as f:
                catalog = pofile.read_po(f)
        else:
            catalog = Catalog()

        lang = self.extension.getConfig('i18n_lang')
        translations = Translations.load(i18n_dir, locales=[lang])
        self.translate(catalog, translations, root)

        with open(pot_path, 'w') as pot_file:
            pofile.write_po(pot_file, catalog)
