

[[nodiscard]]
int foo(int x, int y)
{
    return y;
}

[[nodiscard]] [[test_foo2]]
[[test_foo2_2]]
int foo2(int x, int y)
{
    return y;
}


[[nodiscard]]
int foo_functions([[maybe_unused]] int x, int y,
[[test_1, test_2]] [[test_3]] int z)
{
    return y;
}

[[deprecated]]
struct Wololo
{
    int a;
    int b;
    [[test_c1]]
    [[test_c2]]
    int c;
    private:
    [[test_fnc]]
    void foo(int a, [[test_arg]] int b);
};

[[atr_namespace]]
namespace TestName
{

}

[[test_enum]]
enum TestEnum
{
VAL_1,
VAL_2,
VAL_3
};