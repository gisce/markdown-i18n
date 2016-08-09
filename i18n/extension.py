from markdown.extensions import Extension
from i18n.parser import I18NTreeProcessor


class I18NJinjaExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'i18n_lang': ['en_US', 'Locale'],
            'i18n_dir': ['', 'Path to get the translations and']
        }
        super(I18NJinjaExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('i18n', I18NTreeProcessor(md, self), '_end')
