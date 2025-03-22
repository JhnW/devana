#ifndef ENUMS_HPP
#define ENUMS_HPP

#include <vector>
#include <string>

// basic_log_all_fnc
struct Foo {
    // basic_log_all_fnc
    int x;
    // basic_log_all_fnc()
    int y;
};

// Logger1
struct Bar {
    int x;
    int y;
};

//Logger2
enum class Baz {
    A,
    B
};

//test_nm::generate_stupid_function_based_on_class([1,2,3,4])
class BigC {
public:
double z;
};

//test_nm::generate_stupid_function_based_on_class([1,2,3,4, 9], "custom_name")
class SmallC {
public:
double z;
};

#endif