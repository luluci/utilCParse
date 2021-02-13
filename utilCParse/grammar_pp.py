"""
A.3 Preprocessing directives
grammar定義
"""

from . import token
import pyparsing as pp

pp_dir = token.preprocessing_directive

# (6.10) if-group:
pp_if_group = pp_dir.pp_group + pp_dir.pp_if

pp_group_part = pp.Combine(pp_dir.pp_group + token.constant_def.c_char[1,...])

# Preproは読み捨てる
pp_parser = pp.Group(pp_group_part + pp.lineEnd)

