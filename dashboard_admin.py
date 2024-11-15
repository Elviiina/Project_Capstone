import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, Admin  
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
                df = pd.read_csv("./dataset/Invistico_Airline.csv")
                with st.sidebar:
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col2:
                        st.image("static/images/logowarna.png", width=150)
                    st.markdown('<br>', unsafe_allow_html=True)
                    selected = option_menu("Menu", ["Overview", "Analysis", "Setting"],
                                        icons=['database', 'graph-up', 'gear'],
                                        menu_icon="list", default_index=0)

                if selected == "Overview":
                    st.title("Overview")
                    st.header("Deskripsi Data")
                    st.text(f"Total Jumlah Data: {df.shape[0]}")
                    st.text(f"Jumlah Fitur: {df.shape[1]}")
                    st.text("Dataset:")
                    st.dataframe(df.head())

                    st.header("Distribusi Kepuasan Pelanggan")
                    satisfaction_counts = df['satisfaction'].value_counts()
                    fig1, ax1 = plt.subplots()
                    ax1.pie(satisfaction_counts, labels=satisfaction_counts.index, autopct='%1.1f%%', startangle=90)
                    ax1.axis('equal')
                    st.pyplot(fig1)

                    st.header("Informasi Jenis Pelanggan")
                    customer_type_counts = df['Customer Type'].value_counts()
                    st.bar_chart(customer_type_counts)

                    st.header("Distribusi Fitur Demografis")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Distribusi Gender")
                        gender_counts = df['Gender'].value_counts()
                        st.bar_chart(gender_counts)

                    with col2:
                        st.subheader("Distribusi Usia")
                        fig2, ax2 = plt.subplots()
                        sns.histplot(df['Age'], kde=True, bins=20, ax=ax2)
                        st.pyplot(fig2)

                    st.subheader("Distribusi Kelas Penerbangan")
                    class_counts = df['Class'].value_counts()
                    st.bar_chart(class_counts)

                    st.subheader("Rata-rata Rating Kenyamanan")
                    comfort_features = ["Seat comfort", "Inflight wifi service", "Inflight entertainment", 
                                        "Food and drink", "Leg room service"]
                    comfort_ratings = df[comfort_features].mean()
                    st.bar_chart(comfort_ratings)

                elif selected == "Analysis":
                    st.title("Analysis")

                    st.header("Analisis Kepuasan Berdasarkan Kelas Penerbangan")
                    satisfaction_by_class = df.groupby(['Class', 'satisfaction']).size().unstack()
                    st.bar_chart(satisfaction_by_class)

                    st.header("Analisis Tipe Perjalanan Terhadap Kepuasan")
                    satisfaction_by_travel = df.groupby(['Type of Travel', 'satisfaction']).size().unstack()
                    st.bar_chart(satisfaction_by_travel)

                    st.header("Korelasi Antar Fitur Numerik")
                    numeric_features = ["Flight Distance", "Departure Delay in Minutes", "Arrival Delay in Minutes",
                                        "Seat comfort", "Inflight wifi service", "Inflight entertainment"]
                    correlation_matrix = df[numeric_features].corr()
                    fig3, ax3 = plt.subplots(figsize=(8, 6))
                    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax3)
                    st.pyplot(fig3)

                    st.header("Pengaruh Keterlambatan pada Kepuasan")
                    fig4, ax4 = plt.subplots()
                    sns.scatterplot(data=df, x="Departure Delay in Minutes", y="Arrival Delay in Minutes", hue="satisfaction", ax=ax4)
                    st.pyplot(fig4)

                    st.header("Pengaruh Fitur Kenyamanan terhadap Kepuasan")
                    comfort_features = ["Seat comfort", "Inflight wifi service", "Inflight entertainment", 
                                        "Food and drink", "Leg room service"]
                    for feature in comfort_features:
                        st.subheader(f"Pengaruh {feature}")
                        fig5, ax5 = plt.subplots()
                        sns.boxplot(data=df, x="satisfaction", y=feature, ax=ax5)
                        st.pyplot(fig5)

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
