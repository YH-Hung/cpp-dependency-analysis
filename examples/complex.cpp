// Complex example with multiple groups, circular dependencies, and templates
// Tests: circular deps, templates, overloading, larger graphs

#include <vector>
#include <string>
#include <iostream>

// Group 1: Circular dependency (A <-> B)
void functionA();
void functionB();

void functionA() {
    std::cout << "Function A" << std::endl;
    // Circular call to B
    if (false) functionB();
}

void functionB() {
    std::cout << "Function B" << std::endl;
    // Circular call to A
    if (false) functionA();
}

// Group 2: Template functions
template<typename T>
T add(T a, T b) {
    return a + b;
}

template<typename T>
T multiply(T a, T b) {
    T result = add(a, b);  // Calls add
    return result * a;
}

// Group 3: Overloaded functions (independent group)
void process(int value) {
    std::cout << "Processing int: " << value << std::endl;
}

void process(double value) {
    std::cout << "Processing double: " << value << std::endl;
}

void process(const std::string& value) {
    std::cout << "Processing string: " << value << std::endl;
}

// Group 4: Chain of calls (C -> D -> E)
void functionE() {
    std::cout << "Function E (leaf)" << std::endl;
}

void functionD() {
    std::cout << "Function D" << std::endl;
    functionE();
}

void functionC() {
    std::cout << "Function C" << std::endl;
    functionD();
}

// Group 5: Standalone complex function
void standaloneComplex(const std::vector<int>& data) {
    std::cout << "Standalone processing " << data.size() << " items" << std::endl;
}
