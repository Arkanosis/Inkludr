#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

_version = '0.1'

_eom = r'\s*(?:(?://|/\*).*?)?$'

_ifndef = re.compile(r'^(?P<i1>\s*)\#(?P<i2>\s*)ifndef\s*(?P<guard>[a-zA-Z0-9_]+)' + _eom)
_define = re.compile(r'^\s*\#\s*define\s*(?P<guard>[a-zA-Z0-9_]+)' + _eom)
_endif = re.compile(r'^\s*\#\s*endif' + _eom)
_anyif = re.compile(r'^\s*\#\s*if')
_else = re.compile(r'^\s*\#\s*else')

def matchOn(string):
	_match = [None]
	def on(reg):
		_match[0] = reg.match(string)
		return _match[0]
	def _(group):
		return _match[0].group(group)
	return on, _

def checkGuards(fileName):

	source = ''

	with open(fileName) as sourceFile:

		depth = 0
		guard = None
		guardDepth = -1
		guardIndent = 0
		cachedLine = ''

		for line in sourceFile:
			on, _ = matchOn(line)

			if on(_ifndef):
				depth += 1
				guard = _('guard')
				guardIndent = max(_('i1'), _('i2'))
				cachedLine = line
				continue

			elif on(_define):
				if _('guard') == guard:
					if guardDepth != -1:
						# TODO we may suppose that if a #else of a #endif comes right after it, it's not a guard
						print '%s: error: not sure which macro is the guard, aborting' % fileName
						sys.exit(3)
					if guardIndent:
						print '%s: warning: guard "%s" was indented, maybe a false positive?' % guard
					guardDepth = depth

					standardGuard = fileName.replace('/', '_').replace('.', '_').upper()

					if standardGuard != guard:
						print '%s: %s → %s' % (fileName, guard, standardGuard)
						guard = standardGuard

					source += '#ifndef %s\n' % guard
					source += '# define %s\n' % guard
					guard = None
					continue

			elif on(_endif):
				if depth == guardDepth:
					source += '#endif // !%s\n' % standardGuard
					depth -= 1
					continue
				depth -= 1

			elif on(_anyif):
				depth += 1

			if guard:
				source += cachedLine

			guard = None
			source += line

		if depth:
			print '%s: error: unbalanced #if / #endif, aborting' % fileName
			sys.exit(2)

	with open(fileName, 'w') as sourceFile:
		sourceFile.write(source)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: guardian.py <file>'
		sys.exit(1)

	checkGuards(sys.argv[1])
