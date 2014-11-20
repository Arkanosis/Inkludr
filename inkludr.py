#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

_version = '0.1'
_include = re.compile(r'^\s*?\#\s*?include\s*[<"](?P<path>[a-zA-Z0-9._-]+)[>"]')

def getIncludes(fileName):
	includes = []
	with open(fileName) as source:
		for line in source:
			include = _include.match(line)
			if include:
				includes.append(include.group('path'))
	return includes

def inferIncludesMap(includesMap):
	# TODO FIXME
	pass

def getIncludeMap(fileNames):
	includesMap = {}
	for fileName in fileNames:
		includes = getIncludes(fileName)
		if includes:
			includesMap[fileName] = includes
	inferIncludesMap(includesMap)
	return includesMap

def filterIncludesMap(includesMap, pattern):
	filteredMap = {}
	regexp = re.compile(pattern)
	for fileName, includes in includesMap.items():
		if regexp.search(fileName):
			filteredMap[fileName] = includes
	return filteredMap

if __name__ == '__main__':
	if len(sys.argv) < 2:
                print 'Inkludr v%s' % _version
		print 'Usage: inkludr.py <files>'
		sys.exit(1)

	includesMap = filterIncludesMap(getIncludeMap(sys.argv[1:]), r'\.cpp$')
	print includesMap
