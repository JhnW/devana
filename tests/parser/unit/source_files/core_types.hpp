#ifndef __APPLE__
#include <cstdint>
#else
#include <tr1/cstdint>
#endif

typedef char typechar;
typedef char* typemodchar;
typedef uint32_t typeuint32;

namespace test_namespace
{
typedef double typereal;

namespace test_namespace_v2
{
typedef int16_t typeint16;
}

}
typedef test_namespace::typereal depend_typereal;

class CoreTypes {
int common_integer;
unsigned int common_u_integer;
short common_short;
unsigned short common_u_short;
char common_char;
unsigned char common_u_char;
long common_long;
unsigned long common_u_long;
long long common_long_long;
unsigned long long common_u_long_long;
float common_float;
double common_double;
long double common_long_double;
bool common_bool;

const int const_integer;
const unsigned int const_u_integer;
const short const_short;
const unsigned short const_u_short;
const char const_char;
const unsigned char const_u_char;
const long const_long;
const unsigned long const_u_long;
const long long const_long_long;
const unsigned long long const_u_long_long;
const float const_float;
const double const_double;
const long double const_long_double;
const bool const_bool;

int &ref_integer;
unsigned int &ref_u_integer;
short &ref_short;
unsigned short &ref_u_short;
char &ref_char;
unsigned char &ref_u_char;
long &ref_long;
unsigned long &ref_u_long;
long long &ref_long_long;
unsigned long long &ref_u_long_long;
float &ref_float;
double &ref_double;
long double &ref_long_double;
bool &ref_bool;

int *ptr_integer;
unsigned int *ptr_u_integer;
short *ptr_short;
unsigned short *ptr_u_short;
char *ptr_char;
unsigned char *ptr_u_char;
long *ptr_long;
unsigned long *ptr_u_long;
long long *ptr_long_long;
unsigned long long *ptr_u_long_long;
float *ptr_float;
double *ptr_double;
long double *ptr_long_double;
bool *ptr_bool;

static int static_integer;
static unsigned int static_u_integer;
static short static_short;
static unsigned short static_u_short;
static char static_char;
static unsigned char static_u_char;
static long static_long;
static unsigned long static_u_long;
static long long static_long_long;
static unsigned long long static_u_long_long;
static float static_float;
static double static_double;
static long double static_long_double;
static bool static_bool;

volatile int volatile_integer;
volatile unsigned int volatile_u_integer;
volatile short volatile_short;
volatile unsigned short volatile_u_short;
volatile char volatile_char;
volatile unsigned char volatile_u_char;
volatile long volatile_long;
volatile unsigned long volatile_u_long;
volatile long long volatile_long_long;
volatile unsigned long long volatile_u_long_long;
volatile float volatile_float;
volatile double volatile_double;
volatile long double volatile_long_double;
volatile bool volatile_bool;

const int &const_ref_integer;
static float* static_ptr_float;
void *ptr_void;

int64_t unknown_int64;
uint64_t unknown_u_int64;
int32_t unknown_int32;
uint32_t unknown_u_int32;
int16_t unknown_int16;
uint16_t unknown_u_int16;
int8_t unknown_int8;
uint8_t unknown_u_int8;

const uint8_t unknown_const_u_int8;
const int8_t &unknown_const_ref_int8;
int16_t *unknown_ptr_int16;
static int16_t unknown_static_int16;

typechar typedef_typechar;
const typechar typedef_const_typechar;
static typechar typedef_static_typechar;

const test_namespace::typereal typedef_namespace_typereal;
static test_namespace::test_namespace_v2::typeint16 typedef_namespace_static_nested;
depend_typereal* typedef_namespace_depend_typereal_ptr;


float array[20];
float arrayofarray[4][60];
void (*callback)(char);

};

void arrayGetFunction(int inTab[]);

char* global_var;

constexpr int constexpr_global_var = 77;

double **ptr_ptr_value;
char ***ptr_ptr_ptr_value;
const int **ptr_ptr_const_value;
static float ***ptr_ptr_ptr_static_value;
double** const* ptr_ptr_const_ptr_value;