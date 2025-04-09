from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Chrome ayarları
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda açmak için
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriver yolunu ayarla (eğer gerekiyorsa)
service = Service("/usr/local/bin/chromedriver")

# WebDriver'ı başlat
driver = webdriver.Chrome(service=service, options=chrome_options)

# Google Trends sayfasını aç
keyword = "ekonomi"
url = f"https://trends.google.com/trends/explore?geo=TR&q={keyword}"
driver.get(url)

time.sleep(5)  # Sayfanın yüklenmesini bekle

# Sayfanın başarıyla yüklendiğini test et
print("Sayfa başlığı:", driver.title)

# Örnek: bir veri görseli (grafik alanı) var mı?
try:
    element = driver.find_element(By.CLASS_NAME, "fe-related-queries")
    print("✅ İlgili sorgular bölümü bulundu!")
except:
    print("⚠️ İlgili sorgular bölümü bulunamadı. Sayfa farklı yüklenmiş olabilir.")

driver.quit()
