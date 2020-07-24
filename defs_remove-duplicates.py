#!/usr/bin/env python
# coding=utf-8

"""
This extension removes copies of marker done by copying element.
"""

import inkex
import re

MARKERS = ['marker', 'marker-start', 'marker-mid', 'marker-end']
REDUP = re.compile(r"(.*?)(-[0-9]{1,2})+$")

class RemoveDuplicates(inkex.EffectExtension):
    def __init__(self):
        inkex.Effect.__init__(self)

    def find_child_items(self, node):
        """
        Recursive method for appending all elements
        to self.selected_items (adapted from replace_font extension)
        """
        yield node
        for child in node:
            for elementchild in self.find_child_items(child):
                yield elementchild

    def effect(self):
        list_of_duplicates_marker = []
        items = []
        selected = self.svg

        for item in selected:
            items.extend(self.find_child_items(item))


        for node in items :
            for attr in MARKERS:
                if not node.style.get(attr, '').startswith('url(#'):
                    continue
                marker_id = node.style[attr][5:-1]
                marker_node = self.svg.getElement('/svg:svg//svg:marker[@id="%s"]' % marker_id)
                if marker_node is None:
                    inkex.errormsg(_("unable to locate marker: %s") % marker_id)
                    continue
                match = re.search(REDUP, marker_id)
                if match :
                    orig_name = match.group(1)
                    marker_orig_node = self.svg.getElement('/svg:svg//svg:marker[@id="%s"]' % orig_name)
                    if marker_orig_node is not None:
                        node.style.update_urls(marker_id, orig_name)
                        list_of_duplicates_marker.append(marker_id)
            #inkex.errormsg(node.tostring()) # the output is ok, but not what I get in inkscape after.

        #remove duplicates markers in defs
        list_of_unique_duplicates_marker = set(list_of_duplicates_marker)
        inkex.errormsg(len(list_of_unique_duplicates_marker))
        inkex.errormsg(list_of_unique_duplicates_marker)
        for marker_id in list_of_unique_duplicates_marker :
            marker_node = self.svg.getElement('/svg:svg//svg:marker[@id="%s"]' % marker_id)
            if marker_node is None:
                    #inkex.errormsg(_("unable to locate marker: %s") % marker_id)
                    continue
            else :
                marker_node.delete()

if __name__ == '__main__':
    RemoveDuplicates().run()
