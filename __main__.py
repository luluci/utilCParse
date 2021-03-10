import pathlib
import utilCParse

if True:
	# file
#	path = pathlib.Path("./test/test_c_src/test1.c")
	path = pathlib.Path("./test/test_c_src")
	analyzer = utilCParse.analyzer.analyzer()
	analyzer.analyze_dir(path)
