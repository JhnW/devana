void (*empty_func)();
float (*standard_func)(double, char);
const float& (*return_attributes_func)();
void (*arguments_attributes_func)(const float&, int*);
void (*nested_1)(int, float (*)(const double));
void (*nested_2)(int, float (*ptr)(const double));

struct TestClass
{
    double x;
    double y;
};

TestClass& (*with_class_fnc)(const TestClass*, int);

template<typename T>
struct TestTemplateClass
{
    T* (*standard_func_template)(const T);
};