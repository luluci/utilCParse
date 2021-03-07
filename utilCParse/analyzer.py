from operator import truediv
from typing import List, Dict
import enum
import pyparsing as pp

class var_info:
	"""
	変数情報クラス
	"""

	def __init__(self) -> None:
		self.id: str = None
		self.type: type_info = None
		self.pointer = None
		self.comment: str = None


class type_info:
	"""
	型情報クラス
	"""
	class TAG(enum.Enum):
		base = enum.auto()
		struct = enum.auto()
		union = enum.auto()
		inner_struct = enum.auto()
		inner_union = enum.auto()

	def __init__(self) -> None:
		self.tag = None
		self.id = None
		self.comment = None
		# member情報
		self.member: Dict[str,var_info] = {}
		# 内部構造体定義情報
		self.inner_type: Dict[str, type_info] = {}

	def set_tag_struct(self):
		self.tag = type_info.TAG.struct

class analyzer:

	def __init__(self) -> None:
		# 単独出現コメント
		self._comment = None
		# 情報テーブル
		self.var_info_list: Dict[str, var_info] = {}
		self.type_info_list: Dict[str, type_info] = {}

	def add_var_info(self, item: var_info):
		self.var_info_list[item.id] = item

	def add_type_info(self, item: type_info) -> type_info:
		self.type_info_list[item.id] = item
		return self.type_info_list[item.id]

	def comment(self, loc: int, tokens: pp.ParseResults):
		self._comment = tokens[0][1]

	def external_declaration(self, loc: int, tokens: pp.ParseResults):
		# グローバル定義の開始
		# begin/endはempty()で実装してるので、次のtokenと同じlocになる
		# よって、locチェックしない
		print("external_declaration" + ":" + str(loc) + str(tokens))

		if 'external_decl' not in tokens.keys():
			# 構文構築上、external_declが存在しないのはありえない
			raise Exception("grammar is not preserve rule.")

		if 'typedef' in tokens.external_decl.keys():
			self.external_decl_typedef(loc, tokens.external_decl)
		elif 'struct_spec' in tokens.external_decl.keys():
			self.external_decl_struct(loc, tokens.external_decl)
		else:
			self.external_decl_var(loc, tokens.external_decl)
		# 事前コメントクリア
		self._comment = None

	def external_decl_typedef(self, loc: int, tokens: pp.ParseResults):
		pass

	def external_decl_struct(self, loc: int, tokens: pp.ParseResults):
		# tokensを解析して構造体情報を取得
		type_inf = self._get_type_info(tokens)
		# declaratorが存在するときは変数情報も登録
		if 'declarator_list' in tokens.keys():
			self._make_var_info(tokens, type_inf)

	def external_decl_var(self, loc: int, tokens: pp.ParseResults):
		# declaration-specifiers
		# 型情報取得
		type_inf = self._get_type_info(tokens)
		# 変数情報作成
		self._make_var_info(tokens, type_inf)



	def _make_var_info(self, tokens: pp.ParseResults, type_inf: type_info):
		# comment
		comment = None
		if 'comment' in tokens.keys():
			comment = self._get_comment(tokens.comment)
		# init-declarator-list
		for declarator in tokens.declarator_list:
			new_var = var_info()
			new_var.type = type_inf
			# pointerチェック
			if 'pointer' in declarator.declarator.keys():
				new_var.pointer = " ".join(declarator.pointer)
			# idチェック
			if 'id' not in declarator.declarator.keys():
				# 構文構築上、external_declが存在しないのはありえない
				raise Exception("grammar is not preserve rule.")
			new_var.id = declarator.declarator.id[0]
			# comment
			new_var.comment = comment
			# 追加
			self.add_var_info(new_var)

	def _make_type_info(self, tokens: pp.ParseResults) -> type_info:
		"""
		次の解析結果tokenを受け取る。
			-> external_decl, specifier_qualifier_list
		type_infoを作成して返す。
		"""

	def _get_type_info(self, tokens: pp.ParseResults) -> type_info:
		"""
		external_declを渡すこと。
		external_decl情報から型情報を取得して返す。
		(必要であれば専用のクラスを用意する)
		"""
		result = None
		if 'struct_spec' in tokens.keys():
			# struct_specが存在するとき、struct/union
			id = tokens.struct_spec.struct_id[0]
			# 型情報有無チェック
			tmp_inf = self._get_type_info_by_id(id)
			if tmp_inf is None:
				# 型情報作成
				tmp_inf = self._make_struct_info(tokens)
				#
				result = self.add_type_info(tmp_inf)
			else:
				# 存在するなら何もしない?
				result = tmp_inf

		elif 'decl_spec' in tokens.keys():
			# struct_specが存在せずdecl_specが存在するとき基本型
			pass
		else:
			# その他ケース?
			pass
		# 結果を返す
		return result

	def _get_type_info_by_id(self, id: str):
		if id in self.type_info_list.keys():
			return self.type_info_list[id]
		else:
			return None

	def _get_type_id(self, tokens: pp.ParseResults) -> str:
		"""
		external_declを渡すこと。
		external_decl情報から型情報を取得して返す。
		(必要であれば専用のクラスを用意する)
		"""
		result = None
		if 'struct_spec' in tokens.keys():
			result = tokens.struct_spec.struct_or_union + tokens.struct_spec.struct_id[0]
		else:
			result = " ".join(tokens.decl_spec)
		#
		return result

	def _make_struct_info(self, tokens: pp.ParseResults) -> type_info:
		# grammarチェック
		if 'struct_spec' not in tokens.keys():
			# 構文構築上、struct_specが存在しないのはありえない
			raise Exception("grammar is not preserve rule.")
		if 'struct_decl_list' not in tokens.struct_spec.keys():
			# struct_decl_list が存在しないときは変数宣言
			id = tokens.struct_spec.struct_id[0]
			inf = self._get_type_info(id)
			if inf is not None:
				inf.id = id
				inf.set_tag_struct()
			return inf
		# struct/union情報取得
		new_inf = type_info()
		if 'struct_id' in tokens.struct_spec.keys():
			new_inf.id = tokens.struct_spec.struct_id[0]
		else:
			new_inf.id = "<unnamed>"
		new_inf.struct_union = tokens.struct_spec.struct_or_union
		# comment取得
		comment = None
		if 'comment' in tokens.struct_spec.keys():
			comment = self._get_comment(tokens.struct_spec.comment)
		elif self._comment is not None:
			comment = self._comment
			self._comment = None
		new_inf.comment = comment
		# メンバ取得
		for decl in tokens.struct_spec.struct_decl_list:
			mem_inf = var_info()
			# identifier
			mem_inf.id = decl.id[0]
			# comment
			if 'comment' in decl.keys():
				comment = self._get_comment(decl.comment)
			elif 'comment_pre' in decl.keys():
				comment = self._get_comment(decl.comment_pre)
			# type-spec
			if 'struct_spec' in decl.specifier_qualifier_list.keys():
				# struct_specが存在するときは内部構造体定義
				inner = self._make_struct_info(decl.specifier_qualifier_list)
				new_inf.inner_type[inner.id] = inner
				# 型情報取得
				mem_inf.type = inner
			else:
				# 通常変数
				self._get_type_info_spec_qual_list(mem_inf, decl.specifier_qualifier_list)
			# member登録
			new_inf.member[mem_inf.id] = mem_inf
		# 終了
		return new_inf


	def _get_type_info_spec_qual_list(self, item: var_info, spec_qual_list: pp.ParseResults):
		# check
		if 'type_spec' not in spec_qual_list.keys():
			# 構文構築上、type_specが存在しないのはありえない
			raise Exception("grammar is not preserve rule.")
		# 型情報取得
		# type-qualifier
		# 未実装
		# type-specifier
		if 'struct_spec' in spec_qual_list.keys():
			# struct_specが存在するときは内部構造体定義
			# 上位でチェックする
			raise Exception("grammar is not preserve rule.")
		else:
			# 基本型のとき
			item.type = " ".join(spec_qual_list.type_spec)

	def _get_comment(self, comment: pp.ParseResults) -> str:
		"""
		'comment'tokenを渡すこと。
		コメントテキストを抽出して返す
		"""
		find = False
		for token in comment[0]:
			if find:
				return token.strip()
			if token in {'//', '/*'}:
				find = True
		return None



ev_hdler = analyzer()
