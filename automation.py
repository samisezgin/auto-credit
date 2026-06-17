"""
Ogrenci Not Girisi Otomasyonu (Tab+Arrow)
==========================================
Klavye navigasyonu ile radio butonlari secer.
Cift tikla, sorulari cevapla, baslasin.
Her calistirmada 1 ogrenci islenir.
"""

import time
import random
import sys
import os
import json
from datetime import datetime

try:
    import pyautogui
except ImportError:
    print("HATA: pip install pyautogui")
    sys.exit(1)

pyautogui.FAILSAFE = True

NOT_SECENEKLERI = 4
LOG_DOSYASI = "log.txt"
AYAR_DOSYASI = "settings.json"


def log(mesaj):
    zaman = datetime.now().strftime("%H:%M:%S")
    satir = f"[{zaman}] {mesaj}"
    print(satir)
    with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
        f.write(satir + "\n")


def yorgunluk_katsayisi(satir_no):
    if satir_no < 20:
        return 1.0
    elif satir_no < 50:
        return 1.3
    elif satir_no < 100:
        return 1.6
    else:
        return 2.0


def ayar_oku():
    if not os.path.exists(AYAR_DOSYASI):
        return None
    try:
        with open(AYAR_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def ayar_kaydet(not_degeri, soru_sayisi, islenen):
    with open(AYAR_DOSYASI, "w", encoding="utf-8") as f:
        json.dump({
            "not": not_degeri,
            "soru_sayisi": soru_sayisi,
            "islenen_ogrenci": islenen,
            "tarih": datetime.now().isoformat()
        }, f, ensure_ascii=False)


def kullanici_sor():
    print(f"\n{'='*50}")
    print("  OGRENCI NOT GIRISI OTOMASYONU")
    print(f"{'='*50}")

    onceki = ayar_oku()
    varsayilan_soru = onceki.get("soru_sayisi", 80) if onceki else 80
    varsayilan_not = onceki.get("not") if onceki else None
    islenen = onceki.get("islenen_ogrenci", 0) if onceki else 0

    if onceki:
        not_str = str(varsayilan_not) if varsayilan_not else "Rastgele"
        print(f"\n  Son islem: {islenen} ogrenci islendi")
        print(f"  Enter'a basarsan onceki ayarlar kullanilir.")

    # Soru sayisi
    while True:
        cevap = input(f"\n  Soru sayisi({varsayilan_soru}): ").strip()
        if cevap == "":
            soru_sayisi = varsayilan_soru
            break
        try:
            soru_sayisi = int(cevap)
            if soru_sayisi > 0:
                break
            print("  0'dan buyuk bir sayi gir.")
        except ValueError:
            print("  Sayi gir.")

    # Not secimi
    varsayilan_not_str = str(varsayilan_not) if varsayilan_not else "Rastgele"
    while True:
        cevap = input(f"  Not({varsayilan_not_str}): ").strip()
        if cevap == "":
            not_degeri = varsayilan_not
            break
        if cevap in ("1", "2", "3", "4"):
            not_degeri = int(cevap)
            break
        print("  1-4 arasi bir sayi gir veya Enter'a bas.")

    return not_degeri, soru_sayisi, islenen


def geri_sayim(saniye=10):
    print(f"\n{'='*50}")
    print("  Tarayiciya gec, ilk radio butona tikla!")
    print("  Iptal: Ctrl+C | Durdurma: fareyi sol ust koseye cek")
    print(f"{'='*50}")
    for i in range(saniye, 0, -1):
        print(f"  {i}...", end=" ", flush=True)
        time.sleep(1)
    print("\nBasliyor!\n")


def not_tusla(not_degeri, katsayi):
    if not_degeri == 1:
        time.sleep(random.uniform(0.04, 0.12) * katsayi)
        pyautogui.press('right')
        time.sleep(random.uniform(0.04, 0.12) * katsayi)
        pyautogui.press('left')
    elif not_degeri == 2:
        time.sleep(random.uniform(0.04, 0.12) * katsayi)
        pyautogui.press('right')
    elif not_degeri == 3:
        for _ in range(2):
            time.sleep(random.uniform(0.04, 0.12) * katsayi)
            pyautogui.press('right')
    elif not_degeri == 4:
        for _ in range(3):
            time.sleep(random.uniform(0.04, 0.12) * katsayi)
            pyautogui.press('right')


def ogrenci_isle(soru_sayisi, notlar=None):
    for j in range(soru_sayisi):
        katsayi = yorgunluk_katsayisi(j)

        # 2x Tab: sira no sutununu atlayip not alanina gec
        time.sleep(random.uniform(0.1, 0.35) * katsayi)
        pyautogui.press('tab')
        time.sleep(random.uniform(0.05, 0.15) * katsayi)
        pyautogui.press('tab')

        # Not gir
        if notlar is not None:
            not_degeri = notlar
        else:
            not_degeri = random.randint(1, NOT_SECENEKLERI)

        not_tusla(not_degeri, katsayi)

        if (j + 1) % 20 == 0:
            log(f"  ... {j + 1}/{soru_sayisi} tamamlandi")


def main():
    not_degeri, soru_sayisi, islenen = kullanici_sor()

    not_str = str(not_degeri) if not_degeri else "Rastgele"
    print(f"\n{'='*50}")
    print(f"  Not       : {not_str}")
    print(f"  Soru      : {soru_sayisi}")
    print(f"  Ogrenci # : {islenen + 1}")
    print(f"{'='*50}")

    geri_sayim(10)

    # Ilk soruyu kullanici manuel isaretliyor (focus icin), geri kalani script yapar
    kalan = soru_sayisi - 1
    log(f"[Ogrenci {islenen + 1}] Basliyor... (Not={not_str}, Soru={soru_sayisi}, Script={kalan})")
    ogrenci_isle(kalan, notlar=not_degeri)

    islenen += 1
    ayar_kaydet(not_degeri, soru_sayisi, islenen)

    log(f"\n{'='*50}")
    log(f"TAMAMLANDI! Ogrenci {islenen} islendi.")
    log(f"Toplam islenen: {islenen}")


if __name__ == "__main__":
    main()
