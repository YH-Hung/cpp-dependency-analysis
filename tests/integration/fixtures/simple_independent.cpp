// Simple test file with independent functions
// Expected: 3 groups (each function is independent)

void functionA() {
    // Independent function - does not call anyone
    int x = 42;
    x = x + 1;
}

void functionB() {
    // Independent function - does not call anyone
    double y = 3.14;
    y = y * 2.0;
}

void functionC() {
    // Independent function - does not call anyone
    bool z = true;
    z = !z;
}
