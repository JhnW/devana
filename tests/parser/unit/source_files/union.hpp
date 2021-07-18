union TestUnion
{
    bool a;
    double *b;
    unsigned short c;
};

class SimpleClass
{
    union NamedUnion {
        short a;
        double b;
    };
}

class ClassLikeUnion
{
    union {
        short a;
        double b;
    };
}