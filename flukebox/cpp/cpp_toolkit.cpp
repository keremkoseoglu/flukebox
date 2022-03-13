#include <iostream>
#include <string>
#include <algorithm>

std::string replace_all(std::string str, const std::string& from, const std::string& to) {
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // Handles case where 'to' is a substring of 'from'
    }
    return str;
}

void purify_name_cpp(std::string* name) {
    std::string tmp = *name;
    std::transform(tmp.begin(), tmp.end(), tmp.begin(), ::tolower);
    *name = tmp;
    *name = replace_all(*name, "ı", "i");
    *name = replace_all(*name, "ğ", "g");
    *name = replace_all(*name, "ü", "u");
    *name = replace_all(*name, "ş", "s");
    *name = replace_all(*name, "ö", "o");
    *name = replace_all(*name, "ç", "c");
    *name = replace_all(*name, "Ğ", "g");
    *name = replace_all(*name, "Ü", "u");
    *name = replace_all(*name, "Ş", "s");
    *name = replace_all(*name, "İ", "i");
    *name = replace_all(*name, "Ö", "o");
    *name = replace_all(*name, "Ç", "c");
}

void purify_song_name_cpp(std::string* name) {
    *name = replace_all(*name, "'", " ");
    *name = replace_all(*name, "\"", " ");
    *name = replace_all(*name, "(", " ");
    *name = replace_all(*name, ")", " ");
    *name = replace_all(*name, ";", " ");
    *name = replace_all(*name, "<", " ");
    *name = replace_all(*name, ">", " ");
}

extern "C" {
    void purify_name(char* name) {
        std::string name2 = "";
        name2 += name; 
        purify_name_cpp(&name2);
        strcpy(name, name2.c_str());
    }

    void purify_song_name(char* name) {
        std::string name2 = "";
        name2 += name; 
        purify_song_name_cpp(&name2);
        strcpy(name, name2.c_str());
    }
}

int main() {
    char test[15] = "XxÜxı";
    purify_name(test);
    std::cout << test;
}