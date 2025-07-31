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
import os

from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator import wbi_helpers

from dotenv import load_dotenv

def main():
    ##################################################################
    # CLASS TEST AND DEBUG
    #
    parser = argparse.ArgumentParser(description="SPARQL project", epilog="example: sparql project", add_help=True)

    parser.add_argument("-f", "--format", type=str, help="output format: html|raw")
    parser.add_argument("project", type=str, help="project name")

    args = parser.parse_args()

    if not args.format or args.format == "raw":
        fmt = "raw"
    elif args.format == "html":
        fmt = "html"
    else:
        raise Exception("format must be html or raw")

    s = SPARQL(args.project)
    if fmt == "raw":
        for row in s.result_list:
            print(row)
    else:
        print(s.html())

class SPARQL:
    # akamaitechnologies hangs unless it recognises the User-Agent
    _USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134."

    _project_dir = None # Project directory

    _html_template = None # HTML template filename

    result_list = None # SPARQL query results (List of Dict)

    def __init__(self, project_name):
        load_dotenv(os.getcwd() + os.sep + ".env")

        ##################################################################
        # SPARQL query service
        #
        wbi_config["DEFAULT_LANGUAGE"] = "en"
        wbi_config["USER_AGENT"] = self._USER_AGENT
        if os.getenv("SPARQL_URL"):
            wbi_config['SPARQL_ENDPOINT_URL'] = os.getenv("SPARQL_URL")

        ##################################################################
        # Project files
        #
        self._project_dir = os.getenv("PROJECT_DIR")
        if not self._project_dir:
            raise Exception("PROJECT_DIR is missing")
        elif not self._project_dir.endswith('/'):
            self._project_dir += '/'

        sparql_query = self._project_dir + project_name + ".sparql"
        if not os.path.isfile(sparql_query):
            raise Exception(f"no SPARQL query [{sparql_query}]")

        self._html_template = project_name + ".html"

        ##################################################################
        # SPARQL query
        #
        query = ""
        with open(sparql_query, "r", encoding="utf-8") as f:
            for line in f:
                query += line

        res = wbi_helpers.execute_sparql_query(query, prefix=os.getenv("SPARQL_PREFIX"))
        try:
            bindings = res["results"]["bindings"]
        except:
            raise Exception("no result bindings")

        ##################################################################
        # Result list
        #
        self.result_list = []
        for binding in bindings:
            result_dict = {}
            for key in binding:
                result_dict[key] = binding[key]['value']
            self.result_list.append(result_dict)

    def html(self):
        if not os.path.isfile(self._project_dir + self._html_template):
            raise Exception("no HTML template")

        template_loader = jinja2.FileSystemLoader(searchpath=self._project_dir)
        template_env = jinja2.Environment(loader=template_loader, autoescape=True)
        template = template_env.get_template(self._html_template)

        return template.render(list=self.result_list)

if __name__=="__main__":
    main()

# vim: shiftwidth=4 tabstop=4 softtabstop=4 expandtab
