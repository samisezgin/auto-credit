"""
Test Runner - Tab+Arrow Klavye Navigasyonu (Unite bazli)
========================================================
3 unite x 7 soru = 21 buton. Bot algilandi anda keser.

    python test/test_runner.py
"""

import sys
import os
import time
import random

try:
    import pyautogui
except ImportError:
    print("pip install pyautogui")
    sys.exit(1)

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("pip install selenium")
    sys.exit(1)

UNITE_SAYISI = 3
SORU_PER_UNITE = 7
TOPLAM = UNITE_SAYISI * SORU_PER_UNITE


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


def main():
    print("=" * 50)
    print("  TAB+ARROW BOT ALGILAMA TESTI")
    print(f"  {UNITE_SAYISI} unite x {SORU_PER_UNITE} soru = {TOPLAM} buton")
    print("=" * 50)

    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    html = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
    driver.get("file:///" + html.replace("\\", "/"))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "IOMToolbarActive1_btnKaydet"))
    )
    time.sleep(1)
    print("Sayfa yuklendi.\n")

    # Skorlari sifirla, ilk radio butona focus ver
    driver.execute_script("window.skorSifirla(); window.scrollTo(0,0);")
    time.sleep(0.3)
    driver.execute_script("""
        var btn = document.querySelectorAll('input[type="radio"]')[0];
        btn.scrollIntoView({block: 'center'});
        btn.focus();
    """)
    time.sleep(0.3)

    # Geri sayim
    print("Ilk radio butona focus verildi.")
    for s in range(5, 0, -1):
        print(f"  {s}...", end=" ", flush=True)
        time.sleep(1)
    print("\nBasliyor!\n")

    not_degeri = random.randint(1, 4)
    print(f"Test notu: {not_degeri} (tum satirlara ayni not)\n")

    bot_yakalandi = False
    yakalama_adimi = 0
    toplam_satir = 0

    for u in range(UNITE_SAYISI):
        unite_no = u + 1

        if u == 0:
            # Ilk unite: 1. soru manuel (focus zaten verildi), 2. sorudan basla
            baslangic = 1
            print(f"  Unite {unite_no}/{UNITE_SAYISI} (1. soru manuel)")
        else:
            # Unite gecisi: 2 Tab + Enter
            katsayi = 1.0 + (toplam_satir / 100)
            time.sleep(random.uniform(0.1, 0.35) * katsayi)
            pyautogui.press('tab')
            time.sleep(random.uniform(0.05, 0.15) * katsayi)
            pyautogui.press('tab')
            time.sleep(random.uniform(0.1, 0.3) * katsayi)
            pyautogui.press('enter')
            baslangic = 0
            print(f"  Unite {unite_no}/{UNITE_SAYISI}")

        for j in range(baslangic, SORU_PER_UNITE):
            katsayi = 1.0 + (toplam_satir / 100)

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

            not_tusla(not_degeri, katsayi)
            toplam_satir += 1

            # Bot kontrolu her 7 soruda
            if toplam_satir % SORU_PER_UNITE == 0:
                skor = driver.execute_script("return window.getBotSkor();")
                if skor and skor.get("botAlgilandi"):
                    bot_yakalandi = True
                    yakalama_adimi = toplam_satir
                    print(f"\n  BOT ALGILANDI! ({yakalama_adimi}. soruda yakalandi)")
                    break

        if bot_yakalandi:
            break
        print(f"    Unite {unite_no} tamamlandi")

    # Sonuclari oku
    secilen = driver.execute_script(
        "return document.querySelectorAll('input[type=\"radio\"]:checked').length;"
    )
    skor = driver.execute_script("return window.getBotSkor();")
    driver.quit()

    toplam_skor = skor.get("toplam", 0)
    karar = skor.get("karar", "?")
    # Ilk unite 1. soru manuel, script toplam_satir kadar isledi
    beklenen = TOPLAM - 1

    print(f"\n{'=' * 50}")
    print(f"  SONUC")
    print(f"{'=' * 50}")
    print(f"  Secilen Buton : {secilen}/{TOPLAM}")
    print(f"  Script isledi : {toplam_satir}/{beklenen}")
    print(f"  Toplam Skor   : {toplam_skor}")
    print(f"  Karar         : {karar}")
    print(f"  Detaylar:")
    print(f"    isTrusted ihlali  : {skor.get('trusted', 0)}")
    print(f"    Sabit aralik      : {skor.get('timing', 0)}")
    print(f"    Ayni piksel       : {skor.get('pixel', 0)}")
    print(f"    Hiz asimi         : {skor.get('speed', 0)}")
    print(f"    Fare hareketsiz   : {skor.get('nomouse', 0)}")

    if bot_yakalandi:
        print(f"\n  FAIL - Bot {yakalama_adimi}. soruda yakalandi!")
    elif karar == "INSAN":
        print(f"\n  BASARILI - Sistem bizi INSAN olarak gordu.")
    else:
        print(f"\n  DIKKAT - Karar: {karar}")
    print("=" * 50)


if __name__ == "__main__":
    main()
