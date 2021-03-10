import pyparsing as pp
from . import token
from . import grammar
from . import grammar_comment
from . import grammar_pp
from . import analyzer as analyzer_module

analyzer = analyzer_module.analyzer

parser = pp.OneOrMore(
	grammar.parser
	| grammar_pp.pp_parser
)
