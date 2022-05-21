typedef char* def_char_ptr;
typedef float def_float;
typedef const def_float const_def_float;
typedef def_float*  ptr_def_float;
typedef const def_char_ptr const_def_char_ptr;

namespace test_namespace
{
    typedef double typereal;
    namespace test_namespace_v2
    {
        typedef short typeint16;
    }
}
typedef test_namespace::typereal depend_typereal;
typedef test_namespace::test_namespace_v2::typeint16 depend_depend_typeint16;

typedef float array_1[];
typedef float array_2[5][12];