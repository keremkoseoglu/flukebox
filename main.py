""" Entry point """

# todo
"""
mimari
    data source
        data source sınıfı (abstract)
            dosya listesi döndürecek yordam
        uygulama: directory
        uygulama: youtube
        uygulama: spotify
    data manager
        refresh yordamı: data source'ları dolaşıp URL'leri etc'de bir yere kaydetsin
    writer
        abstract writer (dict alacak, command line'dan da gelebilir zira)
        html writer (prime)
    engine
        verilen playlist'e ait dosyaları topla data manager'lardan
        duplicate'leri temizle sonuçlar arasından
        writer ile HTML yaz; HTML'de olması gerekenler:
            player, iframe ile sağda content açabilsin veya altta
            shuffle

gui
    config edit
    playlist'leri listele
    üret -> seçtiği playlist için engine'e gitsin
    refresh -> spotify ve youtube içeriklerini refresh edecek

readme
    sample config koy
    path.json editle, gerçek config'i göstersin
    youtube api al
    spotify api al
    bu bilgilerle configi güncelle
    screenshot
"""

from spotify_test import test1
print("hello world!")
# youtube sample call: https://www.googleapis.com/youtube/v3/playlistItems?key=xxx&playlistId=PLES3BCUQLP6hBBIODciynJr7VAgXSbonF
# youtube sample call 2: https://www.googleapis.com/youtube/v3/playlistItems?key=xxx&playlistId=PLES3BCUQLP6hBBIODciynJr7VAgXSbonF&part=contentDetails
test1()