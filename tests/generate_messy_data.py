import pandas as pd
import numpy as np
import random
import os

# Hedef dosya boyutu (MB)
TARGET_SIZE_MB = 50
FILE_NAME = "messy_cafe_data_50mb.csv"

print(f"--- {TARGET_SIZE_MB}MB Kirli Veri Üretimi Başlıyor ---")

# 1. Temel Veri Seti (Seed Data)
# Bu veriler, Fix Cafe plugin'inin düzelteceği türden hatalar içeriyor.
products = [
    "Latte", "Cappuccino", "Americano", "Espresso", "Turkish Coffee",
    "Filter Coffee", "Tea", "Herbal Tea", "Hot Chocolate", "Mocha",
    "Iced Latte", "Frappe", "Lemonade", "Orange Juice", "Water",
    "Soda", "Cheesecake", "Brownie", "Cookie", "Sandwich"
]

# Kategori Hataları (Büyük/Küçük Harf, Boşluk)
categories_messy = [
    "Hot Drinks", "hot drinks", "HOT DRINKS ", " Hot Drinks",
    "Cold Drinks", "cold drinks", "COLD DRINKS",
    "Desserts", "desserts ", " DESSERTS",
    "Food", "food", " FOOD "
]

# Fiyat Hataları (TL yazısı, Virgül)
def generate_messy_price():
    base_price = random.uniform(10, 80)
    error_type = random.choice(["clean", "tl_suffix", "comma", "both"])

    if error_type == "clean":
        return f"{base_price:.2f}"
    elif error_type == "tl_suffix":
        return f"{base_price:.2f} TL"
    elif error_type == "comma":
        return f"{base_price:.2f}".replace(".", ",")
    elif error_type == "both":
        return f"{base_price:.2f}".replace(".", ",") + " TL"

# 2. Büyük Veri Çoğaltma Döngüsü
# 50MB'a ulaşana kadar veri üreteceğiz.
chunks = []
total_rows = 0
current_size_mb = 0

while current_size_mb < TARGET_SIZE_MB:
    # Her döngüde 50.000 satırlık bir blok oluştur
    chunk_size = 50000
    
    data = {
        # Kirli Başlıklar (Boşluklu)
        " Product Name ": random.choices(products, k=chunk_size),
        " Category ": random.choices(categories_messy, k=chunk_size),
        # Fiyat sütunu string olacak
        "Price(TL)": [generate_messy_price() for _ in range(chunk_size)],
        # Rastgele sipariş ID'leri
        "Order ID": np.random.randint(1000, 99999, size=chunk_size),
        # Rastgele tarihler
        "Date": pd.date_range(start="2023-01-01", end="2023-12-31", periods=chunk_size).strftime("%Y-%m-%d")
    }
    
    df_chunk = pd.DataFrame(data)
    
    # Tekrar Eden Satırlar Ekle (Verinin %10'u kadar)
    duplicates = df_chunk.sample(frac=0.1)
    df_chunk = pd.concat([df_chunk, duplicates], ignore_index=True)
    
    chunks.append(df_chunk)
    total_rows += len(df_chunk)
    
    # Geçici boyutu hesapla (Tahmini)
    # Bellekteki boyut diskteki boyuttan farklı olabilir, bu kaba bir tahmin.
    current_size_mb = sum([chunk.memory_usage(deep=True).sum() for chunk in chunks]) / (1024 * 1024)
    print(f"Toplam Satır: {total_rows:,} | Tahmini Boyut: {current_size_mb:.2f} MB")

# 3. Birleştir ve Kaydet
print("Bloklar birleştiriliyor...")
full_df = pd.concat(chunks, ignore_index=True)

# Hedef boyuta tam ulaşmak için biraz kırp veya ekle (Opsiyonel, şu an gerek yok)
# full_df = full_df.iloc[:target_rows]

print(f"CSV dosyası yazılıyor: {FILE_NAME}...")
# index=False önemli, gereksiz boyut artışı olmasın.
full_df.to_csv(FILE_NAME, index=False)

final_size_mb = os.path.getsize(FILE_NAME) / (1024 * 1024)
print(f"--- İşlem Tamamlandı ---")
print(f"Dosya: {FILE_NAME}")
print(f"Son Boyut: {final_size_mb:.2f} MB")
print(f"Toplam Satır: {len(full_df):,}")
print("Artık bu dosyayı NeatData Streamlit arayüzüne yükleyebilirsin.")