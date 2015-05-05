#!/usr/bin/python
# -*- coding: utf8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from urllib2 import HTTPError
from rdflib import Graph
from xml.etree import ElementTree
import requests


DOAPs = "https://svn.apache.org/repos/asf/infrastructure/site-tools/trunk/projects/files.xml"
PMCs  = "https://svn.apache.org/repos/asf/infrastructure/site-tools/trunk/projects/pmc_list.xml"


class DOAP:

    def __init__(self, url):
        self.url = url
        self.graph = Graph()
        self.graph.load(url)

    def __len__(self):
        return len(self.graph)


class LocationsFile:

    def __init__(self, path):
        self.path = path
        dir = os.path.dirname(path)
        self.locations = []      
        r = requests.get(path) #TODO: in the real site path would refer to a local file      
        #tree = ElementTree.parse(path)
        tree = ElementTree.fromstring(r.text)
        for location in tree.findall("location"):
            if location.text.startswith("http://") or location.text.startswith("https://"):
                self.locations.append(location.text)
            else:
                self.locations.append("%s/%s" % (dir, location.text))

    def __len__(self):
        return len(self.locations)          

    def __iter__(self):
        return iter(self.locations)
            


if __name__ == "__main__":

    for url in [DOAPs, PMCs]:
        errors = 0
        print
        print "%s:" % url
        print '-' * len(url)
        print
        locations = LocationsFile(url)
        for location in locations:
            try:
                doap = DOAP(location)
                print " - %s : %d RDF triples in the DOAP file" % (location, len(doap))
            except HTTPError, e:
                errors += 1
                print " - %s : %s" % (location, str(e))
        print
        print "(%d errors)" % errors
        print

