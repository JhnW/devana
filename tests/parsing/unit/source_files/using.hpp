namespace nom {
    struct A
    {
        int a;
        float b;
    };
}

using B = const nom::A*;

int foo(const B x) {
    return x->a / x->b;
}

template<typename T>
struct A_T
{
    float x;
    const T y;
};

using AT = const A_T<double>;

namespace num {
    struct A
    {
        char x;
        int y;
    };
}