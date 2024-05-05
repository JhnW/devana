struct SimpleStructTest
{
    double a;
    const int b;
    void *c;
    static bool d;
    float foo(double a);
};

class SimpleClassTest
{
    double a;
    const int b;
    void *c;
    static bool d;
    float foo(double a);
    mutable float e;
};

class ClassSections
{
float foo1();
double a;
private:
float foo2();
double b;
public:
float foo3();
double c;
protected:
float foo4();
double d;
public:
float foo5();
double e;
};

class ClassOperators
{
    float operator()(long b, float b);
    float operator[](char a);
    float operator->();
    bool operator==(double a);
    bool operator!=(double a);
    bool operator>=(double a);
    bool operator<=(double a);
    bool operator<(double a);
    bool operator>(double a);
    bool operator<=>(double a);
    bool operator+(double a);
    bool operator-(double a);
    bool operator*(double a);
    bool operator/(double a);
    bool operator&&(double a);
    bool operator||(double a);
    bool operator%(double a);
    bool operator&(double a);
    bool operator|(double a);
    bool operator^(double a);
    bool operator<<(double a);
    bool operator>>(double a);
    bool operator+=(double a);
    bool operator-=(double a);
    bool operator/=(double a);
    bool operator*=(double a);
    bool operator%=(double a);
    bool operator&=(double a);
    bool operator|=(double a);
    bool operator^=(double a);
    bool operator>>=(double a);
    bool operator<<=(double a);
    bool operator++();
    bool operator++(int);
    bool operator--();
    bool operator--(int);
    operator bool();
    bool operator!();
    bool operator~();
    int operator*();
    int operator&();
    int operator->();
    int operator,(int a);
    void* operator new(size_t a);
    void operator delete(void* a);
    void* operator new[](size_t a);
    void operator delete[](void* a);
};

struct ClassConstructors
{
    ClassConstructors(float b):
        a(0.5+1),
        b(7+b),
        c(":)"),
        d{1,2,3,4,9.5}
        {
        }
    ClassConstructors(const ClassConstructors &src);
    ClassConstructors(const ClassConstructors &&src);
    explicit ClassConstructors(double a);
    ClassConstructors& operator= ( const ClassConstructors& src);
    ClassConstructors& operator= ( const ClassConstructors&& src);
    virtual ~ClassConstructors();

    double a;
    float b;
    char* c;
    double d[];
};

class ClassInheritanceParent
{
public:
    ClassInheritanceParent();
    virtual ~ClassInheritanceParent();

protected:
    int foo();
    double bar();

private:
    int baz();
};

class Parent1
{
    float *data;
};

class Parent2
{
public:
    Parent2(int a = 7);
    virtual ~Parent2();

    virtual void abstractMethod() = 0;
    double foo();
};

class SimpleChild: public Parent1
{
    SimpleChild();
};

class InitChild: public Parent2
{
    InitChild(): Parent2(6)
    {
    }
};

class NoSpecChild: Parent1
{
    NoSpecChild();
};

class MultiChild: private Parent1, public Parent2
{
    MultiChild(int a):
        Parent1(),
        Parent2(a),
        c(a+7)
        {
        }

    double c;
};

class VirtualChild: public virtual Parent2
{
    VirtualChild();

};

class NoSpecVirtualChild: virtual Parent2
{
    NoSpecVirtualChild();
};

class MethodMods
{
public:
    MethodMods() = default;
    MethodMods(const MethodMods&) = delete;
    virtual double virtualMethod_1();
    virtual double virtualMethod_2() = 0;
    double pureVirtualMethod_2() override;
    double pureVirtualMethod_3() final;
    static float staticMethod();
    void method_1(int *a) volatile;
    int method_2(int a) const;
};

class FinalClass final
{
    double b;
};

class DefaultFieldsValue
{
    const double default_value = (1.0+0.7)/4.25;
    static constexpr float default_constexpr_value = 15.75f;
}

namespace TestNamespace
{
    class ParentInNamespace
    {
    };
}

class ChildrenOutsideNamespace: public TestNamespace::ParentInNamespace
{
};