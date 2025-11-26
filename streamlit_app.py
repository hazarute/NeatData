import streamlit as st
import pandas as pd
from frontend.api_client import APIClient
import time

# -----------------------------------------------------------------------------
# 1. SAYFA KONFİGÜRASYONU VE CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NeatData",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    st.markdown("""
    <style>
        /* Genel Arkaplan */
        .stApp {
            background-color: #0f1117;
            color: #e5e7eb;
        }
        
        /* Sidebar Özelleştirme */
        [data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1f2937;
        }
        
        /* Başlıklar */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            color: #ffffff !important;
        }
        
        /* Kart Tasarımı (Configuration Step) */
        .custom-card {
            background-color: #1f2937; /* Dark gray */
            border: 1px solid #374151;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            transition: all 0.2s;
        }
        .custom-card:hover {
            border-color: #3b82f6; /* Primary Blue */
        }
        
        /* Butonlar */
        .stButton button {
            background-color: #2563eb;
            color: white;
            border-radius: 0.5rem;
            border: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: background-color 0.2s;
        }
        .stButton button:hover {
            background-color: #1d4ed8;
        }
        
        /* Status Indicator */
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: #22c55e; /* Green */
            margin-right: 8px;
            box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
        }
        
        /* Login Box */
        .login-box {
            background-color: #1f2937;
            padding: 2rem;
            border-radius: 1rem;
            border: 1px solid #374151;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. YARDIMCI FONKSİYONLAR
# -----------------------------------------------------------------------------
api_client = APIClient()

def render_sidebar():
    with st.sidebar:
        # Logo Alanı
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">ND</div>
            <div>
                <h3 style="margin:0; font-size: 16px; font-weight: 600;">NeatData</h3>
                <p style="margin:0; font-size: 12px; color: #9ca3af;">v1.0 Enterprise</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Menü
        st.markdown("### MENU")
        st.button("📊 Dashboard", use_container_width=True, type="secondary")
        st.button("clock_wise History", use_container_width=True, type="secondary")
        st.button("⚙️ Settings", use_container_width=True, type="secondary")
        
        st.divider()
        
        # API Status (En altta)
        health = api_client.check_health()
        status_color = "#22c55e" if health else "#ef4444"
        status_text = "API Connected" if health else "API Disconnected"
        
        st.markdown(f"""
        <div style="background-color: rgba(31, 41, 55, 0.5); padding: 12px; border-radius: 8px; display: flex; align-items: center; margin-top: auto;">
            <span style="width: 8px; height: 8px; background-color: {status_color}; border-radius: 50%; margin-right: 10px; box-shadow: 0 0 8px {status_color};"></span>
            <span style="font-size: 13px; color: #d1d5db; font-weight: 500;">{status_text}</span>
        </div>
        """, unsafe_allow_html=True)

def render_module_card(col, title, description, icon, key, default=False):
    """Özel CSS ile kart görünümü oluşturur ve içine toggle koyar."""
    with col:
        container = st.container()
        with container:
            # Kartın iç yapısı: Sol (İkon+Metin) - Sağ (Toggle)
            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                st.markdown(f"""
                <div class="custom-card" style="margin-bottom: 0; border: none; padding: 0; background: transparent;">
                    <div style="background-color: #374151; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                        <span style="font-size: 20px;">{icon}</span>
                    </div>
                    <div>
                        <div style="font-weight: 600; font-size: 15px; color: white;">{title}</div>
                        <div style="font-size: 12px; color: #9ca3af;">{description}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                # Streamlit Toggle'ı sağa hizala
                st.markdown("<br>", unsafe_allow_html=True) # Biraz boşluk
                is_checked = st.toggle("Aktif", key=key, value=default, label_visibility="collapsed")
    return is_checked

# -----------------------------------------------------------------------------
# 3. EKRANLAR
# -----------------------------------------------------------------------------

def login_screen():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="width: 60px; height: 60px; background: #3b82f6; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 16px;">
                <span style="font-size: 30px;">🧹</span>
            </div>
            <h2>Welcome to NeatData</h2>
            <p style="color: #9ca3af;">Please enter your API Key to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            api_key = st.text_input("API Key", type="password", placeholder="Enter your key here...")
            submitted = st.form_submit_button("Connect to Platform", use_container_width=True)
            
            if submitted:
                # Basit doğrulama (Gerçekte API'ye sorulabilir)
                if len(api_key) > 5:
                    st.session_state['api_key'] = api_key
                    api_client.set_api_key(api_key)
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid API Key format.")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #6b7280;">
            Default Dev Key: 9a2b6d23-ce71-4cbf-8b2d-c277ca34a2c2
        </div>
        """, unsafe_allow_html=True)

def dashboard_screen():
    render_sidebar()
    
    # Ana İçerik
    st.markdown("## Data Cleaning Pipeline")
    st.markdown("<p style='color: #9ca3af; margin-top: -10px;'>Upload, configure, and clean your datasets in seconds.</p>", unsafe_allow_html=True)
    
    # --- STEP 1: UPLOAD ---
    st.markdown("### 1. Upload Data")
    
    upload_col, _ = st.columns([1, 0.1]) # Genişlik ayarı
    with upload_col:
        # Streamlit file uploader'ı özel bir container içine alıyoruz
        with st.container():
            uploaded_file = st.file_uploader("Drag and drop your CSV file here", type=["csv"], label_visibility="collapsed")
            st.markdown('<p style="color: #9ca3af; font-size: 14px; margin-top: 10px;">Supported formats: CSV (Max 50MB)</p>', unsafe_allow_html=True)

    # Dosya Yükleme Mantığı
    if uploaded_file:
        if 'upload_id' not in st.session_state or st.session_state.get('uploaded_filename') != uploaded_file.name:
            with st.spinner("Uploading to secure storage..."):
                upload_id = api_client.upload_file(uploaded_file)
                if upload_id:
                    st.session_state['upload_id'] = upload_id
                    st.session_state['uploaded_filename'] = uploaded_file.name
                    st.toast(f"File uploaded successfully! ID: {upload_id}", icon="✅")
                else:
                    st.error("Upload failed. Please check API connection.")

    # --- STEP 2: CONFIGURATION ---
    if 'upload_id' in st.session_state:
        st.markdown("### 2. Configuration")
        st.markdown("<p style='color: #9ca3af; margin-bottom: 20px;'>Select the cleaning modules you want to apply.</p>", unsafe_allow_html=True)
        
        # Modülleri API'den çek
        modules_data = api_client.get_modules()
        core_modules = modules_data.get("core_modules", [])
        custom_modules = modules_data.get("custom_modules", [])
        
        selected_modules = []
        
        # Grid Layout (2 Sütunlu Kartlar)
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        
        # Manuel Mapping (Görsel ikonlar için)
        # API'den gelen key'lere göre ikon atıyoruz
        icon_map = {
            "drop_duplicates": "📄",
            "trim_spaces": "✂️",
            "standardize_headers": "Tt",
            "convert_types": "🔢",
            "handle_missing": "❓",
            "text_normalize": "🔤"
        }
        
        # Core Modülleri Listele
        cols = [row1_col1, row1_col2, row2_col1, row2_col2]
        current_col_idx = 0
        
        for mod in core_modules:
            col = cols[current_col_idx % 4]
            icon = icon_map.get(mod['key'], "🔧")
            
            if render_module_card(col, mod['name'], mod['description'], icon, mod['key']):
                selected_modules.append(mod['key'])
            
            current_col_idx += 1
            
        # Custom Modüller
        if custom_modules:
            st.markdown("#### Custom Plugins")
            c_col1, c_col2 = st.columns(2)
            for idx, mod in enumerate(custom_modules):
                col = c_col1 if idx % 2 == 0 else c_col2
                if render_module_card(col, mod['name'], "Custom Plugin", "🧩", mod['key']):
                    selected_modules.append(mod['key'])

        # --- STEP 3: ACTION ---
        st.markdown("### 3. Action")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Cleaning Pipeline", type="primary", use_container_width=True, disabled=len(selected_modules) == 0):
            with st.spinner("Processing data pipeline..."):
                result = api_client.run_pipeline(st.session_state['upload_id'], selected_modules)
                
                if result and result.get("status") == "success":
                    st.success("Pipeline completed successfully!")
                    
                    # Sonuçları Göster
                    result_data = result.get("result_data", {})
                    df_result = pd.DataFrame(result_data)
                    
                    st.markdown("#### Results Preview")
                    st.dataframe(df_result.head(50), use_container_width=True)
                    
                    # İstatistikler
                    m1, m2 = st.columns(2)
                    m1.metric("Original Rows", result.get('original_shape', [0])[0])
                    m2.metric("Cleaned Rows", result.get('cleaned_shape', [0])[0], delta_color="normal")
                    
                    # İndir
                    csv = df_result.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Cleaned CSV",
                        data=csv,
                        file_name=f"clean_{st.session_state['uploaded_filename']}",
                        mime="text/csv",
                        type="primary"
                    )
                else:
                    st.error("Pipeline failed. Check logs.")

# -----------------------------------------------------------------------------
# 4. MAIN ORCHESTRATOR
# -----------------------------------------------------------------------------
def main():
    inject_custom_css()
    
    # Session State'den API Key'i geri yükle (Sayfa yenilendiğinde client'ı güncellemek için)
    if 'api_key' in st.session_state:
        api_client.set_api_key(st.session_state['api_key'])
    
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        
    if not st.session_state['authenticated']:
        login_screen()
    else:
        dashboard_screen()

if __name__ == "__main__":
    main()
