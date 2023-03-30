#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CLink:
    """
    manage the links in a line
    """

    def __init__(self):
        self.beginning_of_link = '<a '
        self.end_of_link = '</a>'
        self.beginning_of_url = 'href=\"'
        self.end_of_url = '\">'
        self.beginning_of_object = '<'
        self.end_of_object = '>'

    def replace_link_by_text(self, line):
        p_link = line.find(self.beginning_of_link)
        if p_link < 0: return line

        while p_link > -1:
            start = line.find(self.beginning_of_link)
            stop = line.find(self.end_of_link)

            before = line[:start]
            link = line[start+len(self.beginning_of_link):stop]
            text = self.extract_text(link)
            after = line[stop + len(self.end_of_link):]
            line = before + text + after
            p_link = line.find(self.beginning_of_link)

        return line

    def extract_text(self, link):
        text = None

        # url
        p = link.find(self.end_of_url)
        link = link[p+len(self.end_of_url):]
        text = link.strip()

        # the others
        p_object = text.find(self.beginning_of_object)
        while p_object > -1:
            if p_object > 0:
                text = text[0:p_object]
                text = text.strip()
                p_object = -1
            else:
                stop = text.find(self.end_of_object)
                text = text[stop+len(self.end_of_object):]
                text = text.strip()
            p_object = text.find(self.beginning_of_object)

        return text
