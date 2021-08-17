import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

linkler = []
headers = {"User-Agent": "Super Bot Power Level Over 9000"}

# 95 sayfa icin ilan linklerini al
for i in range(2, 97):
    r = requests.get("https://www.hepsiemlak.com/kiralik?page={}".format(i), headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    sayfalar = soup.find_all("div", attrs={"class": "listing-item"})
    for sayfa in sayfalar:
        linkler.append(sayfa.find("a").get("href"))  #linkleri dizide tut

#ozellikleri kaydetmek icin dizi olustur
dataset = []

# her bir sayfa linkinin icine gir
for link in linkler:
    r = requests.get("https://www.hepsiemlak.com{}".format(link), headers=headers)
    print("https://www.hepsiemlak.com{}".format(link))
    soup = BeautifulSoup(r.content, "html.parser")

    # ev fiyatları
    fiyat = soup.find("p", attrs={"class": "fontRB fz24 price"}).text.strip().replace(" TL", "")

    # alacagimiz ozellikler spec-item classının altında bulunuyor
    ozellikler = soup.find_all("li", attrs={"class": "spec-item"})

    # her bir ilan icin tek tek ozellikleri al
    for ozellik in ozellikler:
        text = ozellik.find_all("span")[0].text
        if text == "Oda + Salon Sayısı":
            oda = ozellik.find_all("span")[1].text.strip()

        if text == "Brüt / Net M2":
            brut = ozellik.find_all("span")[1].text.strip().replace("m2", "")

        if text == "Brüt / Net M2":
            net = ozellik.find_all("span")[2].text.strip().replace("/ ", "").replace("m2", "")

        if text == "Bina Yaşı":
            yas = ozellik.find_all("span")[1].text.strip().replace(" Yaşında", "").replace("Sıfır Bina", "0")

        if text == "Kat Sayısı":
            kat = ozellik.find_all("span")[1].text.strip().replace(" Katlı", "")

        if text == "Eşya Durumu":
            esyali_mi = ozellik.find_all("span")[1].text.strip().replace("Eşyalı Değil", "0").replace("Eşyalı", "1")

        if text == "Banyo Sayısı":
            banyo = ozellik.find_all("span")[1].text.strip()

        if text == "Depozito":
            depozito = ozellik.find_all("span")[1].text.strip().replace(" TL", "")

    # print("fiyat ", fiyat)
    # print("oda ", oda)
    # print("brut ", brut)
    # print("net ", net)
    # print("yas ", yas)
    # print("kat ", kat)
    # print("esyali ", esyali_mi)
    # print("banyo ", banyo)
    # print("depozito ", depozito)

    # ev ilanı icin alinan ozellikleri diziye kaydet
    dataset.append([fiyat, oda, brut, net, yas, kat, esyali_mi, banyo, depozito])

df = pd.DataFrame(dataset)
df.columns = ["fiyat", "oda", "brut", "net", "yas", "kat", "esyali_mi", "banyo", "depozito"]
df.to_excel("kiralik.xlsx")