#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import re
import sys

def main():
	if len(sys.argv) < 2:
		print 'Usage: inkludr.py <files>'
		sys.exit(1)

	for fileName in sys.argv[1:]:
		mapIncludes(fileName)

_include = re.compile('^\s*#\s*include\s*[<"]([a-zA-Z_-]+)[">]')

def mapIncludes(fileName):
	with open(fileName) as source:
		for line in source:
			header = _include.match(line)
			if header:
				print 'includes', header.group(1)
