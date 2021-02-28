from typing import List, Dict
import enum
import pyparsing as pp


class event_tag(enum.Enum):
	# コメント
	comment = enum.auto()
	# グローバル変数宣言
	ext_decl_begin = enum.auto()
	ext_decl_end = enum.auto()
	ext_decl_type = enum.auto()
	ext_decl_id = enum.auto()


class state_tag(enum.Enum):
	ini = enum.auto()
	decl_var = enum.auto()
	decl_struct = enum.auto()



class event_handler:

	def __init__(self) -> None:
		self._analyzer = analyzer()

	def comment(self, loc: int, tokens: pp.ParseResults):
		self._analyzer.event(event_tag.comment, loc, tokens)
		print("comment" + ":" + str(loc) + str(tokens))

	def external_declaration_begin(self, loc: int, tokens: pp.ParseResults):
		# グローバル定義の開始
		# begin/endはempty()で実装してるので、次のtokenと同じlocになる
		# よって、locチェックしない
		self._analyzer.event(event_tag.ext_decl_begin, None, tokens)
		print("external_declaration_begin" + ":" + str(loc) + str(tokens))

	def external_declaration_end(self, loc: int, tokens: pp.ParseResults):
		# グローバル定義の終了
		# begin/endはempty()で実装してるので、次のtokenと同じlocになる
		# よって、locチェックしない
		self._analyzer.event(event_tag.ext_decl_end, None, tokens)
		print("external_declaration_end" + ":" + str(loc) + str(tokens))

	def declaration_type(self, loc: int, tokens: pp.ParseResults):
		# type-specifier
		self._analyzer.event(event_tag.ext_decl_type, loc, tokens)
		print("declaration_type" + ":" + str(loc) + str(tokens))

	def global_var_id(self, loc: int, tokens: pp.ParseResults):
		# identifier
		self._analyzer.event(event_tag.ext_decl_id, loc, tokens)
		print("global_var_name" + ":" + str(loc) + str(tokens))

	def typedef_begin(self, loc: int, tokens: pp.ParseResults):
		print("typedef_begin" + ":" + str(loc) + str(tokens))

	def global_var_init(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言の開始
		print("global_var_init" + ":" + str(loc) + str(tokens))

	def struct_begin(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言の開始
		print("struct_begin" + ":" + str(loc) + str(tokens))

	def struct_name(self, loc: int, tokens: pp.ParseResults):
		print("struct_name" + ":" + str(loc) + str(tokens))

	def struct_declare_begin(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_begin" + ":" + str(loc) + str(tokens))

	def struct_declare_member_begin(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_member_begin" + ":" + str(loc) + str(tokens))

	def struct_declare_member_type(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_member_type" + ":" + str(loc) + str(tokens))

	def struct_declare_member_name(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_member_name" + ":" + str(loc) + str(tokens))

	def struct_declare_member_bit(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_member_bit" + ":" + str(loc) + str(tokens))

	def struct_declare_member_end(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_member_end" + ":" + str(loc) + str(tokens))

	def struct_declare_end(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_end" + ":" + str(loc) + str(tokens))

	def struct_end(self, loc: int, tokens: pp.ParseResults):
		print("struct_end" + ":" + str(loc) + str(tokens))


class decl_info:
	def __init__(self) -> None:
		self.name = None
		self.comment = None
		self.member = []

class struct_info:
	def __init__(self) -> None:
		pass

class analyzer:
	def __init__(self) -> None:
		self._decl_info: Dict[str, decl_info] = {}
		# FollowedByでもparseActionが実行されるので、
		# locを元に解析済みを判定する。
		self._loc = -1
		self._comment = None
		#
		self._trans_tbl = {}
		self._trans_tbl[state_tag.ini] = {}
		self._trans_tbl[state_tag.decl_var] = {}
		# 状態遷移テーブル:初期状態
		self._trans_tbl[state_tag.ini] = {
			event_tag.comment: (
				self.action_pre_comment,
				None
			),
			event_tag.ext_decl_begin:(
				None,
				self._trans_tbl[state_tag.decl_var]
			)
		}
		# 状態遷移テーブル:グローバル宣言
		self._trans_tbl[state_tag.decl_var].update({
			event_tag.ext_decl_type: (
				self.action_decl_type,
				None
			),
			event_tag.ext_decl_id: (
				self.action_decl_id,
				None
			),
			event_tag.comment: (
				self.action_post_comment,
				None
			),
			event_tag.ext_decl_end: (
				self.action_decl_end,
				None
			)
		})
		self._init_trans()

	def _init_trans(self):
		"""
		解析状態を初期状態へ設定
		"""
		self._trans_tbl_ptr = self._trans_tbl[state_tag.ini]
		# 今回解析取得情報初期化
		self._temp_type = None
		self._temp_id = []
		self._comment = None

	def event(self, event: event_tag, loc: int, tokens: pp.ParseResults):
		# locチェック, Noneのケースあり
		loc_check = False
		next_loc = loc
		if loc is None:
			# Noneの場合はチェック無効、locも進めない
			loc_check = True
			next_loc = self._loc
		else:
			if self._loc < loc:
				loc_check = True
		if loc_check:
			# eventが登録されていない場合、初期状態へ戻る
			# 初期状態からの遷移を考慮して先に1度登録有無をチェックする
			if event not in self._trans_tbl_ptr.keys():
				self._init_trans()
			# eventが登録されていれば受理して処理する
			if event in self._trans_tbl_ptr.keys():
				act, tbl = self._trans_tbl_ptr[event]
				# action実行
				if act is not None:
					act(tokens)
				# 状態遷移チェック
				if tbl is None:
					# Noneのときは何もせず現状維持
					pass
				else:
					self._trans_tbl_ptr = tbl
				# location更新
				# 一応、受理したときだけ更新
				# 同じtokenのイベントハンドラが2回発生することがある
				self._loc = next_loc
		else:
			# 解析済みlocの場合は無視する
			pass

	def action_pre_comment(self, tokens: pp.ParseResults):
		"""
		単独で書いてあるコメント
		変数の手前とかに書いてあるやつのはず
		"""
		self._comment = tokens[0][1].strip()

	def action_post_comment(self, tokens: pp.ParseResults):
		"""
		変数の後ろに書いてあるコメント
		"""
		self._comment = tokens[0][1].strip()

	def action_decl_type(self, tokens: pp.ParseResults):
		temp = ""
		for token in tokens:
			if type(token) == str:
				temp += token + " "
			else:
				temp += " ".join(token) + " "
		self._temp_type = temp.strip()

	def action_decl_id(self, tokens: pp.ParseResults):
		id = tokens["id"][0]
		self._temp_id.append(id)

	def action_decl_end(self, tokens: pp.ParseResults):
		# 変数情報登録
		for name in self._temp_id:
			# 情報作成
			new_info = decl_info()
			new_info.name = name
			new_info.comment = self._comment
			# 情報登録
			if name not in self._decl_info.keys():
				self._decl_info[name] = new_info

		# 状態初期化
		self._init_trans()


ev_hdler = event_handler()
