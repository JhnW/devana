#include <vector>
#include <string>
#include <memory>

struct TestElement
{
    std::string a;
};

struct TestClass
{
    std::string a;
    std::vector<float> b;
    std::vector<TestElement> c;
    const std::vector<std::vector<double>> *d;
    std::shared_ptr<TestElement> e;
    std::vector<std::vector<double>> foo();
    void bar(const std::vector<std::vector<double>>& arg);
};

template<typename T>
struct TestTemplateElement
{
    T a;
    std::vector<T> b;
};

struct TestClassWithTemplate
{
    TestTemplateElement<const std::string*> a;
};

class TestInheritance: public std::string
{
};

class TestTemplateInheritance: public std::enable_shared_from_this<TestTemplateInheritance>
{
};

