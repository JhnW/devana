class Array
{
public:
    const double getData()
    {
        return data;
    }

    void setData(double d)
    {
        data = d;
    }

private:
    double data;
};

void functionClassArg(const Array &a);
Array* functionClassReturn();

class StorageClass
{
    Array *data;
};