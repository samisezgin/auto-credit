"""
Ogrenci Not Girisi Otomasyonu (Tab+Arrow)
==========================================
Unite bazli klavye navigasyonu ile radio butonlari secer.
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


def yorgunluk_katsayisi(toplam_satir):
    if toplam_satir < 20:
        return 1.0
    elif toplam_satir < 50:
        return 1.3
    elif toplam_satir < 100:
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


def ayar_kaydet(not_degeri, unite_sayisi, soru_per_unite, islenen):
    with open(AYAR_DOSYASI, "w", encoding="utf-8") as f:
        json.dump({
            "not": not_degeri,
            "unite_sayisi": unite_sayisi,
            "soru_per_unite": soru_per_unite,
            "islenen_ogrenci": islenen,
            "tarih": datetime.now().isoformat()
        }, f, ensure_ascii=False)


def sayi_sor(prompt, varsayilan):
    while True:
        cevap = input(f"  {prompt}({varsayilan}): ").strip()
        if cevap == "":
            return varsayilan
        try:
            val = int(cevap)
            if val > 0:
                return val
            print("  0'dan buyuk bir sayi gir.")
        except ValueError:
            print("  Sayi gir.")


def kullanici_sor():
    print(f"\n{'='*50}")
    print("  OGRENCI NOT GIRISI OTOMASYONU")
    print(f"{'='*50}")

    onceki = ayar_oku()
    v_unite = onceki.get("unite_sayisi", 10) if onceki else 10
    v_soru = onceki.get("soru_per_unite", 8) if onceki else 8
    v_not = onceki.get("not") if onceki else None
    islenen = onceki.get("islenen_ogrenci", 0) if onceki else 0

    if onceki:
        not_str = str(v_not) if v_not else "Rastgele"
        print(f"\n  Son islem: {islenen} ogrenci islendi")
        print(f"  Son ayar : Unite={v_unite}, Soru/unite={v_soru}, Not={not_str}")
        print(f"  Enter'a basarsan onceki ayarlar kullanilir.")

    unite_sayisi = sayi_sor("Unite sayisi", v_unite)
    soru_per_unite = sayi_sor("Soru/unite", v_soru)

    # Not secimi
    v_not_str = str(v_not) if v_not else "Rastgele"
    while True:
        cevap = input(f"  Not({v_not_str}): ").strip()
        if cevap == "":
            not_degeri = v_not
            break
        if cevap in ("1", "2", "3", "4"):
            not_degeri = int(cevap)
            break
        print("  1-4 arasi bir sayi gir veya Enter'a bas.")

    return not_degeri, unite_sayisi, soru_per_unite, islenen


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
        time.sleep(random.uniform(0.02, 0.06) * katsayi)
        pyautogui.press('right')
        time.sleep(random.uniform(0.02, 0.06) * katsayi)
        pyautogui.press('left')
    elif not_degeri == 2:
        time.sleep(random.uniform(0.02, 0.06) * katsayi)
        pyautogui.press('right')
    elif not_degeri == 3:
        for _ in range(2):
            time.sleep(random.uniform(0.02, 0.06) * katsayi)
            pyautogui.press('right')
    elif not_degeri == 4:
        for _ in range(3):
            time.sleep(random.uniform(0.02, 0.06) * katsayi)
            pyautogui.press('right')


def ogrenci_isle(unite_sayisi, soru_per_unite, notlar=None):
    toplam_satir = 0

    for u in range(unite_sayisi):
        unite_no = u + 1

        if u == 0:
            # Ilk unite: 1. soru manuel (kullanici tikladi), 2. sorudan basla
            baslangic = 1
            log(f"  Unite {unite_no}/{unite_sayisi} (1. soru manuel)")
        else:
            # Unite gecisi: 2 Tab + Enter
            katsayi = yorgunluk_katsayisi(toplam_satir)
            time.sleep(random.uniform(0.1, 0.35) * katsayi)
            pyautogui.press('tab')
            time.sleep(random.uniform(0.05, 0.15) * katsayi)
            pyautogui.press('tab')
            time.sleep(random.uniform(0.1, 0.3) * katsayi)
            pyautogui.press('enter')

            # Yeni unitenin 1. sorusu: 1 Tab + Arrow
            baslangic = 0
            log(f"  Unite {unite_no}/{unite_sayisi}")

        for j in range(baslangic, soru_per_unite):
            katsayi = yorgunluk_katsayisi(toplam_satir)

            if u == 0 or j > 0:
                # Normal soru: 2 Tab
                time.sleep(random.uniform(0.1, 0.35) * katsayi)
                pyautogui.press('tab')
                time.sleep(random.uniform(0.05, 0.15) * katsayi)
                pyautogui.press('tab')
            else:
                # Yeni unitenin 1. sorusu: 1 Tab
                time.sleep(random.uniform(0.1, 0.35) * katsayi)
                pyautogui.press('tab')

            # Not gir
            if notlar is not None:
                not_degeri = notlar
            else:
                not_degeri = random.randint(1, NOT_SECENEKLERI)

            not_tusla(not_degeri, katsayi)
            toplam_satir += 1

        log(f"    Unite {unite_no} tamamlandi ({soru_per_unite} soru)")


def main():
    not_degeri, unite_sayisi, soru_per_unite, islenen = kullanici_sor()

    toplam = unite_sayisi * soru_per_unite
    not_str = str(not_degeri) if not_degeri else "Rastgele"

    while True:
        print(f"\n{'='*50}")
        print(f"  Unite     : {unite_sayisi}")
        print(f"  Soru/unite: {soru_per_unite}")
        print(f"  Toplam    : {toplam} soru")
        print(f"  Not       : {not_str}")
        print(f"  Ogrenci # : {islenen + 1}")
        print(f"{'='*50}")

        geri_sayim(5)

        log(f"[Ogrenci {islenen + 1}] Basliyor... (Not={not_str}, {unite_sayisi} unite x {soru_per_unite} soru)")
        ogrenci_isle(unite_sayisi, soru_per_unite, notlar=not_degeri)

        islenen += 1
        ayar_kaydet(not_degeri, unite_sayisi, soru_per_unite, islenen)

        log(f"\n{'='*50}")
        log(f"TAMAMLANDI! Ogrenci {islenen} islendi.")
        log(f"Toplam islenen: {islenen}")

        print(f"\n{'='*50}")
        print("  Sonraki ogrenci icin Enter'a bas")
        print("  Cikmak icin 'q' yaz ve Enter'a bas")
        print(f"{'='*50}")
        cevap = input("  > ").strip().lower()
        if cevap == "q":
            log("Kullanici cikis yapti.")
            break
        log("Sonraki ogrenciye geciliyor...")


if __name__ == "__main__":
    main()
