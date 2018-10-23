from markdown.extensions import Extension
from markdown_i18n.parser import I18NTreeProcessor


class I18NExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'i18n_lang': ['en_US', 'Locale'],
            'i18n_dir': ['', 'Path to get the translations and']
        }
        self.toc_found = False
        self.md = None
        self.priority = 1
        super(I18NExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.treeprocessors.register(
            I18NTreeProcessor(md, self), 'i18n', self.priority)
        self.md = md

    def reset(self):
        if not self.toc_found and 'toc' in self.md.treeprocessors:
            self.md.treeprocessors.add(
                'i18n', I18NTreeProcessor(self.md, self), '<toc')
            self.toc_found = True
