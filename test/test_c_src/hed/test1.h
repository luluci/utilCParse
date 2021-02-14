#include <stdint.h>

// hoge定義
struct hoge {
	int byte;		// byte1
};

// bt_type定義
struct bf_type {
	uint16_t	b0    :1;			// 0bit目
	uint16_t	b1_5  :5;			// 1～5bit目
	uint16_t	b6    :1;			// 6bit目
	uint16_t	b7_8  :2;			// 7～8bit目、バイト境界またぎ
	uint16_t	b9_14 :6;			// 9～14bit目
	uint16_t	b15   :1;			// 15bit目
	uint16_t	b16   :1;			// 16bit目
	uint16_t	byte2;				// 2バイト、パディングあり
	struct bf_inner_type {			// インナー構造体定義
		uint16_t	b0    :1;		// b0
		uint16_t	b1_5  :5;		// b1_5
		uint16_t	byte1;
	} inner;
	union {
		uint16_t	u16[2];
		uint32_t	u32;
	} port_t[5];
};

typedef struct bf_type bf_t;

/* bt変数1 */
bf_t var1;		// bt変数1
bt_t var2;		/* bt変数2 */
const static unsigned char var3 = 0;