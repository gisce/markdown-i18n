from setuptools import setup, find_packages


setup(
    name='markdown-i18n',
    version='0.3.0',
    packages=find_packages(),
    url='https://github.com/gisce/markdown-i18n',
    license='MIT',
    install_requires=['Markdown', 'babel'],
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    test_suite="tests",
    description=''
)
