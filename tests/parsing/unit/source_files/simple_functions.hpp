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

constexpr int mod_constexpr_func(int a);
consteval int mod_consteval_func(int a);
int mod_consteval_if_func(int a)
{
    if consteval
    {
        return 8;
    }
    else
    {
        return 7;
    }
}
static int mod_static_func(int a);
inline int mod_inline_func(int a);
int mod_noexcept_func(int a) noexcept;

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

