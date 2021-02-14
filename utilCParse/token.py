"""
A.1 Lexical grammar 定義
"""
import pyparsing as pp


# A.1.2 Keywords
class keyword:
	auto_ = pp.Keyword("auto")
	break_ = pp.Keyword("break")
	case_ = pp.Keyword("case")
	char_ = pp.Keyword("char")
	const_ = pp.Keyword("const")
	continue_ = pp.Keyword("continue")
	default_ = pp.Keyword("default")
	do_ = pp.Keyword("do")
	double_ = pp.Keyword("double")
	else_ = pp.Keyword("else")
	enum_ = pp.Keyword("enum")
	extern_ = pp.Keyword("extern")
	float_ = pp.Keyword("float")
	for_ = pp.Keyword("for")
	goto_ = pp.Keyword("goto")
	if_ = pp.Keyword("if")
	inline_ = pp.Keyword("inline")
	int_ = pp.Keyword("int")
	long_ = pp.Keyword("long")
	register_ = pp.Keyword("register")
	restrict_ = pp.Keyword("restrict")
	return_ = pp.Keyword("return")
	short_ = pp.Keyword("short")
	signed_ = pp.Keyword("signed")
	sizeof_ = pp.Keyword("sizeof")
	static_ = pp.Keyword("static")
	struct_ = pp.Keyword("struct")
	switch_ = pp.Keyword("switch")
	typedef_ = pp.Keyword("typedef")
	union_ = pp.Keyword("union")
	unsigned_ = pp.Keyword("unsigned")
	void_ = pp.Keyword("void")
	volatile_ = pp.Keyword("volatile")
	while_ = pp.Keyword("while")
	_Bool_ = pp.Keyword("_Bool")
	_Complex_ = pp.Keyword("_Complex")
	Imaginary_ = pp.Keyword("_Imaginary")

# A.1.3 Identifiers
class identifier_def:
	nondigit = pp.Char(pp.alphas + "_")
	digit = pp.Char(pp.nums)
	universal_character_name_u = pp.Literal("\\u") + pp.Char(pp.hexnums * 4)
	universal_character_name_U = pp.Literal("\\U") + pp.Char(pp.hexnums * 8)
	universal_character_name = (universal_character_name_u | universal_character_name_U)
	identifier_nondigit = (nondigit | universal_character_name)
# (6.4.2.1) identifier:
identifier = pp.Combine(identifier_def.identifier_nondigit + pp.ZeroOrMore(identifier_def.identifier_nondigit | identifier_def.digit))

# A.1.5 Constants
class constant_def:
	zero = pp.Char("0")
	nonzero_digit = pp.Char("123456789")
	digit = pp.Char(pp.nums)
	octal_digit = pp.Char("01234567")
	hexadecimal_digit = pp.Char(pp.hexnums)
	# (6.4.4.1) decimal-constant:
	decimal_constant = nonzero_digit + digit.copy()[...]
	# (6.4.4.1) octal-constant:
	octal_constant = zero + octal_digit.copy()[...]
	# (6.4.4.1) hexadecimal-constant:
	hexadecimal_prefix = pp.Word("0x") | pp.Word("0X")
	hexadecimal_constant = hexadecimal_prefix + hexadecimal_digit.copy()[1, ...]
	# (6.4.4.1) integer-suffix:
	unsigned_suffix = pp.Char("uU")
	long_suffix = pp.Char("lL")
	longlong_suffix = pp.Word("ll") | pp.Word("LL")
	integer_suffix = (unsigned_suffix + pp.Optional(long_suffix | longlong_suffix)) | ((long_suffix | longlong_suffix) + pp.Optional(unsigned_suffix))
	# (6.4.4.1) integer-constant:
	integer_constant = (decimal_constant | octal_constant | hexadecimal_constant) + pp.Optional(integer_suffix)
	# (6.4.4.2) floating-constant:
	# 略
	# (6.4.4.3) enumeration-constant:
	enumeration_constant = identifier
	# (6.4.4.4) character-constant:
	simple_escape_sequence = pp.Char("\\") + pp.Char("\\'\"?abfnrtv")
	octal_escape_sequence = pp.Char("\\") + octal_digit.copy()[1, ...]
	hexadecimal_escape_sequence = pp.Word("\\x") + hexadecimal_digit.copy()[1, ...]
	escape_sequence = simple_escape_sequence | octal_escape_sequence | hexadecimal_escape_sequence | identifier_def.universal_character_name
	c_char = pp.CharsNotIn("'\\\r\n") | escape_sequence
	character_constant = pp.Optional(pp.Char("L")) + pp.Char("'") + c_char[1,...] + pp.Char("'")
# (6.4.4) constant:
constant = pp.Combine(constant_def.integer_constant | constant_def.enumeration_constant | constant_def.character_constant)

# A.1.6 String literals
class string_literal_def:
	s_char = pp.CharsNotIn('"\\\r\n') | constant_def.escape_sequence
string_literal = pp.Combine(pp.Optional(pp.Char("L")) + pp.Char('"') + string_literal_def.s_char[1, ...] + pp.Char('"'))

# A.1.7 Punctuators
class punctuator:
	left_bracket = pp.Literal("[")
	right_bracket = pp.Literal("]")
	left_paren = pp.Literal("(")
	right_paren = pp.Literal(")")
	left_brace = pp.Literal("{")
	right_brace = pp.Literal("}")
	dot = pp.Literal(".")
	arrow_op = pp.Literal("->")
	increment_op = pp.Literal("++")
	decrement_op = pp.Literal("--")
	ampersand = pp.Literal("&")
	asterisk = pp.Literal("*")
	plus = pp.Literal("+")
	minus = pp.Literal("-")
	bitwise_complement_op = pp.Literal("~")
	logical_negation_op = pp.Literal("!")
	div_op = pp.Literal("/")
	remain_op = pp.Literal("%")
	left_shift_op = pp.Literal("<<")
	right_shift_op = pp.Literal(">>")
	lt_op = pp.Literal("<")
	gt_op = pp.Literal(">")
	lte_op = pp.Literal("<=")
	gte_op = pp.Literal(">=")
	equal_op = pp.Literal("==")
	inequal_op = pp.Literal("!=")
	bitwise_EXOR_op = pp.Literal("^")
	bitwise_OR_op = pp.Literal("|")
	logical_AND_op = pp.Literal("&&")
	logical_OR_op = pp.Literal("||")
	conditional_op = pp.Literal("?")
	colon = pp.Literal(":")
	semicolon = pp.Literal(";")
	ellipsis = pp.Literal("...")
	simple_assign_op = pp.Literal("=")
	mul_assign_op = pp.Literal("*=")
	div_assign_op = pp.Literal("/=")
	remain_assign_op = pp.Literal("%=")
	add_assign_op = pp.Literal("+=")
	sub_assign_op = pp.Literal("-=")
	left_shift_assign_op = pp.Literal("<<=")
	right_shift_assign_op = pp.Literal(">>=")
	bitwise_AND_assign_op = pp.Literal("&=")
	bitwise_EXOR_assign_op = pp.Literal("^=")
	bitwise_OR_assign_op = pp.Literal("|=")
	comma = pp.Literal(",")
	sharp = pp.Literal("#")
	sharp_sharp = pp.Literal("##")
	alt_left_bracket = pp.Literal("<:")
	alt_right_bracket = pp.Literal(":>")
	alt_left_brace = pp.Literal("<%")
	alt_right_brace = pp.Literal("%>")
	alt_sharp = pp.Literal("%:")
	alt_sharp_sharp_op = pp.Literal("%:%:")


# A.3 Preprocessing directives
class preprocessing_directive:
	pp_group = pp.Char("#")
	# 
	pp_if = pp.Keyword("if")
	pp_ifdef = pp.Keyword("ifdef")
	pp_ifndef = pp.Keyword("ifndef")
	pp_elif = pp.Keyword("elif")
	pp_else = pp.Keyword("else")
	pp_endif = pp.Keyword("endif")
	# control
	pp_include = pp.Keyword("include")
	pp_define = pp.Keyword("define")
	pp_undef = pp.Keyword("undef")
	pp_line = pp.Keyword("line")
	pp_error = pp.Keyword("error")
	pp_pragma = pp.Keyword("pragma")


