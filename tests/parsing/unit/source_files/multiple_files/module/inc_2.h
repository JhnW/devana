#include "inc_1.hpp"

namespace Test1
{
    Test::TestArray foo();
}

namespace Test2
{
    using namespace Test;

    struct TestArrayArray
    {
        TestArray *d;
    };

}