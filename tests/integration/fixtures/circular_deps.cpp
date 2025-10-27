// Test file with circular dependencies
// Expected: 1 group with circular dependency (funcA <-> funcB)

// Forward declarations
void funcA();
void funcB();

void funcA() {
    // Calls funcB - creates circular dependency
    funcB();
}

void funcB() {
    // Calls funcA - completes the cycle
    funcA();
}
