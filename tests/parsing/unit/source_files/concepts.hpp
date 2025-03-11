template<typename T>
concept ConceptCase1 = requires(T a) {
    { --a };
    { a-- };
};

template<typename T>
concept ConceptCase2 = requires(T a, T b) {
    { a + b };
};

template<class T>
concept ConceptCase3 = requires(T a, T b) {
    a = b;
} || requires(T a, T b) {
    b = a;
};

template<typename T>
concept ConceptCase4 = requires {
    T{};
};

template<class T>
concept ConceptCase5 = requires {
    T(-1) < T(0); 
};

template<typename T>
concept ConceptCase6 = ConceptCase1<T> && requires(T t) {
    *t;
};

template<typename T>
concept ConceptCase7 = (T{} > 0);

template<ConceptCase7 T>
concept ConceptCase8 = ConceptCase7<T>;

template<class T>
concept ConceptCase9 = ConceptCase1<T> && ConceptCase2<T>;

template<typename T>
concept ConceptCase10 = ConceptCase1<T> || ConceptCase2<T>;

namespace testNamespace {
    template<class T>
    concept ConceptCase11 = true;
};

template<typename T>
concept ConceptCase12 = T::value || true;

template<typename U>
concept ConceptCase13 = testNamespace::ConceptCase11<U*>;

template<typename A, class B = int, typename... Args>
concept ConceptTemplate = true;
