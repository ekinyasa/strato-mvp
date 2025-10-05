# trends_dashboard.py
import streamlit as st
from serpapi_fetcher import fetch_trends_with_serpapi
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale
import pandas as pd

st.set_page_config(page_title="Google Trend Grafiği", layout="wide")
st.title("📈 Google Trends Zaman Serisi")

keyword = st.text_input("🔍 Anahtar kelimeyi girin:", "ekonomi")

if keyword:
    with st.spinner("Veri getiriliyor..."):
        try:
            data = fetch_trends_with_serpapi(keyword)
            st.write("🔎 Aranan kelime:", keyword)
            st.write("📦 Gelen veri:", data)
            # Tarih ve değerleri DataFrame'e dönüştür
            df = pd.DataFrame(data)

            
            """
            try:
                locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")
            except locale.Error:
                st.warning("⚠️ Sisteminizde 'tr_TR.UTF-8' yerel ayarı yüklü değil. Tarihler İngilizce görünebilir.")
            """

            # Tarihi datetime'a çevir, sıralı hale getir
            # Haftalık aralıktaki ilk tarihi al: "Apr 7 – 13, 2024" -> "Apr 7, 2024"
            df["clean_date"] = df["date"].str.extract(r"^([A-Za-z]+ \d{1,2}),?") + ", " + df["date"].str.extract(r"(\d{4})")
            df["datetime"] = pd.to_datetime(df["clean_date"], errors="coerce")
            df = df.dropna(subset=["datetime"]).sort_values("datetime")

            # Grafik çizimi
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df["datetime"], df["value"], marker="o", linestyle="-", color="steelblue")

            ax.set_title(f"'{keyword}' için Google Trends Zaman Serisi", fontsize=14)
            ax.set_xlabel("Tarih", fontsize=12)
            ax.set_ylabel("Trend Değeri", fontsize=12)

            # Tarih formatı ve eksen ayarları
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            fig.autofmt_xdate(rotation=45)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"Hata oluştu: {e}")
