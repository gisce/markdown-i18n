from setuptools import setup, find_packages


setup(
    name='markdown-i18n',
    version='3.0.0',
    packages=find_packages(),
    url='https://github.com/gisce/markdown-i18n',
    license='MIT',
    install_requires=[
        'Markdown>=3',
        'babel',
        'six'
    ],
    entry_point={
        'markdown.extensions': [
            'markdown_i18n = markdown_i18n.extension.py:I18NExtension'
        ]
    },
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    test_suite="tests",
    description='i18n extension for Python Markdown'
)
