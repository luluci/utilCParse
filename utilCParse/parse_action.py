import pyparsing as pp
from collections.abc import Callable

class parse_action_handler:
	"""
	PyParsingのsetParseActionのコールバック関数定義クラス
	このクラスに対して上位クラスからコールバック関数を登録し、
	PyParsingからのactionを伝播する。
	"""
#	handler_t = Callable[[int, pp.ParseResults], None]

	def __init__(self) -> None:
		#self.hdl_comment: parse_action_handler.handler_t = None
		#self.hdl_external_declaration: parse_action_handler.handler_t = None
		self.hdl_comment = None
		self.hdl_external_declaration = None

	def comment(self, loc: int, tokens: pp.ParseResults):
		# コメント
		# 行内に単独で出現するコメント、または、tokenの間に出現するブロックコメントが該当する。
		# 何かしらの記載の後ろに出現するコメントは、それら記載の解析結果に含まれる。
		# print("comment" + ":" + str(loc) + str(tokens))
		if self.hdl_comment is not None:
			self.hdl_comment(loc, tokens)

	def external_declaration(self, loc: int, tokens: pp.ParseResults):
		# 外部宣言
		# print("external_declaration" + ":" + str(loc) + str(tokens))
		if self.hdl_external_declaration is not None:
			self.hdl_external_declaration(loc, tokens)

parse_action = parse_action_handler()
