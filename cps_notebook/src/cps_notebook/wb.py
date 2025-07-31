#! /usr/bin/env python3
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
import argparse
import jinja2
import logging
import os

from wikibaseintegrator.wbi_config import config as wbi_config

from cps_wb.wikibase import WB

from dotenv import load_dotenv

def main():
    ##################################################################
    # CLASS TEST AND DEBUG
    #
    parser = argparse.ArgumentParser(description="Wikibase project", epilog="example: wb project", add_help=True)

    parser.add_argument("-f", "--format", type=str, help="output format: html|raw")
    parser.add_argument("project", type=str, help="project name")

    args = parser.parse_args()

    if not args.format or args.format == "raw":
        fmt = "raw"
    elif args.format == "html":
        fmt = "html"
    else:
        raise Exception("format must be html or raw")

    w = W(args.project)
    if fmt == "raw":
        for row in w.result_list:
            print(row)
    else:
        print(w.html())

class W:
    # akamaitechnologies hangs unless it recognises the User-Agent
    _USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134."

    _project_dir = None # Project directory

    _html_template = None # HTML template filename

    result_list = None # Wikibase query results (List of Dict)

    def __init__(self, project_name):
        load_dotenv(os.getcwd() + os.sep + ".env")

        if os.getenv("LOGGING"):
            logging.basicConfig(level=os.getenv("LOGGING"), format="%(asctime)s %(name)s %(message)s")
        else:
            logging.basicConfig(level="INFO", format="%(asctime)s %(name)s %(message)s")

        ##################################################################
        # Wikibaseintegrator configuration
        #
        if not os.getenv("WB_URL"):
            raise Exception("WB_URL is missing")

        if not os.getenv("WB_USERNAME"):
            raise Exception("WB_USERNAME is missing")

        if not os.getenv("WB_PASSWORD"):
            raise Exception("WB_PASSWORD is missing")

        wbi_config["DEFAULT_LANGUAGE"] = "en"
        wbi_config["USER_AGENT"] = self._USER_AGENT
        wbi_config["WIKIBASE_URL"] = os.getenv("WB_URL")
        wbi_config["MEDIAWIKI_API_URL"] = os.getenv("WB_URL") + "w/api.php"

        ##################################################################
        # Project files
        #
        self._project_dir = os.getenv("PROJECT_DIR")
        if not self._project_dir:
            raise Exception("PROJECT_DIR is missing")
        elif not self._project_dir.endswith('/'):
            self._project_dir += '/'

        wb_query = self._project_dir + project_name + ".wb"
        if not os.path.isfile(wb_query):
            raise Exception("no Wikibase query [{wb_query}]")

        self._html_template = project_name + ".html"

        ##################################################################
        # Wikibase query
        #
        query = ""
        with open(wb_query, "r", encoding="utf-8") as f:
            for line in f:
                if not line.startswith('#'):
                    query = line.strip()
                    break

        # Get wikibase entity
        if not query.startswith("P") and not query.startswith("Q"):
            raise Exception("no Wikibase entity")

        # Login to Wikibase
        wb = WB(os.getenv("WB_USERNAME"), os.getenv("WB_PASSWORD"))

        # Get wikibase entity
        if query.startswith("P"):
            e = wb.Pproperty(query)

        elif query.startswith("Q"):
            e = wb.Qitem(query)

        self.result_list = wb.Edict(e)

    def html(self):
        raise Exception("not implemented")

if __name__=="__main__":
    main()

# vim: shiftwidth=4 tabstop=4 softtabstop=4 expandtab
