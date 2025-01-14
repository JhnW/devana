
// Test comment 1.
void base_function();

/*
Test comment 2.
*/
constexpr void constexpr_function(int a);

enum TestEnum {
    // Test comment 3.
    VALUE_TEST_1,

    /*
    Test comment 4.
    Bla bla bla.
    */
    VALUE_TEST_2
};

class TestClass {
    private:
        int x;
    public:

        // Test comment 5.
        TestClass() {
            x = 10;
        }

        // Test comment 6.
        void increaseX();
};

