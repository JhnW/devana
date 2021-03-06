void procedure_forward();
float* num_forward(double x, short *b);
float& num_default_forward(double test_var=76.0, double* a = nullptr);
void procedure_def()
{
    int a = 6*8;
    int b = 2*a;
    for(int i = 0; i < 5; i++)
    {
        a += b*i;
    }
}

constexpr int mod_constexpt_func(int a);
static int mod_static_func(int a);
inline int mod_inline_func(int a);

namespace test_namespace
{
typedef double typereal;
}

test_namespace::typereal namespace_return_func(int a);

static double attribute_func_1(char a);
inline double attribute_func_2(char a);
constexpr double attribute_func_3(char a)
{
    return 2.0;
}

static inline double attribute_func_4(char a);

