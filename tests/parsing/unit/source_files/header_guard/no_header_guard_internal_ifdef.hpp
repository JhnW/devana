struct Test1
{
    int a;
};

#ifndef TEST_DEF
#define TEST_DEF
struct Test2
{
    double a;
    float *c;
};
#endif

Test2* foo();