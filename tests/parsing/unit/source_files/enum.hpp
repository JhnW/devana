enum TestEnum
{
    VALUE_TEST_1,
    VALUE_TEST_2,
    VALUE_TEST_3 = 100,
    VALUE_TEST_4
    VALUE_TEST_5 = 0xdf,
    VALUE_TEST_6,
    VALUE_TEST_7
};

enum class TestEnumClass
{
    VALUE_TEST_1,
    VALUE_TEST_2,
    VALUE_TEST_3 = 100,
    VALUE_TEST_4
    VALUE_TEST_5 = 0xdf,
    VALUE_TEST_6,
    VALUE_TEST_7
};

enum struct TestEnumStruct
{
    VALUE_TEST_1,
    VALUE_TEST_2,
    VALUE_TEST_3 = 100,
    VALUE_TEST_4
    VALUE_TEST_5 = 0xdf,
    VALUE_TEST_6,
    VALUE_TEST_7
};

enum TestEnumNumber: char
{
    NUM_VALUE_TEST_1,
    NUM_VALUE_TEST_2 = 'a',
    NUM_VALUE_TEST_3
};