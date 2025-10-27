// Real-world example: Simple string utilities library
// Demonstrates realistic C++ code with multiple related and unrelated functions

#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

// Group 1: String trimming utilities (related functions)
bool isWhitespace(char c) {
    return std::isspace(static_cast<unsigned char>(c));
}

std::string trimLeft(const std::string& str) {
    auto it = std::find_if_not(str.begin(), str.end(), isWhitespace);
    return std::string(it, str.end());
}

std::string trimRight(const std::string& str) {
    auto it = std::find_if_not(str.rbegin(), str.rend(), isWhitespace);
    return std::string(str.begin(), it.base());
}

std::string trim(const std::string& str) {
    return trimLeft(trimRight(str));  // Calls both helpers
}

// Group 2: String splitting utilities (independent from Group 1)
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> result;
    std::string::size_type start = 0;
    std::string::size_type end = str.find(delimiter);

    while (end != std::string::npos) {
        result.push_back(str.substr(start, end - start));
        start = end + 1;
        end = str.find(delimiter, start);
    }

    result.push_back(str.substr(start));
    return result;
}

std::string join(const std::vector<std::string>& parts, const std::string& separator) {
    if (parts.empty()) return "";

    std::string result = parts[0];
    for (size_t i = 1; i < parts.size(); ++i) {
        result += separator + parts[i];
    }
    return result;
}

// Group 3: Case conversion utilities (independent from Groups 1 & 2)
std::string toLowerCase(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return result;
}

std::string toUpperCase(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return result;
}

// Group 4: String validation (independent utility)
bool startsWith(const std::string& str, const std::string& prefix) {
    if (prefix.length() > str.length()) return false;
    return str.compare(0, prefix.length(), prefix) == 0;
}

bool endsWith(const std::string& str, const std::string& suffix) {
    if (suffix.length() > str.length()) return false;
    return str.compare(str.length() - suffix.length(), suffix.length(), suffix) == 0;
}

bool contains(const std::string& str, const std::string& substring) {
    return str.find(substring) != std::string::npos;
}

// Group 5: String replacement (uses validation from Group 4)
std::string replace(const std::string& str, const std::string& from, const std::string& to) {
    if (from.empty() || !contains(str, from)) {  // Uses contains() from Group 4
        return str;
    }

    std::string result = str;
    size_t pos = 0;
    while ((pos = result.find(from, pos)) != std::string::npos) {
        result.replace(pos, from.length(), to);
        pos += to.length();
    }
    return result;
}
