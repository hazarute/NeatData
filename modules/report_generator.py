def print_report(rapor, module_changes=None):
    print("\n--- Detaylı Temizlik Raporu ---")
    print(f"Dosya: {rapor.get('dosya', 'Bilinmiyor')}")
    print(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk', '-')}")
    print(f"Son satır sayısı: {rapor.get('satir_sayisi_son', '-')}")
    print(f"Toplam silinen satır: {rapor.get('tekrar_silinen', 0) + (rapor.get('eksik_silinen', 0) if isinstance(rapor.get('eksik_silinen'), int) else 0)}")
    print(f"Tekrar eden satır silinen: {rapor.get('tekrar_silinen', '-')}")
    print(f"Eksik değer nedeniyle silinen/doldurulan: {rapor.get('eksik_silinen', '-')}")
    
    if module_changes:
        print("\nModül Bazlı Değişiklikler:")
        for mod, change in module_changes.items():
            print(f"  - {mod}: {change} hücre değişti")
    
    print("\nHata Özeti:")
    if rapor.get('hatalar'):
        for hata in rapor['hatalar']:
            print(f"  - {hata}")
    else:
        print("  - Hiç hata yok.")
    
    print("--------------------------------\n")

def generate_gui_report(rapor, module_changes=None, log_callback=None):
    """GUI için rapor üret, log_callback ile mesaj gönder"""
    if log_callback:
        log_callback(f"\n--- Detaylı Temizlik Raporu ---")
        log_callback(f"Dosya: {rapor.get('dosya', 'Bilinmiyor')}")
        log_callback(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk', '-')}")
        log_callback(f"Son satır sayısı: {rapor.get('satir_sayisi_son', '-')}")
        log_callback(f"Toplam silinen satır: {rapor.get('tekrar_silinen', 0) + (rapor.get('eksik_silinen', 0) if isinstance(rapor.get('eksik_silinen'), int) else 0)}")
        log_callback(f"Tekrar eden satır silinen: {rapor.get('tekrar_silinen', '-')}")
        log_callback(f"Eksik değer nedeniyle silinen/doldurulan: {rapor.get('eksik_silinen', '-')}")
        
        if module_changes:
            log_callback("\nModül Bazlı Değişiklikler:")
            for mod, change in module_changes.items():
                log_callback(f"  - {mod}: {change} hücre değişti")
        
        log_callback("\nHata Özeti:")
        if rapor.get('hatalar'):
            for hata in rapor['hatalar']:
                log_callback(f"  - {hata}")
        else:
            log_callback("  - Hiç hata yok.")
        
        log_callback("--------------------------------")