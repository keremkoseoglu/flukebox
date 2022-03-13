"""
g++ -c -fPIC cpp_toolkit.cpp -o cpp_toolkit.o
g++ -shared -o cpp_toolkit.so cpp_toolkit.o
"""

from ctypes import cdll
lib = cdll.LoadLibrary("/Users/kerem/Dropbox/Mac/Documents/software/Kerem/Development/flukebox/flukebox/cpp/cpp_toolkit.so")

def purify_name(name: str) -> str:
    name2 = name.encode(encoding="utf-8", errors="ignore")
    lib.purify_name(name2)
    return name2.decode(encoding="utf-8", errors="ignore")[:len(name)]

def purify_song_name(name: str) -> str:
    name2 = name.encode(encoding="utf-8", errors="ignore")
    lib.purify_song_name(name2)
    return name2.decode(encoding="utf-8", errors="ignore")[:len(name)]

# x = purify_name("xxığüşiöçIĞÜŞİÇÖdd")
# print(x)
