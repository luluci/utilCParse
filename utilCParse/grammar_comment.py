import pyparsing as pp

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

