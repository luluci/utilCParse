from typing import List

class analyzer_:

	def __init__(self) -> None:
		pass

	def comment(self, loc, tokens: List[str]):
		print("comment" + ":" + str(loc) + str(tokens))

	def external_declaration_begin(self, loc, tokens: List[str]):
		# グローバル定義の開始
		print("external_declaration_begin" + ":" + str(loc) + str(tokens))

	def declaration_type(self, loc, tokens: List[str]):
		# グローバル定義の開始
		print("declaration_type" + ":" + str(loc) + str(tokens))

	def struct_begin(self, loc, tokens: List[str]):
		# 構造体宣言の開始
		print("struct_begin" + ":" + str(loc) + str(tokens))

	def struct_name(self, tokens: List[str]):
		print("struct_name" + str(tokens))

	def struct_declare_begin(self, tokens: List[str]):
		print("struct_declare_begin" + str(tokens))

	def struct_declare_member_begin(self, tokens: List[str]):
		print("struct_declare_member_begin" + str(tokens))

	def struct_declare_member_type(self, tokens: List[str]):
		print("struct_declare_member_type" + str(tokens))

	def struct_declare_member_name(self, tokens: List[str]):
		print("struct_declare_member_name" + str(tokens))

	def struct_declare_member_bit(self, tokens: List[str]):
		print("struct_declare_member_bit" + str(tokens))

	def struct_declare_member_end(self, tokens: List[str]):
		print("struct_declare_member_end" + str(tokens))

	def struct_declare_end(self, tokens: List[str]):
		print("struct_declare_end" + str(tokens))

	def struct_end(self, tokens: List[str]):
		print("struct_end" + str(tokens))

	def typedef_begin(self, loc, tokens: List[str]):
		print("typedef_begin" + ":" + str(loc) + str(tokens))

	def global_var_name(self, loc, tokens: List[str]):
		# 構造体宣言の開始
		print("global_var_name" + ":" + str(loc) + str(tokens))

	def global_var_init(self, loc, tokens: List[str]):
		# 構造体宣言の開始
		print("global_var_init" + ":" + str(loc) + str(tokens))

	def external_declaration_end(self, loc, tokens: List[str]):
		# グローバル定義の開始
		print("external_declaration_end" + ":" + str(loc) + str(tokens))


analyzer = analyzer_()
