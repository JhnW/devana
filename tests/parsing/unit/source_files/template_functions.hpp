template<typename T>
double simple_function_typename(float a, bool b = true);

template<class T>
double simple_function_class(float a, bool b = true);

template<typename T, typename P = const float>
const T complex_function(float a, T b, P& c, char d = '3');

template<>
const int* specialisation_function(float a, int* b, float& c, char d);