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
	# struct宣言
	ext_decl_struct_begin = enum.auto()
	struct_name = enum.auto()
	#struct_end = enum.auto() 			# 無い
	strcut_decl_begin = enum.auto()
	strcut_decl_mem_begin = enum.auto()
	strcut_decl_mem_type = enum.auto()
	strcut_decl_mem_id = enum.auto()
	strcut_decl_mem_end = enum.auto()
	strcut_decl_end = enum.auto()
	# 特殊
	event_else = enum.auto()


class state_tag(enum.Enum):
	ini = enum.auto()
	ext_decl = enum.auto()
	ext_decl_var = enum.auto()
	ext_decl_struct = enum.auto()
	ext_decl_struct_mem_block = enum.auto()
	decl_struct_mem = enum.auto()
	# 特殊
	analyze_continue = enum.auto()
	analyze_end = enum.auto()


class event_handler:

	def __init__(self) -> None:
		self._analyzer = analyzer()

	def comment(self, loc: int, tokens: pp.ParseResults):
		# コメントは同じtokenが2回出現するのでlocチェックしない
		self._analyzer.event(event_tag.comment, None, tokens)
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
		# 
		print("global_var_init" + ":" + str(loc) + str(tokens))

	def struct_begin(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言の開始
		self._analyzer.event(event_tag.ext_decl_struct_begin, loc, tokens)
		print("struct_begin" + ":" + str(loc) + str(tokens))

	def struct_name(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言:名称
		self._analyzer.event(event_tag.struct_name, loc, tokens)
		print("struct_name" + ":" + str(loc) + str(tokens))

	def struct_declare_begin(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言:メンバー宣言ブロック開始
		self._analyzer.event(event_tag.strcut_decl_begin, loc, tokens)
		print("struct_declare_begin" + ":" + str(loc) + str(tokens))

	def struct_declare_member_begin(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言:メンバー宣言開始
		self._analyzer.event(event_tag.strcut_decl_mem_begin, loc, tokens)
		print("struct_declare_member_begin" + ":" + str(loc) + str(tokens))

	def struct_declare_member_type(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言:メンバー宣言:型
		self._analyzer.event(event_tag.strcut_decl_mem_type, loc, tokens)
		print("struct_declare_member_type" + ":" + str(loc) + str(tokens))

	def struct_declare_member_name(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言:メンバー宣言:名称
		self._analyzer.event(event_tag.strcut_decl_mem_id, loc, tokens)
		print("struct_declare_member_name" + ":" + str(loc) + str(tokens))

	def struct_declare_member_bit(self, loc: int, tokens: pp.ParseResults):
		print("struct_declare_member_bit" + ":" + str(loc) + str(tokens))

	def struct_declare_member_end(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言:メンバー宣言終了
		self._analyzer.event(event_tag.strcut_decl_mem_end, loc, tokens)
		print("struct_declare_member_end" + ":" + str(loc) + str(tokens))

	def struct_declare_end(self, loc: int, tokens: pp.ParseResults):
		# 構造体宣言:メンバー宣言ブロック終了
		self._analyzer.event(event_tag.strcut_decl_end, loc, tokens)
		print("struct_declare_end" + ":" + str(loc) + str(tokens))

	def struct_end(self, loc: int, tokens: pp.ParseResults):
		print("struct_end" + ":" + str(loc) + str(tokens))


class decl_info:
	class TAG(enum.Enum):
		var = enum.auto()
		struct = enum.auto()

	def __init__(self) -> None:
		self.tag = None
		self.name = None
		self.comment = None
		self.member = []

class analyzer:
	class temp_decl_info:
		def __init__(self) -> None:
			# 解析取得情報初期化
			self.tag = None
			self.type = None
			self.id = []
			self.comment = None
			self.member = []
			self.member_ptr = None

	def __init__(self) -> None:
		self._decl_info: Dict[str, decl_info] = {}
		# FollowedByでもparseActionが実行されるので、
		# locを元に解析済みを判定する。
		self._loc = -1
		self._comment = None
		# 解析中変数情報
		self._temp_decl_info = None
		#
		self._trans_tbl = {}
		self._trans_tbl[state_tag.ini] = {}
		self._trans_tbl[state_tag.ext_decl] = {}
		self._trans_tbl[state_tag.ext_decl_var] = {}
		self._trans_tbl[state_tag.ext_decl_struct] = {}
		self._trans_tbl[state_tag.ext_decl_struct_mem_block] = {}
		self._trans_tbl[state_tag.decl_struct_mem] = {}
		# 状態遷移テーブル:初期状態
		self._trans_tbl[state_tag.ini] = {
			event_tag.comment: (
				self.action_pre_comment,
				state_tag.analyze_continue
			),
			event_tag.ext_decl_begin: (
				self.action_decl_begin,
				state_tag.ext_decl
			),
		}
		# 状態遷移テーブル:グローバル宣言
		self._trans_tbl[state_tag.ext_decl].update({
			event_tag.ext_decl_type: (
				self.action_decl_type,
				state_tag.ext_decl_var
			),
			event_tag.ext_decl_struct_begin: (
				self.action_struct_begin,
				state_tag.ext_decl_struct
			),
			event_tag.event_else: (
				None,
				state_tag.analyze_end
			),
		})
		# 状態遷移テーブル:グローバル宣言:変数
		self._trans_tbl[state_tag.ext_decl_var].update({
			event_tag.ext_decl_id: (
				self.action_decl_id,
				state_tag.analyze_continue
			),
			event_tag.comment: (
				self.action_post_comment,
				state_tag.analyze_continue
			),
			event_tag.ext_decl_end: (
				self.action_decl_end,
				state_tag.analyze_end
			),
		})
		# 状態遷移テーブル:グローバル宣言:struct定義
		# 'struct <id>' まで
		self._trans_tbl[state_tag.ext_decl_struct].update({
			event_tag.struct_name: (
				self.action_struct_id,
				state_tag.analyze_continue
			),
			event_tag.comment: (
				None,
				state_tag.analyze_continue
			),
			event_tag.strcut_decl_begin: (
				self.action_decl_struct_begin,
				state_tag.ext_decl_struct_mem_block
			),
			event_tag.event_else: (
				self.action_struct_end,
				state_tag.analyze_end
			),
		})
		# メンバー宣言ブロック部
		self._trans_tbl[state_tag.ext_decl_struct_mem_block].update({
			event_tag.strcut_decl_mem_begin: (
				self.action_struct_decl_member_begin,
				state_tag.decl_struct_mem
			),
			event_tag.strcut_decl_end: (
				self.action_decl_end,
				None
			)
		})
		# メンバー宣言部
		self._trans_tbl[state_tag.decl_struct_mem].update({
			event_tag.strcut_decl_mem_type: (
				self.action_struct_decl_member_type,
				state_tag.analyze_continue
			),
			event_tag.strcut_decl_mem_id: (
				self.action_struct_decl_member_id,
				state_tag.analyze_continue
			),
			event_tag.comment: (
				self.action_post_comment,
				state_tag.analyze_continue
			),
			event_tag.strcut_decl_mem_end: (
				self.action_struct_decl_member_end,
				state_tag.analyze_end
			)
		})
		# デフォルト状態遷移テーブルを設定
		self._trans_tbl_stack = []
		self._trans_tbl_stack.append(self._trans_tbl[state_tag.ini])

	def _push_trans_tbl(self, new_tbl):
		"""
		解析状態コンテキスト遷移
		"""
		self._trans_tbl_stack.append(new_tbl)

	def _pop_trans_tbl(self):
		"""
		解析状態コンテキスト復帰
		"""
		# 状態遷移テーブルスタックから1つpopしてコンテキスト復帰
		self._trans_tbl_stack.pop()

	def _get_trans_tbl(self, event: event_tag):
		tbl_ptr = self._trans_tbl_stack[-1]
		if event in tbl_ptr.keys():
			return event, self._trans_tbl_stack[-1][event]
		elif event_tag.event_else in tbl_ptr.keys():
			return event_tag.event_else, self._trans_tbl_stack[-1][event_tag.event_else]
		else:
			return None

	def _check_loc(self, loc: int) -> int:
		next_loc = None
		if loc is None:
			# Noneの場合はチェック無効、locも進めない
			pass
		else:
			if self._loc < loc:
				# locが新しければチェック有効
				next_loc = loc
		return next_loc


	def event(self, event: event_tag, loc: int, tokens: pp.ParseResults):
		# locチェック
		next_loc = self._check_loc(loc)
		if next_loc:
			# eventが登録されていれば受理して処理する
			result = self._get_trans_tbl(event)
			if result:
				ev, act, next_state = result
				# action実行
				if act is not None:
					act(tokens)
				# 状態遷移実施
				if next_state is not None:
					self.event_trans(next_state)
				# 特殊イベントチェック
				if ev == event_tag.event_else:
					# else
					# ここまででelseイベントを実施、
					# 発生したイベント自体は未処理なので再帰的に実行する
					self.event(event, loc, tokens)
				# location更新
				# 一応、受理したときだけ更新
				# 同じtokenのイベントハンドラが2回発生することがある
				self._loc = next_loc
		else:
			# 解析済みlocの場合は無視する
			pass

	def event_trans(self, tag: state_tag):
		if tag == state_tag.analyze_continue:
			# 現状態継続
			pass
		elif tag == state_tag.analyze_end:
			# 前状態復帰
			self._pop_trans_tbl()
		else:
			self._push_trans_tbl(self._trans_tbl[tag])

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

	def action_decl_begin(self, tokens: pp.ParseResults):
		# 宣言開始
		self._temp_decl_info = analyzer.temp_decl_info()

	def action_decl_type(self, tokens: pp.ParseResults):
		# 変数宣言開始
		# 宣言タイプ設定
		self._temp_decl_info.tag = decl_info.TAG.var
		# type情報作成
		temp = ""
		for token in tokens:
			if type(token) == str:
				temp += token + " "
			else:
				temp += " ".join(token) + " "
		# type情報設定
		self._temp_decl_info.type = temp.strip()

	def action_decl_id(self, tokens: pp.ParseResults):
		id = tokens["id"][0]
		self._temp_id.append(id)
		# identifier設定
		self._temp_decl_info.id.append(id)

	def action_decl_end(self, tokens: pp.ParseResults):
		# 変数情報登録
		for name in self._temp_id:
			# 情報作成
			new_info = decl_info()
			new_info.tag = self._temp_tag
			new_info.name = name
			new_info.comment = self._comment
			# 情報登録
			if name not in self._decl_info.keys():
				self._decl_info[name] = new_info


	def action_struct_begin(self, tokens: pp.ParseResults):
		# struct宣言
		self._temp_tag = decl_info.TAG.struct

	def action_struct_end(self, tokens: pp.ParseResults):
		# else(external_declaration_end)で遷移する前提
		# external_declaration_endは上位で受理するので、再帰的にイベント処理を実施
		# コンテキスト復帰
		self._pop_trans_tbl()
		self.event()

	def action_struct_id(self, tokens: pp.ParseResults):
		# struct id
		id = tokens["id"][0]
		self._temp_id.append(id)

	def action_decl_struct_begin(self, tokens: pp.ParseResults):
		# struct member宣言開始
		self._temp_member_ptr = self._temp_member

	def action_struct_decl_begin(self, tokens: pp.ParseResults):
		# コンテキストスイッチ：struct宣言
		self._push_trans_tbl(self._trans_tbl[state_tag.ext_decl_struct])
		self._temp_tag = decl_info.TAG.struct

	def action_struct_decl_member_begin(self, tokens: pp.ParseResults):
		# コンテキストスイッチ：変数宣言
		self._temp_tag = decl_info.TAG.var

	def action_struct_decl_member_type(self, tokens: pp.ParseResults):
		# コンテキストスイッチ：変数宣言
		self._temp_tag = decl_info.TAG.var

	def action_struct_decl_member_id(self, tokens: pp.ParseResults):
		# コンテキストスイッチ：変数宣言
		self._temp_tag = decl_info.TAG.var

	def action_struct_decl_member_end(self, tokens: pp.ParseResults):
		# コンテキストスイッチ：変数宣言
		self._temp_tag = decl_info.TAG.var


ev_hdler = event_handler()
