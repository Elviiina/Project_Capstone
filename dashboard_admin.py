import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, Admin  
import time

st.set_page_config(page_title="Aerosite for Admin", page_icon=":airplane:", layout="wide")

st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #0077b6;
    }
    div.stButton > button {
        background-color: red; 
        color: white;
    }
    div.stButton > button:active {
        background-color: red; 
        color: white;
    }     
    </style>
    """, unsafe_allow_html=True)

def show_error(message):
    time.sleep(2)
    st.error(message)

try:
    with app.app_context():
        params = st.query_params
        session_token = params.get('sessionToken', [None])
        
        if not session_token or session_token is None:
            show_error("Tidak ada sesi yang ditemukan. Akses tidak diizinkan.")
        else:
            admin = Admin.query.filter_by(token=session_token).first()  
            if admin:
                with st.sidebar:
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col2:
                        st.image("static/images/logowarna.png", width=150)
                    st.markdown('<br>', unsafe_allow_html=True)
                    selected = option_menu("Menu", ["Overview", "Analysis", "Setting"],
                                        icons=['database', 'graph-up', 'gear'],
                                        menu_icon="list", default_index=0)

                # Konten untuk setiap opsi menu
                if selected == "Overview":
                    st.title("Overview")

                elif selected == "Analysis":
                    st.title("Isi Survei")

                elif selected == "Setting":
                    st.title("Setting")
                    if st.button("Log Out", key='logout_button', icon=':material/logout:'):
                        if "session_token" in st.session_state:
                            del st.session_state["session_token"]
                        admin.token = None
                        db.session.commit()
                        st.write(st.markdown("<meta http-equiv='refresh' content='0; url=http://localhost:5000/admin_logout'>", unsafe_allow_html=True))
            
            else:   
                show_error("Token tidak valid. Akses tidak diizinkan.")

except Exception as e:
    show_error(f"Error! Hubungi Admin jika menurut anda ini adalah kesalahan.")
