// Edge cases: recursion, function overloads, lambdas, operators
// Tests special C++ features and boundary conditions

#include <functional>
#include <iostream>
#include <vector>

// Edge Case 1: Recursive function (calls itself)
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);  // Recursive call
}

// Edge Case 2: Mutual recursion
bool isEven(int n);
bool isOdd(int n);

bool isEven(int n) {
    if (n == 0) return true;
    return isOdd(n - 1);
}

bool isOdd(int n) {
    if (n == 0) return false;
    return isEven(n - 1);
}

// Edge Case 3: Function overloads (same name, different signatures)
void print(int x) {
    std::cout << "Int: " << x << std::endl;
}

void print(double x) {
    std::cout << "Double: " << x << std::endl;
}

void print(const char* x) {
    std::cout << "String: " << x << std::endl;
}

// Edge Case 4: Lambda expressions
void useLambdas() {
    auto lambda1 = [](int x) { return x * 2; };
    auto lambda2 = [](int x, int y) { return x + y; };

    int result = lambda1(5) + lambda2(3, 4);
    std::cout << "Lambda result: " << result << std::endl;
}

// Edge Case 5: Operator overloading
class Counter {
public:
    int value;

    Counter() : value(0) {}

    Counter& operator++() {  // Prefix increment
        ++value;
        return *this;
    }

    Counter operator++(int) {  // Postfix increment
        Counter temp = *this;
        ++value;
        return temp;
    }

    bool operator==(const Counter& other) const {
        return value == other.value;
    }
};

// Edge Case 6: Function with callback
void processWithCallback(int data, std::function<void(int)> callback) {
    callback(data * 2);
}

void myCallback(int result) {
    std::cout << "Callback received: " << result << std::endl;
}

void useCallback() {
    processWithCallback(42, myCallback);
}

// Edge Case 7: Static member function
class Utility {
public:
    static void staticFunction() {
        std::cout << "Static function" << std::endl;
    }

    void memberFunction() {
        std::cout << "Member function" << std::endl;
        staticFunction();  // Calls static function
    }
};

// Edge Case 8: Inline function
inline int square(int x) {
    return x * x;
}

void useInline() {
    int result = square(5);
    std::cout << "Square: " << result << std::endl;
}
