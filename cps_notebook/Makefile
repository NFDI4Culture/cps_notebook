#
# Copyright (C) 2025 The Authors
# All rights reserved.
#
# This file is part of cps_notebook.
#
# cps_notebook is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation.
#
# cps_notebook is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with cps_notebook. If not, see http://www.gnu.org/licenses/
#

cps_notebook:
	python3 -m pip install --no-dependencies .

clean:
	find -name "*~" -delete

distclean:clean
	rm -Rf dist

install:
	python3 -m pip install .
	python3 -m pip install dotenv
	python3 -m pip install -i https://test.pypi.org/simple/ "cps-wb>=0.1.3"
	#python3 -m pip install hg+https://hg.kewl.org/pub/cps_wb

uninstall:
	python3 -m pip uninstall -y cps_notebook

venv:
	python3 -m venv ~/.venvs/cps_notebook

tools:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine

build:distclean
	python3 -m build

upload:
	python3 -m twine upload --verbose --repository testpypi dist/*

ls:
	find -type f -not -path "./.hg/*" -ls

notebook:
	cd src/cps_notebook && jupyter-notebook
