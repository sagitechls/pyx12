######################################################################
# Copyright (c) 2001-2011 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Locate the correct xml map file given:
    - Interchange Control Version Number (ISA12)
    - Functional Identifier Code (GS01)
    - Version / Release / Industry Identifier Code (GS08)
    - Transaction Set Purpose Code (BHT02) (For 278 only)
"""

import xml.etree.ElementTree
import errors

class map_index(object):
    """
    Interface to the maps.xml file
    """
    def __init__(self, map_index_file):
        """
        @param map_index_file: Absolute path of maps.xml
        @type map_index_file: string
        """
        self.maps = []

        t = xml.etree.ElementTree.parse(map_index_file)
        for v in t.iter('version'):
            icvn = v.get('icvn')
            for m in v.iterfind('map'):
                self.add_map(icvn, m.get('vriic'), m.get('fic'), m.get('tspc'), m.text, m.get('abbr'))
    
    def add_map(self, icvn, vriic, fic, tspc, map_file, abbr):
        self.maps.append({'icvn':icvn, 'vriic':vriic, 'fic':fic, 'tspc':tspc, 'map_file':map_file, 'abbr':abbr})
    
    def get_filename(self, icvn, vriic, fic, tspc=None):
        """
        Get the map filename associated with the given icvn, vriic, fic, 
        and tspc values
        @rtype: string
        """
        for a in self.maps:
            if a['icvn'] == icvn and a['vriic'] == vriic and a['fic'] == fic \
                    and (tspc is None or a['tspc'] == tspc):
                return a['map_file']
        return None

    def get_abbr(self, icvn, vriic, fic, tspc=None):
        """
        Get the informal abbreviation associated with the given icvn, vriic, 
        fic, and tspc values
        @rtype: string
        """
        for a in self.maps:
            if a['icvn'] == icvn and a['vriic'] == vriic and a['fic'] == fic \
                    and (tspc is None or a['tspc'] == tspc):
                return a['abbr']
        return None

    def print_all(self):
        for a in self.maps:
            print a

