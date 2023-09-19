[[devana::custom_1]]
struct TestStruct_1
{
    int a;
    [[devana::custom_1_2]]
    int b;
};

namespace TestNamespace_1
{

    void testFunction_1([[maybe_unused]] int a);

    [[devana::custom_fnc]]
    void testFunction_2();

}

[[devana::custom_2]]
namespace TestNamespace_2
{

    void testFunction_2_1();

    void testFunction_2_2();

    void testFunction_2_3();

    namespace TestNamespace_3
    {

        [[devana::custom_fnc_internal]]
        void testFunction_3_1();

    }

}
