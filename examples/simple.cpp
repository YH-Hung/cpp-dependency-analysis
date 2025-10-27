// Simple example with 3 functions forming 2 independent groups
// Group 1: helper() and process() are connected
// Group 2: independentFunction() is standalone

#include <iostream>

// Group 2: Independent function
void independentFunction() {
    double value = 42.0;
    std::cout << "Independent: " << value << std::endl;
}

// Group 1: Helper function
void helper() {
    int temp = 0;
    std::cout << "Helper: " << temp << std::endl;
}

// Group 1: Process function that calls helper()
void process() {
    helper();
    std::cout << "Processing..." << std::endl;
}
