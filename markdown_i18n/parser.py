from __future__ import unicode_literals
import logging
import os

from markdown.treeprocessors import Treeprocessor
from markdown.util import etree

from babel.messages.catalog import Catalog
from babel.messages import pofile
from babel.support import Translations


logger = logging.getLogger(__name__)


class I18NTreeProcessor(Treeprocessor):

    def __init__(self, md, extension):
        self.extension = extension
        super(I18NTreeProcessor, self).__init__(md)

    def run(self, root):

        i18n_dir = self.extension.getConfig('i18n_dir')

        catalog = Catalog()

        lang = self.extension.getConfig('i18n_lang')
        translations = Translations.load(i18n_dir, locales=[lang])

        childs = root.getchildren()
        for idx, child in enumerate(childs):
            if child.tag in ('p', 'h1'):
                translatable = child.text or ''
                translatable += '\n'.join([
                    etree.tostring(c) for c in child.getchildren() if c.tag != 'code'
                ])
                if translatable:
                    catalog.add(translatable)
                    content = '<{0}>{1}</{0}>'.format(
                        child.tag, translations.gettext(translatable)
                    )
                    try:
                        new_node = etree.fromstring(content.encode('utf-8'))
                        root.remove(child)
                        root.insert(idx, new_node)
                    except etree.ParseError:
                        pass

        pot_path = os.path.join(i18n_dir, 'messages.pot')

        with open(pot_path, 'w') as pot_file:
            pofile.write_po(pot_file, catalog)
