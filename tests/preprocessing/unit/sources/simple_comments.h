#ifndef SIMPLE_COMMENTS_H
#define SIMPLE_COMMENTS_H

#include <string>
#include <vector>

//META
//devana::meta_name("Tester")
class TestClass
{
public:
    //devana::property()
    const std::string& getName() const
    {
        return name;
    }

private:
    std::string name;
    //generate_getter("getData", PUBLIC)
    //devana::test(1, 6.5)
    std::vector<double> _data;
};

#endif