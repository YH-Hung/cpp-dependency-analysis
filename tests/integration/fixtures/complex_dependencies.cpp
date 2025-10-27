// Complex test file with function dependencies
// Expected: 2 groups
// Group 1: helper, process, analyze (3 functions, connected)
// Group 2: independentFunction (1 function, isolated)

void helper() {
    // Helper function - called by others
    int temp = 0;
}

void process() {
    // Calls helper
    helper();
    int data = 100;
}

void analyze() {
    // Calls both process and helper
    process();
    helper();
}

void independentFunction() {
    // Separate group - calls no one in this file
    double value = 42.0;
}
