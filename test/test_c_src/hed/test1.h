#include <stdint.h>

// 基本型
unsigned int u16_var, u16_var_2 = 0;				/* uint16変数1,2 */
uint32_t **u32p_unspe_var = 0;
__near uint32_t *u32p_near_var = 0;
__far uint32_t *u32p_far_var = 0;
static signed int i16_static = 1;
const unsigned char u8_const = 2;
static const volatile uint32_t u32_var = 3;

typedef void *(func1_t)(uint32_t, int16_t *);
typedef void *(*funcptr1_t)(uint32_t, int16_t *);

// enum
enum					// def ENUM_1
{						/* 1st hogehoge */
	ENUM_1_1 = 0,		// 1-1 => ?
	ENUM_1_2,			/* 1-2 => ?? */
	ENUM_1_3 = 100,		// 1-3
	// max size
	ENUM_1_SIZE,		// enum1 size
} enum1_var;			// enum1 variable
// enum 2nd
enum enum_2 {				/* def ENUM_2 */
	ENUM2_1 = (ENUM_1_SIZE),
	ENUM2_2 = (ENUM_1_2 + 100),
	ENUM2_3 = (ENUM2_2 + 1000),
};
enum enum_2 enum2_var;

// hoge定義
struct hoge {/* def_hoge */
	// bytes
	int byte;		// byte1
} hoge_;

// bt_type定義
struct bf_type {
	// bitfield
	uint16_t	b0    :1;			// 0bit目
	uint16_t	b1_5  :5;			// 1～5bit目
	uint16_t	b6    :1;			// 6bit目
	uint16_t	b7_8  :2;			// 7～8bit目、バイト境界またぎ
	uint16_t	b9_14 :6;			// 9～14bit目
	uint16_t	b15   :1;			// 15bit目
	uint16_t	b16   :1;			// 16bit目
	// padding: ?bit
	// bytes
	uint16_t	byte2;				// 2バイト、パディングあり
	funcptr1_t fp1_ary1[2];
	struct bf_inner_type {			// インナー構造体定義
		uint16_t	b0    :1;		// b0
		uint16_t	b1_5  :5;		// b1_5
		uint16_t	byte1;
	} inner;
	uint32_t *u32p_var;
	// union
	union {
		uint16_t	u16[2];
		uint32_t	u32;
	} port_t[5];
};

typedef struct bf_type bf_t;

/* bt変数1 */
struct bf_type var1;	// bt変数1
bt_t var2;				/* bt変数2 */
const static unsigned char var3 = 0;

struct unknown_t var_unknown;

bf_t bf_func(bf_t bf, bf_t const * const bf_ptr);
STATIC GLOBAL int int_var;
hoge hoge??
//EOF