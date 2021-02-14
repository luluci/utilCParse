import pathlib

import utilCParse

"""
test = "if \\uFFFF\\UABCDABCDa_152 _hoge"

def get_str(match):
	print(match)


parser = token.keyword.if_ + token.identifier.setParseAction(get_str) + token.identifier.setParseAction(get_str)

ret = parser.parseString(test)
print(ret)
"""

if True:
	# file
#	path = pathlib.Path("./test/test_c_src/test1.c")
	path = pathlib.Path("./test/test_c_src/hed/test1.h")
	# parser
	parser = utilCParse.parser
	#parser = utilCParse.grammar.grammar_def.expression[1,...]

	# run
	text = ""
	with open(path, "r", encoding="utf-8") as fp:
		text = fp.read()

	ret = parser.parseString(text)
	print(ret)
