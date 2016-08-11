Markdown i18n
=============

.. image:: https://travis-ci.org/gisce/markdown-i18n.svg?branch=master
    :target: https://travis-ci.org/gisce/markdown-i18n

This is an extension for `Python Markdown <http://pythonhosted.org/Markdown/>`_

Install
-------

.. code-block::

  $ pip install markdown-i18n

Configure
---------

* i18n_lang: Lang to use on rendering
* i18n_dir: Path to localitzation

The structure of `i18n_dir` must be:

.. code-block::

    ├── en_US
    │   └── LC_MESSAGES
    │       ├── messages.mo
    │       └── messages.po
    └── messages.pot

The first time rendering the content it will generate the ``messages.pot`` file
