template<typename T>
double simple_function_typename(float a, bool b = true);

template<class T>
double simple_function_class(float a, bool b = true);

template<typename T, typename P = const float>
const T complex_function(float a, T b, P& c, char d = '3');

template<>
const int* specialisation_function(float a, int* b, float& c, char d);

template<typename T>
concept AlwaysTrue = true;

template<typename T>
void requires_concept_function(T a) requires AlwaysTrue<T>;

template<AlwaysTrue T>
int requires_bool_function(T a = 1) requires true or false;

template<AlwaysTrue T>
T basic_concept_function();
