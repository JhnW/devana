template <typename T>
class TemplateArray
{
public:
    const T* getData()
    {
        return data;
    }

    void setData(T* d)
    {
        data = d;
    }

private:
    T* data;
};

template<typename T, typename P = float>
struct TemplateData
{
    T* data1;
    P* data2;
};


void functionTemplateArg_1(const TemplateArray<float> &a);
void functionTemplateArg_2(const TemplateArray<TemplateArray<float>> &a);
void functionTemplateArg_3(const TemplateData<float, int*> &a);
void functionTemplateArg_4(const TemplateData<TemplateData<double, int>, int*> &a);
template<typename T>
void functionTemplateArg_5(const TemplateArray<T> &a);
template<typename T>
void functionTemplateArg_6(const TemplateArray<const TemplateArray<T>> &a);
template<typename T>
void functionTemplateArg_7(const TemplateArray<const T*> &a);
template<typename T>
void functionTemplateArg_8(const TemplateData<double, T> &a);

TemplateArray<float> functionTemplateReturn_1();
TemplateArray<float*> functionTemplateReturn_2();
const TemplateArray<float>* functionTemplateReturn_3();
TemplateArray<TemplateArray<float>> functionTemplateReturn_4();
template<typename T>
TemplateArray<T> functionTemplateReturn_5();
template<typename T>
TemplateArray<T*> functionTemplateReturn_6();
template<typename T>
const TemplateArray<float>* functionTemplateReturn_7();
template<typename T>
TemplateArray<TemplateArray<T>> functionTemplateReturn_8();

typedef TemplateArray<char*> typedefCharArray;
typedef TemplateArray<TemplateArray<char*>> typedefCharArrayArray;

typedefCharArray* typedefFunction_1(typedefCharArrayArray a);
TemplateArray<typedefCharArray*> typedefFunction_2(TemplateArray<typedefCharArrayArray> a);

struct FieldHolder
{
    TemplateArray<float> a;
};

template<typename T>
struct FieldHolderTemplate
{
    TemplateArray<T> a;
};

struct TemplateParent_1: FieldHolderTemplate<float>
{
    double b;
};

template<typename T>
struct TemplateParent_2: FieldHolderTemplate<const T>
{
    T *a;
};

template<typename T>
void templateFunctionSpec_1(double b, T a) {}

template<>
void templateFunctionSpec_1<FieldHolderTemplate<char>*>(double b, FieldHolderTemplate<char>* a) {}

struct TemplateFunctionSpecHolder
{
    template<typename T>
    void templateMethodSpec_1(double b, T a) { return; }
};

template<>
void TemplateFunctionSpecHolder::templateMethodSpec_1<FieldHolderTemplate<char>*>(double b, FieldHolderTemplate<char>* a)
{
    return;
}

template<typename T>
struct BaseArray
{
    T* data;
    long len;
};

template<typename T>
struct TestTemplateFields
{
    const BaseArray<float> data1;
    BaseArray<BaseArray<const char*>> data2;
    BaseArray<T*> data3;
};

template<typename A, class B>
concept TestConceptCase1 = A{} and B{};

template<class T = int>
concept TestConceptCase2 = false;