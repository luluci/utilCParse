from typing import List, Dict
import enum
import pathlib
import pyparsing as pp
from . import parse_action
from . import grammar
from . import grammar_pp

# PyParsing parseActionHandler管理クラス インスタンス
act_hdler = parse_action.parse_action
# parser
parser = pp.OneOrMore(
	grammar.parser
	| grammar_pp.pp_parser
)

class var_info:
	"""
	変数情報クラス
	"""

	def __init__(self) -> None:
		self.id: str = None
		self.type: type_info = None
		self.pointer = None
		self.comment: str = None
		# 解析元ファイル情報
		self.dir_path: pathlib.Path = None
		self.file_path: pathlib.Path = None


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
		# 解析元ファイル情報
		self.dir_path: pathlib.Path = None
		self.file_path: pathlib.Path = None

	def set_tag_base(self):
		self.tag = type_info.TAG.base

	def set_tag_struct(self):
		self.tag = type_info.TAG.struct

	def set_tag_union(self):
		self.tag = type_info.TAG.union

	def set_struct_or_union(self, struct_union: str):
		if struct_union == 'struct':
			self.set_tag_struct()
		elif struct_union == 'union':
			self.set_tag_union()

class analyzer:

	def __init__(self) -> None:
		# 単独出現コメント
		self._comment = None
		# 情報テーブル
		# [id / filepath / *_info] の階層で構築する
		self.var_info_list: Dict[str, Dict[str, var_info]] = {}
		self.type_info_list: Dict[str, Dict[str, type_info]] = {}
		# ハンドラ初期化
		self._init_hanlder()

	def _init_hanlder(self):
		# ハンドラ登録
		act_hdler.hdl_comment = self._hdl_comment
		act_hdler.hdl_external_declaration = self._hdl_external_declaration


	def analyze_dir(self, dir_path: pathlib.Path, glob:str = '**/*', encoding:str = 'utf-8'):
		self._dir_path = dir_path
		# フォルダ探索
		for path in dir_path.glob(glob):
			if path.is_file():
				# 相対パスでファイルパス情報を作成
				self._file_path_rel = path.relative_to(self._dir_path)
				# ファイルからテキスト取得
				text = ""
				with open(path, "r", encoding=encoding) as fp:
					text = fp.read()
				# テキスト解析
				ret = parser.parseString(text)
				print(ret)

	def _add_var_info(self, item: var_info):
		# ファイル情報追記
		item.dir_path = self._dir_path
		item.file_path = self._file_path_rel
		# 
		if item.id not in self.var_info_list.keys():
			self.var_info_list[item.id] = {}
		self.var_info_list[item.id][str(item.file_path)] = item

	def _add_type_info(self, item: type_info) -> type_info:
		# ファイル情報追記
		item.dir_path = self._dir_path
		item.file_path = self._file_path_rel
		#
		if item.id not in self.type_info_list.keys():
			self.type_info_list[item.id] = {}
		self.type_info_list[item.id][str(item.file_path)] = item
		return self.type_info_list[item.id][str(item.file_path)]

	def _hdl_comment(self, loc: int, tokens: pp.ParseResults):
		self._comment = tokens[0][1]

	def _hdl_external_declaration(self, loc: int, tokens: pp.ParseResults):
		# グローバル定義の開始
		# begin/endはempty()で実装してるので、次のtokenと同じlocになる
		# よって、locチェックしない
		print("external_declaration" + ":" + str(loc) + str(tokens))

		if 'external_decl' not in tokens.keys():
			# 構文構築上、external_declが存在しないのはありえない
			raise Exception("grammar is not preserve rule.")

		if 'typedef' in tokens.external_decl.keys():
			self._analyze_external_decl_typedef(loc, tokens.external_decl)
		elif 'struct_spec' in tokens.external_decl.keys():
			self._analyze_external_decl_struct(loc, tokens.external_decl)
		else:
			self._analyze_external_decl_var(loc, tokens.external_decl)
		# 事前コメントクリア
		self._comment = None

	def _analyze_external_decl_typedef(self, loc: int, tokens: pp.ParseResults):
		pass

	def _analyze_external_decl_struct(self, loc: int, tokens: pp.ParseResults):
		# tokensを解析して構造体情報を取得
		type_inf = self._get_type_info(tokens)
		# declaratorが存在するときは変数情報も登録
		if 'declarator_list' in tokens.keys():
			self._make_var_info(tokens, type_inf)

	def _analyze_external_decl_var(self, loc: int, tokens: pp.ParseResults):
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
			self._add_var_info(new_var)

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
				result = self._add_type_info(tmp_inf)
			else:
				# 存在するなら何もしない?
				result = tmp_inf

		elif 'decl_spec' in tokens.keys():
			# struct_specが存在せずdecl_specが存在するとき基本型
			id = " ".join(tokens.decl_spec)
			# 型情報有無チェック
			tmp_inf = self._get_type_info_by_id(id)
			if tmp_inf is None:
				# 型情報作成
				tmp_inf = self._make_base_type_info(tokens)
				#
				result = self._add_type_info(tmp_inf)
			else:
				# 存在するなら何もしない?
				result = tmp_inf
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

	def _make_base_type_info(self, tokens: pp.ParseResults) -> type_info:
		new_inf = type_info()
		# tag
		new_inf.set_tag_base()
		# id
		id = " ".join(tokens.decl_spec)
		new_inf.id = id
		#
		return new_inf

	def _make_struct_info_incomplete(self, tokens: pp.ParseResults, prefix: str = "") -> type_info:
		"""
		不完全型
		"""
		type_inf = type_info()
		#
		id = tokens.struct_spec.struct_id[0]
		type_inf.id = prefix + id
		#
		struct_union = tokens.struct_spec.struct_or_union
		type_inf.set_struct_or_union(struct_union)
		#
		return type_inf

	def _make_struct_info(self, tokens: pp.ParseResults, prefix:str = "", unnamed_cnt:int = 0) -> type_info:
		# grammarチェック
		if 'struct_spec' not in tokens.keys():
			# 構文構築上、struct_specが存在しないのはありえない
			raise Exception("grammar is not preserve rule.")
		if 'struct_decl_list' not in tokens.struct_spec.keys():
			# 不完全型のときにこのパスにくる
			# struct_decl_list が存在しないときは変数宣言
			inf = self._make_struct_info_incomplete(tokens, prefix)
			return inf
		# struct/union情報取得
		new_inf = type_info()
		# tag
		new_inf.set_struct_or_union(tokens.struct_spec.struct_or_union)
		# id 
		if 'struct_id' in tokens.struct_spec.keys():
			new_inf.id = prefix + tokens.struct_spec.struct_id[0]
		else:
			new_inf.id = prefix + "unnamed_" + str(unnamed_cnt)
			unnamed_cnt += 1
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
				inner = self._make_struct_info(decl.specifier_qualifier_list, new_inf.id+"@", unnamed_cnt)
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
