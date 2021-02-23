import pyparsing as pp
from . import token
from . import grammar
from . import grammar_comment
from . import grammar_pp
from . import analyzer

parser = pp.OneOrMore(
	grammar.parser
	| grammar_pp.pp_parser
)
#parser = grammar.grammar_def.declaration[1,...]

"""
parser.ignore(
	grammar_comment.comment_parser
)
"""

"""
	pp.Group(
		grammar_comment.single_line_comment
#		| pp.cStyleComment
		| grammar_comment.multi_line_comment
	).setParseAction(analyzer.ev_hdler.comment)
"""
