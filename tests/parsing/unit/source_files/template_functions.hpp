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

template<AlwaysTrue T = int, AlwaysTrue ...Args>
T template_concept_function();

template<typename T> requires AlwaysTrue<  T>
void requires_template_function1(T a) requires true or false;

template<AlwaysTrue T>
    requires true     or AlwaysTrue<T    >
int requires_template_function2(T a = 1)
    requires AlwaysTrue<T> and true;

template<AlwaysTrue T> requires (AlwaysTrue<T> or true) and false
void basic_concept_function();
