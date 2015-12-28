# dupeGuru

[dupeGuru][dupeguru] is a cross-platform (Linux, OS X, Windows) GUI tool to find duplicate files in
a system. It's written mostly in Python 3 and has the peculiarity of using
[multiple GUI toolkits][cross-toolkit], all using the same core Python code. On OS X, the UI layer
is written in Objective-C and uses Cocoa. On Linux and Windows, it's written in Python and uses Qt5.

dupeGuru comes in 3 editions (standard, music and picture) which are all buildable from this same
source tree. You choose the edition you want to build in a `configure.py` flag.

# Current status: People wanted

dupeGuru has currently only one maintainer, me. This is a dangerous situation that needs to be
corrected.

The goal is to eventually have another active maintainer, but before we can get there, the project
needs more contributors. It is very much lacking on that side right now.

Whatever your skills, if you are remotely interestested in being a contributor, I'm interested in
mentoring you. If that's the case, please refer to [the open ticket on the subject][contrib-issue]
and let's get started.

## Slowed development

Until I manage to find contributors, I'm slowing the development pace of dupeGuru. I'm not much
interested in maintaining it alone, I personally have no use for this app (it's been a *loooong*,
time since I had dupe problems :) )

I don't want to let it die, however, so I will still do normal maintainership, that is, issue
triaging, code review, critical bugfixes, releases management.

But anything non-critical, I'm not going to implement it myself because I see every issue as a
contribution opportunity.

# Contents of this folder

This folder contains the source for dupeGuru. Its documentation is in `help`, but is also
[available online][documentation] in its built form. Here's how this source tree is organised:

* core: Contains the core logic code for dupeGuru. It's Python code.
* core_*: Edition-specific-cross-toolkit code written in Python.
* cocoa: UI code for the Cocoa toolkit. It's Objective-C code.
* qt: UI code for the Qt toolkit. It's written in Python and uses PyQt.
* images: Images used by the different UI codebases.
* pkg: Skeleton files required to create different packages
* help: Help document, written for Sphinx.
* locale: .po files for localisation.

There are also other sub-folder that comes from external repositories and are part of this repo as
git subtrees:

* hscommon: A collection of helpers used across HS applications.
* cocoalib: A collection of helpers used across Cocoa UI codebases of HS applications.
* qtlib: A collection of helpers used across Qt UI codebases of HS applications.

# How to build dupeGuru from source

## The very, very, very easy way

If you're on Linux or Mac, there's a bootstrap script that will make building very, very easy. There
might be some things that you need to install manually on your system, but the bootstrap script will
tell you when what you need to install. You can run the bootstrap with:

    ./bootstrap.sh

and follow instructions from the script. You can then ignore the rest of the build documentation.

If building of the help files fails with an unknown locale error, set your locale environment:

    $ export LC_ALL=en_US.UTF-8
    $ export LANG=en_US.UTF-8

## Prerequisites installation

Prerequisites are installed through `pip`. However, some of them are not "pip installable" and have
to be installed manually.

* All systems: [Python 3.3+][python] and [setuptools][setuptools]
* Mac OS X: The last XCode to have the 10.7 SDK included. Python 3.4+.
* Windows: Visual Studio 2010, [PyQt 5.0+][pyqt], [cx_Freeze][cxfreeze] and
  [Advanced Installer][advinst] (you only need the last two if you want to create an installer)

On Ubuntu (14.04+), the apt-get command to install all pre-requisites is:

    $ apt-get install python3-dev python3-pyqt5 pyqt5-dev-tools

On Arch, it's:

    $ pacman -S python-pyqt5

### OS X and pyenv

[pyenv][pyenv] is a popular way to manage multiple python versions. However, be aware that dupeGuru
will not compile with a pyenv's python unless it's been built with `--enable-framework`. You can do
this with:

    $ env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.4.3

## Setting up the virtual environment

Use Python's built-in `pyvenv` to create a virtual environment in which we're going to install our.
Python-related dependencies. `pyvenv` is built-in Python but, unlike its `virtualenv` predecessor,
it doesn't install setuptools and pip (unless you use Python 3.4+), so it has to be installed
manually:

    $ pyvenv --system-site-packages env
    $ source env/bin/activate
    $ python get-pip.py

Then, you can install pip requirements in your virtualenv:

    $ pip install -r requirements-[osx|win].txt
    
([osx|win] depends, of course, on your platform. On other platforms, just use requirements.txt).

## Actual building and running

With your virtualenv activated, you can build and run dupeGuru with these commands:

    $ python configure.py
    $ python build.py
    $ python run.py

You can also package dupeGuru into an installable package with:
    
    $ python package.py

[dupeguru]: http://www.hardcoded.net/dupeguru/
[cross-toolkit]: http://www.hardcoded.net/articles/cross-toolkit-software
[contrib-issue]: https://github.com/hsoft/dupeguru/issues/300
[documentation]: http://www.hardcoded.net/dupeguru/help/en/
[python]: http://www.python.org/
[setuptools]: https://pypi.python.org/pypi/setuptools
[pyqt]: http://www.riverbankcomputing.com
[cxfreeze]: http://cx-freeze.sourceforge.net/
[advinst]: http://www.advancedinstaller.com
[pyenv]: https://github.com/yyuu/pyenv
