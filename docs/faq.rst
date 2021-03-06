Frequently Asked Questions
==========================

Configuration
+++++++++++++

.. _auto-workflow:

How to create automatic worflow?
--------------------------------

Weblate can handle all the translation things semi-automatically for you. If
you will give it push access to your repository, the translations can live
without interaction unless some merge conflict occurs.

1. Set up you git repository to tell Weblate whenever there is any change, see
   :ref:`hooks` for information how to do it.
2. Set push URL at your :ref:`subproject` in Weblate, this will allow Weblate
   to push changes to your repository.
3. Enable push on commit on your :ref:`project` in Weblate, this will make
   Weblate push changes to your repo whenever they are commited at Weblate.

How to fix merge conflicts in translations?
-------------------------------------------

The easiest way is to solve all conflicts locally at your workstation - simply
add Weblate as remote repository, merge it into upstream and fix conflicts.
Once you push changes back, Weblate will be able to use merged version without
any other special actions.

.. seealso:: :ref:`git-export`

.. _git-export:

How to export Git repository weblate uses?
------------------------------------------

There is nothing special about the repository, it lives under
:setting:`GIT_ROOT` directory and is named as `project/subproject/`. If you
have SSH access to this machine, you can use the repository directly.

For anonymous acces you might want to run git server and let it serve the
repository to outside world.

What are options of pushing changes back upstream?
--------------------------------------------------

This heavily depends on your setup, Weblate is quite flexible in this area.
Here are examples of workflows used with Weblate:

- Weblate automatically pushes and merges changes (see :ref:`auto-workflow`)
- You tell manually Weblate to push (it needs push access to upstream repository)
- Somebody manually merges changes from Weblate git repository into upstream 
  repository
- Somebody rewrites history produced by Weblate (eg. by eliminating merge
  commits), merges changes and tells Weblate to reset contet on upstream
  repository.

Of course your are free to mix all of these as you wish.

Troubleshooting
+++++++++++++++

Requests sometimes fail with too many open files error
------------------------------------------------------

This happens sometimes when your Git repository grows too much and you have
more of them. Compressing the Git repositories will improve this situation.

The easiest way to do this is to run:

.. code-block:: sh

    cd repos
    for d in */* ; do
        pushd $d
        git gc
        popd
    done

.. _faq-ft-slow:

Fulltext search is too slow
---------------------------

Depending on various conditions (frequency of updates, server restarts and
other), fulltext index might get too fragmented over time. It is recommended to
rebuild it from scratch time to time:

.. code-block:: sh

    ./manage.py rebuild_index --clean

.. seealso:: :djadmin:`rebuild_index`

.. _faq-ft-lock:

I get "Lock Error" quite often while translating
------------------------------------------------

This is usually caused by concurent updates to fulltext index. In case you are
running multithreaded server (eg. mod_wsgi), this happens quite often. For such
setup it is recommended to enable :setting:`OFFLOAD_INDEXING`.

.. seealso:: :ref:`fulltext`

.. _faq-ft-space:

Rebuilding index has failed with "No space left on device"
----------------------------------------------------------

Whoosh uses temporary directory to build indices. In case you have small /tmp
(eg. using ramdisk), this might fail. Change used temporary directory by passing 
as ``TEMP`` variable:

.. code-block:: sh

    TEMP=/path/to/big/temp ./manage.py rebuild_index --clean

.. seealso:: :djadmin:`rebuild_index`

Features
++++++++

Does Weblate support other VCS than Git?
----------------------------------------

Not currently. Weblate requires distributed VCS and could be probably adjusted
to work with anything else than Git, but somebody has to implement this support.

Why does Weblate force to have show all po files in single tree?
----------------------------------------------------------------

Weblate was designed in a way that every po file is represented as single
subproject. This is beneficial for translators, that they know what they are
actually translating. If you feel your project should be translated as one,
consider merging these po files. It will make life easier even for translators
not using Weblate.

.. note::

    In case there will be big demand for this feature, it might be implemented
    in future versions, but it's definitely not a priority for now.
