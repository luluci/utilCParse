"""

"""
import enum
import pyparsing as pp
from . import token
from . import grammar_pp
from . import grammar_comment
from . import parse_action
pp.ParserElement.enablePackrat()

act_hdler = parse_action.parse_action

# .copy().setParseAction(parse_debug)
# + pp.Empty().setParseAction(parse_debug)
def parse_debug(loc, var):
	print("debug:" + str(loc) + "," + str(var))

# マッチしなかったらトークンを読み捨てて次へ行く。
# 読み捨て分をエラーとして出力しておく。
def parse_debug_unknown_token(loc, var):
	print("[parse error]:" + str(loc) + "," + str(var))

class grammar_def:

	# Forward定義
	expression = pp.Forward()
	assignment_expression = pp.Forward()
	type_name = pp.Forward()
	initializer_list = pp.Forward()
	cast_expression = pp.Forward()

	# (6.5.2) argument-expression-list:
	argument_expression_list = (
		assignment_expression
		+ pp.ZeroOrMore(
			token.punctuator.comma
			+ assignment_expression
		)
	)

	# (6.5.1) primary-expression:
	primary_expression = (
		token.identifier
		| token.constant
		| token.string_literal
		| (token.punctuator.left_paren + expression + token.punctuator.right_paren)
	)
	# (6.5.2) postfix-expression:
	postfix_expression_1 = (
		token.punctuator.left_bracket
		+ expression
		+ token.punctuator.right_bracket
	)
	postfix_expression_2 = (
		token.punctuator.left_paren
		+ argument_expression_list
		+ token.punctuator.right_paren
	)
	postfix_expression_3 = (
		(token.punctuator.dot | token.punctuator.arrow_op)
		+ token.identifier
	)
	postfix_expression_4 = (
		postfix_expression_1
		| postfix_expression_2
		| postfix_expression_3
		| token.punctuator.increment_op
		| token.punctuator.decrement_op
	)
	# ( type-name ) { init-list } はcast-expressionで解析する
	postfix_expression_5 = (
		token.punctuator.left_paren
		+ type_name
		+ token.punctuator.right_paren
		+ token.punctuator.left_brace
		+ initializer_list
		+ pp.Optional(token.punctuator.comma)
		+ token.punctuator.right_bracket
	)
	postfix_expression = pp.Forward()
	postfix_expression <<= (
		(primary_expression + pp.ZeroOrMore(postfix_expression_4))
		| postfix_expression_5
	)
	# (6.5.3) unary-operator: one of
	unary_operator = (
		token.punctuator.ampersand
		| token.punctuator.asterisk
		| token.punctuator.plus
		| token.punctuator.minus
		| token.punctuator.bitwise_complement_op
		| token.punctuator.logical_negation_op
	)
	# (6.5.3) unary-expression:
	unary_expression = pp.Forward()
	unary_expression_1 = (
		token.keyword.sizeof_ + (
			unary_expression
			| (
				token.punctuator.left_paren
				+ type_name
				+ token.punctuator.right_paren
			)
		)
	)
	unary_expression <<= (
		postfix_expression
		| (token.punctuator.increment_op + unary_expression)
		| (token.punctuator.decrement_op + unary_expression)
		| (unary_operator + cast_expression)
		| unary_expression_1
	)
	# (6.5.4) cast-expression:
	# "( identifier )" のケースのみgrammarが区別できない
	# ケース：postfix-expression: ( type-name ) { initializer-list }
	cast_expression_1 = (
		pp.FollowedBy(
			token.punctuator.left_paren
			+ token.identifier
			+ token.punctuator.right_paren
			+ token.punctuator.left_brace
		)
		+ token.punctuator.left_paren
		+ token.identifier
		+ token.punctuator.right_paren
		+ token.punctuator.left_brace
		+ initializer_list
		+ pp.Optional(token.punctuator.comma)
		+ token.punctuator.right_bracket
	)
	cast_expression_2 = (
		pp.FollowedBy(
			token.punctuator.left_paren
			+ token.identifier
			+ token.punctuator.right_paren
			+ cast_expression
		)
		+ token.punctuator.left_paren
		+ token.identifier
		+ token.punctuator.right_paren
		+ cast_expression
	)
	cast_expression_3 = (
		pp.FollowedBy(
			token.punctuator.left_paren
			+ type_name
			+ token.punctuator.right_paren
			+ cast_expression
		)
		+ token.punctuator.left_paren
		+ type_name
		+ token.punctuator.right_paren
		+ cast_expression
	)
	cast_expression <<= (
		cast_expression_1
		| cast_expression_2
		| cast_expression_3
		| unary_expression
	)
	# (6.5.5) multiplicative-expression:
	multiplicative_expression = pp.Forward()
	multiplicative_expression <<= (
		cast_expression
		+ pp.Optional(
			(
				token.punctuator.asterisk
				| token.punctuator.div_op
				| token.punctuator.remain_op
			)
			+ cast_expression
		)
	)
	# (6.5.6) additive-expression:
	additive_expression = pp.Forward()
	additive_expression <<= (
		multiplicative_expression
		+ pp.Optional(
			(
				token.punctuator.plus
				| token.punctuator.minus
			)
			+ multiplicative_expression
		)
	)
	# (6.5.7) shift-expression:
	shift_expression = pp.Forward()
	shift_expression <<= (
		additive_expression
		+ pp.Optional(
			(
				token.punctuator.left_shift_op
				| token.punctuator.right_shift_op
			)
			+ additive_expression
		)
	)
	# (6.5.8) relational-expression:
	relational_expression = pp.Forward()
	relational_expression <<= (
		shift_expression
		+ pp.Optional(
			(
				token.punctuator.lt_op
				| token.punctuator.gt_op
				| token.punctuator.lte_op
				| token.punctuator.gte_op
			)
			+ shift_expression
		)
	)
	# (6.5.9) equality-expression:
	equality_expression = pp.Forward()
	equality_expression <<= (
		relational_expression
		+ pp.Optional(
			(
				token.punctuator.equal_op
				| token.punctuator.inequal_op
			)
			+ relational_expression
		)
	)
	# (6.5.10) AND-expression:
	AND_expression = pp.Forward()
	AND_expression <<= (
		equality_expression
		+ pp.Optional(
			token.punctuator.ampersand
			+ equality_expression
		)
	)
	# (6.5.11) exclusive-OR-expression:
	exclusive_OR_expression = pp.Forward()
	exclusive_OR_expression <<= (
		AND_expression
		+ pp.Optional(
			token.punctuator.bitwise_EXOR_op
			+ AND_expression
		)
	)
	# (6.5.12) inclusive-OR-expression:
	inclusive_OR_expression = pp.Forward()
	inclusive_OR_expression <<= (
		exclusive_OR_expression
		+ pp.Optional(
			token.punctuator.bitwise_OR_op
			+ exclusive_OR_expression
		)
	)
	# (6.5.13) logical-AND-expression:
	logical_AND_expression = pp.Forward()
	logical_AND_expression <<= (
		inclusive_OR_expression
		+ pp.Optional(
			token.punctuator.logical_AND_op
			+ inclusive_OR_expression
		)
	)
	# (6.5.14) logical-OR-expression:
	logical_OR_expression = pp.Forward()
	logical_OR_expression <<= (
		logical_AND_expression
		+ pp.Optional(
			token.punctuator.logical_OR_op
			+ logical_AND_expression
		)
	)
	# (6.5.15) conditional-expression:
	conditional_expression = pp.Forward()
	conditional_expression <<= (
		logical_OR_expression
		+ pp.Optional(
			token.punctuator.conditional_op
			+ expression
			+ token.punctuator.colon
			+ conditional_expression
		)
	)
	# (6.5.16) assignment-operator: one of
	assignment_operator = (
		token.punctuator.simple_assign_op
		| token.punctuator.mul_assign_op
		| token.punctuator.div_assign_op
		| token.punctuator.remain_assign_op
		| token.punctuator.add_assign_op
		| token.punctuator.sub_assign_op
		| token.punctuator.left_shift_assign_op
		| token.punctuator.right_shift_assign_op
		| token.punctuator.bitwise_AND_assign_op
		| token.punctuator.bitwise_EXOR_assign_op
		| token.punctuator.bitwise_OR_assign_op
	)
	# (6.5.16) assignment-expression:
	assignment_expression = pp.Forward()
	assignment_expression <<= (
		conditional_expression
		| (unary_expression + assignment_operator + assignment_expression)
	)
	# (6.5.17) expression:
	expression <<= (
		assignment_expression
		+ pp.Optional(
			token.punctuator.comma
			+ assignment_expression
		)
	)
	# (6.6) constant-expression:
	constant_expression = conditional_expression







	# (6.7.3) type-qualifier:
	type_qualifier = (
		token.keyword.const_
		| token.keyword.restrict_
		| token.keyword.volatile_
	)
	# (6.7.5) type-qualifier-list:
	type_qualifier_list = type_qualifier[1, ...]
	# (6.7.4) function-specifier:
	function_specifier = token.keyword.inline_

	# (6.7.5) pointer:
	pointer = pp.Group(
		(token.punctuator.asterisk + pp.Optional(type_qualifier_list))[1, ...])

	# (6.7.5) declarator:
	direct_declarator_base = pp.Optional(pointer) + token.identifier
	direct_declarator_postfix1 = (
		token.punctuator.left_bracket
		+ pp.SkipTo(token.punctuator.right_bracket)
		+ token.punctuator.right_bracket
	)
	direct_declarator_postfix2 = (
		token.punctuator.left_paren
		+ pp.SkipTo(token.punctuator.right_paren)
		+ token.punctuator.right_paren
	)
	declarator = pp.Forward()
	direct_declarator_1 = (token.identifier.copy())("id")
	direct_declarator_2 = (
		token.punctuator.left_paren
		+ declarator
		+ token.punctuator.right_paren
	)
	direct_declarator = (
		direct_declarator_1
		| direct_declarator_2
	) + pp.ZeroOrMore(direct_declarator_postfix1 | direct_declarator_postfix2)
	declarator <<= (pp.Optional(pointer))("pointer") + direct_declarator
	

	# (6.7.8) designator:
	"""
	designator_1 = pp.Forward()
	designator_1 <<= (
		token.punctuator.left_bracket
		+ pp.SkipTo(pp.Word("[]"))
		+ pp.ZeroOrMore(
			designator_1
			+ pp.SkipTo(pp.Word("[]"))
		)
		+ token.punctuator.right_bracket
	)
	"""
	designator_1 = pp.nestedExpr("[", "]")
	designator = pp.Combine(
		designator_1
		| (token.punctuator.dot + token.identifier)
	)
	# (6.7.8) designator-list:
	designator_list = pp.OneOrMore(designator)
	# (6.7.8) designation:
	designation = designator_list + token.punctuator.simple_assign_op
	# (6.7.8) initializer:
	initializer_1 = (
		# assignment-expression代替
		pp.SkipTo(token.punctuator.semicolon)
	)
	initializer_2 = (
		token.punctuator.left_brace
		+ initializer_list
		+ pp.Optional(token.punctuator.comma)
		+ token.punctuator.right_brace
	)
	initializer = (
		initializer_1
		| initializer_2
	)
	# (6.7.8) initializer-list:
	initializer_list_1 = pp.Optional(designation) + initializer
	initializer_list <<= (
		initializer_list_1
		+ pp.ZeroOrMore(
			token.punctuator.comma
			+ initializer_list_1
		)
	)

	# (6.7) init-declarator:
	init_declarator = pp.Group(
		pp.Group(declarator.copy())("declarator")
		+ pp.Optional(
			token.punctuator.simple_assign_op
			+ initializer
		)("init")
	)
	# (6.7) init-declarator-list:
#	init_declarator_list = (
#		init_declarator
#		+ pp.ZeroOrMore(
#			token.punctuator.comma
#			+ init_declarator
#		)
#	)("declarator_list")
	init_declarator_list = pp.Group(
		pp.delimitedList(init_declarator, ",")
	)("declarator_list")

	# (6.7.1) storage-class-specifier:
	storage_class_specifier = (
#		token.keyword.typedef_.copy().setParseAction(ev_hdler.typedef_begin)
		token.keyword.typedef_("typedef")
		| token.keyword.extern_
		| token.keyword.static_
		| token.keyword.auto_
		| token.keyword.register_
		| token.keyword.near
		| token.keyword.far
	)
	storage_class_specifier_la = (
		token.keyword.typedef_
		| token.keyword.extern_
		| token.keyword.static_
		| token.keyword.auto_
		| token.keyword.register_
		| token.keyword.near
		| token.keyword.far
	)

	struct_or_union_specifier = pp.Forward()
	enum_specifier = pp.Forward()
	typedef_name = token.identifier

	# (6.7.2) type-specifier:
	type_specifier_int_pre = (
		token.keyword.signed_
		| token.keyword.unsigned_
	)
	type_specifier_int = (
		token.keyword.char_
		| token.keyword.short_
		| token.keyword.int_
		| (token.keyword.long_ + pp.Optional(token.keyword.long_))
	)
	type_specifier = (
		token.keyword.void_
		| (pp.Optional(type_specifier_int_pre) + type_specifier_int)
		| token.keyword.float_
		| token.keyword.double_
		| token.keyword._Bool_
		| token.keyword._Complex_
		| struct_or_union_specifier
		| enum_specifier
		| typedef_name
	)
	type_specifier_root = (
		token.keyword.void_
		| (pp.Optional(type_specifier_int_pre) + type_specifier_int)
		| token.keyword.float_
		| token.keyword.double_
		| token.keyword._Bool_
		| token.keyword._Complex_
		| struct_or_union_specifier
		| enum_specifier
		| typedef_name
	)

	# (6.7.2.1) specifier-qualifier-list:
	# type-specifierは1度しか出現しないものとする
	specifier_qualifier_list = pp.Group(
		pp.ZeroOrMore(type_qualifier)
		+ type_specifier.copy()('type_spec')
		+ pp.ZeroOrMore(type_qualifier)
	)('specifier_qualifier_list')

	# (6.7.2.1) struct-or-union:
	struct_or_union = (token.keyword.struct_ | token.keyword.union_)

	# (6.7.2.1) struct-declarator:
	struct_declarator_1 = (
		token.punctuator.colon
		+ constant_expression.copy()
	)
	struct_declarator_2 = (
		declarator.copy()
		+ pp.Optional(struct_declarator_1)
	)
	struct_declarator = (struct_declarator_1 | struct_declarator_2)
	# (6.7.2.1) struct-declarator-list:
	struct_declarator_list = (
		struct_declarator
		+ pp.Optional(
			token.punctuator.comma
			+ struct_declarator
		)
	)
	# (6.7.2.1) struct-declaration:
	struct_declaration = pp.Group(
		pp.ZeroOrMore(grammar_comment.any_comment_parser)("comment_pre")
		+ specifier_qualifier_list
		+ struct_declarator_list
		+ token.punctuator.semicolon
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
	)
	# (6.7.2.1) struct-declaration-list:
	struct_declaration_list = pp.OneOrMore(struct_declaration)
	# (6.7.2.1) struct-or-union-specifier:
	struct_or_union_specifier_1 = (
		token.punctuator.left_brace
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ pp.Group(struct_declaration_list)("struct_decl_list")
		+ token.punctuator.right_brace
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
	)
	struct_or_union_specifier_2 = (
		token.identifier.copy()("struct_id")
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ pp.Optional(struct_or_union_specifier_1)
	)
	struct_or_union_specifier <<= pp.Group(
		struct_or_union("struct_or_union")
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ (
			struct_or_union_specifier_1
			| struct_or_union_specifier_2
		)
	)("struct_spec")

	# (6.7) declaration-specifiers:
	declaration_specifiers = (
		pp.ZeroOrMore(storage_class_specifier)
		& pp.Optional(type_specifier)
		& pp.ZeroOrMore(type_qualifier)
		& pp.ZeroOrMore(function_specifier)
	)
	declaration_specifiers_root = (
		pp.ZeroOrMore(storage_class_specifier)
		& pp.Optional(type_specifier_root)
		& pp.ZeroOrMore(type_qualifier)
		& pp.ZeroOrMore(function_specifier)
	)
	# lookAhead用のハンドラ無しver
	declaration_specifiers_la = (
		pp.ZeroOrMore(storage_class_specifier_la)
		& pp.Optional(type_specifier)
		& pp.ZeroOrMore(type_qualifier)
		& pp.ZeroOrMore(function_specifier)
	)
	"""
	declaration_specifiers = (
		pp.ZeroOrMore(
			storage_class_specifier
			| type_qualifier
			| function_specifier
		)
		+ type_specifier.copy().setParseAction(analyzer.declaration_type)
		+ pp.ZeroOrMore(
			storage_class_specifier
			| type_qualifier
			| function_specifier
		)
	)
	"""

	# (6.7.2.2) enumerator:
	enumerator = (
		token.constant_def.enumeration_constant.copy()("enum_id")
		+ pp.Optional(
			token.punctuator.simple_assign_op
			# expression解析は再帰し過ぎで死ぬ
#			+ constant_expression
			+ pp.CharsNotIn(',}')
		)("enum_init")
	)
	# (6.7.2.2) enumerator-list:
	enumerator_list = (
		pp.ZeroOrMore(grammar_comment.any_comment_parser)("comment_pre")
		+ enumerator
		+ pp.ZeroOrMore(
			token.punctuator.comma
			+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
			+ pp.ZeroOrMore(grammar_comment.any_comment_parser)("comment_pre")
			+ pp.Optional(enumerator)
		)
	)
	# (6.7.2.2) enum-specifier:
	enum_specifier_1 = (
		token.punctuator.left_brace
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ pp.Group(enumerator_list)("enum_list")
		+ token.punctuator.right_brace
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
	)
	enum_specifier_2 = (
		token.identifier.copy()("enum_id")
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ pp.Optional(enum_specifier_1)
	)
	enum_specifier <<= pp.Group(
		token.keyword.enum_("enum")
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ (
			enum_specifier_2
			| enum_specifier_1
		)
	)("enum_spec")

	# (6.7) declaration:
	# 実質不使用
	# グローバル宣言はdeclarationから始まらず、external-declarationから開始である点に注意
	declaration = pp.Group(
		declaration_specifiers
		+ pp.Optional(init_declarator_list)
		+ token.punctuator.semicolon
	)



	abstract_declarator = pp.Forward()

	# (6.7.5) parameter-declaration:
	parameter_declaration = (
		declaration_specifiers
		+ (
			declarator
			| pp.Optional(abstract_declarator)
		)
	)
	# (6.7.5) parameter-list:
	parameter_list = (
		parameter_declaration
		+ pp.Optional(
			token.punctuator.comma
			+ parameter_declaration
		)
	)
	# (6.7.5) parameter-type-list:
	parameter_type_list = (
		parameter_list
		+ pp.Optional(
			token.punctuator.comma
			+ token.punctuator.ellipsis
		)
	)

	direct_abstract_declarator = pp.Forward()
	# (6.7.6) abstract-declarator:
	abstract_declarator_1 = (
		pointer
		+ pp.Optional(direct_abstract_declarator)
	)
	abstract_declarator_2 = (
		direct_abstract_declarator
	)
	abstract_declarator <<= (
		abstract_declarator_1
		| abstract_declarator_2
	)
	# (6.7.6) direct-abstract-declarator:
	direct_abstract_declarator_1 = (
		token.punctuator.left_paren
		+ abstract_declarator
		+ token.punctuator.right_paren
	)
	direct_abstract_declarator_2 = (
		pp.Optional(direct_abstract_declarator)
		+ (
			pp.nestedExpr("[", "]")
			| (
				token.punctuator.left_paren
				+ pp.Optional(parameter_type_list)
				+ token.punctuator.right_paren
			)
		)
	)
	direct_abstract_declarator <<= (
		direct_abstract_declarator_1
		| direct_abstract_declarator_2
	)

	# (6.7.6) type-name:
	type_name <<= (
		specifier_qualifier_list
		+ pp.Optional(abstract_declarator)
	)

	# (6.9.1) declaration-list:
	declaration_list = pp.OneOrMore(declaration)

	# (6.9) external-declaration:
	# (6.9.1) function-definition:
	#     declaration-specifiers declarator declaration-listopt compound-statement
	# (6.7) declaration:
	#     declaration-specifiers init-declarator-listopt ;
	# declarator移行をlookaheadでチェック
	# 1) "declarator =", "declarator ,", "declarator ;", ";" はdeclaration
	external_declaration_lookahead_1 = pp.FollowedBy(
		declaration_specifiers_la
		+ (
			(
				declarator
				+ (
					token.punctuator.simple_assign_op
					| token.punctuator.comma
					| token.punctuator.semicolon
				)
			)
			| token.punctuator.semicolon
		)
	)
	external_declaration_1 = (
		external_declaration_lookahead_1.ignore(grammar_comment.comment_parser)
		+ pp.Group(
			(
				declaration_specifiers_root("decl_spec")
				+ pp.Optional(init_declarator_list)
			).ignore(grammar_comment.comment_parser)
			+ (
				token.punctuator.semicolon
				+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
			)
		)("external_decl").setParseAction(act_hdler.external_declaration)
	)
	# 2) "declarator declaration", "declarator {" はfunction-definition
	external_declaration_lookahead_2 = pp.FollowedBy(
		declaration_specifiers_la
		+ declarator
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ (
			declaration
			| token.punctuator.left_brace
		)
	)
	external_declaration_2 = (
		external_declaration_lookahead_2
		+ declaration_specifiers
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ declarator
		+ pp.Optional(declaration_list)
		+ pp.Optional(grammar_comment.one_line_comment_parser)("comment")
		+ pp.nestedExpr("{", "}")
	)
	external_declaration = (
		grammar_pp.parser
		| external_declaration_1
		| external_declaration_2.ignore(grammar_comment.comment_parser)
		| grammar_comment.any_comment_parser.copy().setParseAction(act_hdler.comment)
		# ここまでにマッチしなかったら適当に読み捨てる
		| token.identifier.copy().setParseAction(parse_debug_unknown_token)
	)
	translation_unit = pp.OneOrMore(external_declaration) + pp.Regex(r".*").setParseAction(parse_debug_unknown_token)

parser = grammar_def.translation_unit
