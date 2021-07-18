namespace SimpleNamespace
{
    double foo();
}

namespace NestedNamespace
{
    double bar();
    namespace InternalNamespace
    {
        int bar();
    }
}

namespace MultiNamespace
{
    double bar();
    using namespace SimpleNamespace;
    using namespace NestedNamespace::InternalNamespace;

}