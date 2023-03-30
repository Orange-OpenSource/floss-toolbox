#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CHtmlTag:

    def delete_the_blocks(self, line):
        p_begin = line.find('<')
        if p_begin == -1: return line

        while p_begin > -1:
            r = self.extract_text_before_tag(line)
            if r == None:
                return line
            before, after = r

            after = self.delete_tag(after)

            line = before + after
            p_begin = line.find('<')

        return line

    def extract_text_before_tag(self, line):
        p_begin = line.find('<')
        if p_begin < 0:
            return None

        before = str()
        after = str()
        if p_begin == 0:
            after = line
        else:
            # p_begin > 0
            before = line[0:p_begin]
            after = line[p_begin:]

        return (before, after)

    def delete_tag(self, line):
        p_end = line.find('>')
        if p_end < 0:
            return str()

        # delete the tags in this tag
        line = line[1:]
        p_end = p_end -1
        p_begin = line.find('<')
        while (p_begin > -1) and (p_begin < p_end):
            line = line[p_end +1:]
            p_begin = line.find('<')
            p_end = line.find('>')

        after = str()
        last_indice = len(line) -1
        if p_end < last_indice:
            after = line[p_end +1:]

        after = after.strip()
        return after
