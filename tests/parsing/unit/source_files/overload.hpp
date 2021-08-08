int overloadFunc();
int overloadFunc(int a);
double overloadFunc(double b);
double overloadFunc(double *b = nullptr);

int overloadFunc()
{
    return 777;
}

int overloadFunc_2();
double overloadFunc_2();

int overloadFunc_3();
int overloadFunc_3(int a)
{
    return 8;
}

int overloadFunc_3(int a)
{
    return 9;
}

template<typename T>
double overloadFunc_4(T a)
{
    return 1.5;
}

template<typename T>
double overloadFunc_4(T a, char b)
{
    return 100.5;
}

template<typename T>
double overloadFunc_4(T* a)
{
    return 2.5;
}

double overloadFunc_4(int a)
{
    return 0.7;
}

template<>
double overloadFunc_4<double&>(double& a)
{
    return 2.7;
}

template<>
double overloadFunc_4<float>(float* a)
{
    return 2.7;
}
