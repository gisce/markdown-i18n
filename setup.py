from setuptools import setup, find_packages


setup(
    name='markdown-i18n',
    version='2.1.1',
    packages=find_packages(),
    url='https://github.com/gisce/markdown-i18n',
    license='MIT',
    install_requires=['Markdown', 'babel', 'six'],
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    test_suite="tests",
    description='i18n extension for Python Markdown'
)
