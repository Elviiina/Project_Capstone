import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, Admin  

def show_error(message):
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
                st.write(f"Admin Token: {admin.token}")  

                def show_dashboard():
                    st.title("Dashboard Admin")
                    st.write("Ini adalah halaman Dashboard.")
                    
                def show_survey():
                    st.title("Survey")
                    st.write("Ini adalah halaman Survey.")
                    
                def show_users_account():
                    st.title("Users Account")
                    st.write("Ini adalah halaman Users Account.")
                    
                with st.sidebar:
                    selected = option_menu(
                        menu_title="Main Menu", 
                        options=["Dashboard", "Survey", "Users Account"], 
                        icons=["house", "bar-chart", "person"],  
                        menu_icon="cast",  
                        default_index=0, 
                    )
                    
                if selected == "Dashboard":
                    show_dashboard()
                elif selected == "Survey":
                    show_survey()
                elif selected == "Users Account":
                    show_users_account()
            else:   
                show_error("Token tidak valid. Akses tidak diizinkan.")

except Exception as e:
    show_error(f"Terjadi kesalahan pada url anda!")
