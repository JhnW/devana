template<typename T>
concept ConceptRequiresExpr = requires(T a, T b) {
    { a + b };
    { a-- };
};

template<typename A, class T>
concept ConceptMultipleRequires = requires(A a, T b) {
    a = b;
} || requires(A a, T b) {
    b = a;
};

template<typename T>
concept ConceptRequiresAlone = requires {
    T{};
};

template<typename T>
concept ConceptRefAndRequires = ConceptRequiresAlone<T> && requires(T t) {
    *t;
};

template<typename T>
concept ConceptParenExpr = (T{} > 0);

template<typename T>
concept ConceptRefToConcept = ConceptParenExpr<T>;

template<class T>
concept ConceptMultipleRefs = ConceptRequiresAlone<T> && ConceptRefToConcept<T>;

namespace ConceptNamespace {
    template<class T>
    concept ConceptInNamespace = true;
};

template<typename T>
concept ConceptStaticValue = T::value || true;

template<typename U>
concept ConceptNamespaceRef = ConceptNamespace::ConceptInNamespace<U*>;

template<typename A, class B = int, typename... Args>
concept ConceptTemplate = true;

template<ConceptStaticValue T = bool, ConceptNamespace::ConceptInNamespace ...Args>
class ClassBasicConcept;

template<ConceptStaticValue T>
class ClassMethodsConcept {
public:
    T process(const T arg);

    template<ConceptStaticValue B>
    void pair(const T arg1, const B arg2);
private:
    inline T* secret_stuff_(T* p) noexcept;
};

template<typename T> requires (true and ConceptStaticValue<T>)
struct StructRequires {
    const T abc;

    template<class B> requires ConceptNamespace::ConceptInNamespace< B >
    B foo() requires ConceptStaticValue<B  > ||  false;

    void calc() requires (
        true or false
    );
};

template<ConceptParenExpr T = int, ConceptParenExpr ...Args>
T function_with_concept();

template<typename T> requires ConceptParenExpr<T>
void function_with_requires_1(T a) requires true or false;

template<ConceptStaticValue T> requires  true  or ConceptParenExpr<T  >
int function_with_requires_2(T a = 1) requires ConceptParenExpr<T  > and  (true);

template<ConceptNamespace::ConceptInNamespace T>
T function_with_concept_namespace();
