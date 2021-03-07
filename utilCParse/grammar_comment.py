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
	#+ pp.SkipTo(pp.lineEnd)
	#+ ...
	#+ parts.single_line_comment_end
	+ pp.restOfLine
)
multi_line_comment = (
	parts.multi_line_comment_begin
	+ ...
	+ parts.multi_line_comment_end
)

# 構文途中に出現するコメントのignore用
# 末尾をLineEndにマッチさせないことで、行末尾のコメントにはマッチさせない
comment_parser = pp.Group(
	(single_line_comment + (~pp.lineEnd.copy()))
#	| pp.cStyleComment
	| (multi_line_comment + (~pp.lineEnd.copy()))
)

any_comment_parser = pp.Group(
	single_line_comment
    #	| pp.cStyleComment
	| multi_line_comment
)

# 改行はマッチさせず１行内のコメントにマッチ
one_line_comment_parser = pp.Group(
	pp.Word(' \t')[...]
	+ (
		single_line_comment
	#	| pp.cStyleComment
		| multi_line_comment
	)
).leaveWhitespace()
