"""
Test Runner - Tab+Arrow Klavye Navigasyonu
===========================================
Tek test: 1 ogrenci (80 buton), saf klavye, bot algilandi anda keser.

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


def main():
    print("=" * 50)
    print("  TAB+ARROW BOT ALGILAMA TESTI")
    print("  1 ogrenci, 80 buton, saf klavye")
    print("=" * 50)

    # Chrome ac
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

    # Skorlari sifirla, ilk radio butona focus ver (gercek sistemde kullanici manuel yapar)
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

    # Sabit not sec (1-4 arasi)
    not_degeri = random.randint(1, 4)
    print(f"Test notu: {not_degeri} (tum satirlara ayni not)\n")

    # 80 buton dongusu
    bot_yakalandi = False
    yakalama_adimi = 0

    for i in range(80):
        katsayi = 1.0 + (i / 100)

        # Once 2x Tab: sira no sutununu atlayip not alanina gec
        time.sleep(random.uniform(0.1, 0.35) * katsayi)
        pyautogui.press('tab')
        time.sleep(random.uniform(0.05, 0.15) * katsayi)
        pyautogui.press('tab')

        # Sonra arrow ile not gir
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

        if (i + 1) % 20 == 0:
            print(f"  ... {i + 1}/80 tamamlandi")

        # Her 10 butonda bot kontrolu
        if (i + 1) % 10 == 0:
            skor = driver.execute_script("return window.getBotSkor();")
            if skor and skor.get("botAlgilandi"):
                bot_yakalandi = True
                yakalama_adimi = i + 1
                print(f"\n  BOT ALGILANDI! ({yakalama_adimi}. butonda yakalandi)")
                break

    # Kaydet
    if not bot_yakalandi:
        time.sleep(random.uniform(0.3, 0.7))
        pyautogui.press('enter')
        time.sleep(1)
        try:
            driver.switch_to.alert.accept()
        except Exception:
            pass

    # Sonuclari oku
    secilen = driver.execute_script(
        "return document.querySelectorAll('input[type=\"radio\"]:checked').length;"
    )
    skor = driver.execute_script("return window.getBotSkor();")
    driver.quit()

    # Rapor
    toplam = skor.get("toplam", 0)
    karar = skor.get("karar", "?")

    print(f"\n{'=' * 50}")
    print(f"  SONUC")
    print(f"{'=' * 50}")
    print(f"  Secilen Buton : {secilen}/80")
    print(f"  Toplam Skor   : {toplam}")
    print(f"  Karar         : {karar}")
    print(f"  Detaylar:")
    print(f"    isTrusted ihlali  : {skor.get('trusted', 0)}")
    print(f"    Sabit aralik      : {skor.get('timing', 0)}")
    print(f"    Ayni piksel       : {skor.get('pixel', 0)}")
    print(f"    Hiz asimi         : {skor.get('speed', 0)}")
    print(f"    Fare hareketsiz   : {skor.get('nomouse', 0)}")

    if bot_yakalandi:
        print(f"\n  FAIL - Bot {yakalama_adimi}. butonda yakalandi!")
    elif karar == "INSAN":
        print(f"\n  BASARILI - Sistem bizi INSAN olarak gordu.")
    else:
        print(f"\n  DIKKAT - Karar: {karar}")
    print("=" * 50)


if __name__ == "__main__":
    main()
