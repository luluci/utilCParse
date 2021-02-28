import pyparsing as pp
from . import analyzer as analyzer_mod

ev_hdler = analyzer_mod.ev_hdler

class grammar_comment_def:
	single_line_comment_begin = pp.Literal("//")
	single_line_comment_end = pp.LineEnd()
	multi_line_comment_begin = pp.Literal("/*")
	multi_line_comment_end = pp.Literal("*/")

parts = grammar_comment_def
single_line_comment = (
	parts.single_line_comment_begin
	#+ pp.SkipTo(pp.LineEnd())
	#+ ...
	#+ parts.single_line_comment_end
	+ pp.restOfLine
)
multi_line_comment = (
	parts.multi_line_comment_begin
	+ ...
	+ parts.multi_line_comment_end
)


comment_parser = pp.Group(
	single_line_comment
#	| pp.cStyleComment
	| multi_line_comment
).setParseAction(ev_hdler.comment)

one_line_comment_parser = pp.Group(
	pp.Word(' \t')[...]
	+ (
		single_line_comment
	#	| pp.cStyleComment
		| multi_line_comment
	)
).leaveWhitespace().setParseAction(ev_hdler.comment)
