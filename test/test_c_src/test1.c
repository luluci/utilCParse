int *hoge;


// preprocessor
#define DEBUG_MODE				/* DEBUGモード */
#if 1
	#include <stdio.h>			//【コメント】
	# include <stdint.h>		//<! ※
#else
	# include <stdint.h>
#endif
#ifdef DEBUG_MODE
	#pragma xxx
	#undef DEBUG_MODE
#endif
#ifndef DEBUG_MODE
	#error xxx
#endif

// 変数定義
/* var1 */
int var1;					// 変数var1: char*
uint8_t var2;

char str1[] = "a//b";		// 変数str1: char*
