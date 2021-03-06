#!/usr/bin/python
# -*- coding: latin-1 -*-

from HTMLParser import HTMLParser

class TableParser(HTMLParser):
    
    def __init__(self,type):
        HTMLParser.__init__(self)

        if type == 'savings':
            self.summary_count = 1
        elif type == 'current':
            self.summary_count = 2

        self.summary = 0
        self.finish = False
        self.recording = 0
        self.data = []
        self.line = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for name, value in attrs:
                if name == 'class' and value == 'summaryTable':
                    self.summary += 1

        if tag == 'td':
            if self.summary == self.summary_count:
                for name, value in attrs:
                    if name == 'class' and value == 'summaryDetailC':
                        self.recording = 1
                    if name == 'class' and value == 'summaryDetailL':
                        self.recording = 1
                    if name == 'class' and value == 'summaryDetailR':
                        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'td' and self.recording:
          self.recording = 0
        if tag == 'tr' and self.summary == self.summary_count and not self.finish:
          if len(self.line) == 6:
              self.line[2] = self.line[2].replace('\xa3','')
              self.line[3] = self.line[3].replace('\xa3','')
              self.line[4] = self.line[4].replace('\xa3','')
              self.line[5] = self.line[5].replace('\xa3','')
              self.data.append(self.line)
          self.line = []
        if tag == 'table' and self.summary == self.summary_count:
          self.finish = True

    def handle_data(self, data):
        if self.recording and not self.finish:
          self.line.append(data.strip())

