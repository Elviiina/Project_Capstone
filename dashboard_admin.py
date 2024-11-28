import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, Admin  
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Aerosite for Admin", page_icon=":airplane:", layout="wide")

# CSS untuk navbar
st.markdown("""
    <style>
    .navbar {
        background-color: #0077b6;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .navbar .logo img {
        height: 40px;
    }
    .navbar .title-section {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .navbar .title {
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin: 0;
    }
    .navbar .profile {
        display: flex;
        align-items: center;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .navbar .profile img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        border: 2px solid white;
    }
    .navbar .filter-dropdown {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px 10px;
        font-size: 14px;
        color: #0077b6;
    }
    </style>
    """, unsafe_allow_html=True)

# Navbar dengan filter
st.markdown("""
    <div class="navbar">
        <div class="logo">
            <img src="https://asset.cloudinary.com/dv94ldeq4/bbd6323c21ba53f2d9bfdc3dec89a7b5" alt="Logo">
        </div>
        <div class="profile">
            <img src="https://via.placeholder.com/40?text=A" alt="Admin">
            Admin123
        </div>
    </div>
    """, unsafe_allow_html=True)

response = requests.get('http://127.0.0.1:5000/statistics')
                
if response.status_code == 200:
    stats = response.json()
    survey_count = stats['survey_count']
    satisfied_count = stats['satisfied_count']
    dissatisfied_count = stats['dissatisfied_count']
else:
    st.error("Data gagal dimuat")
    survey_count = 0
    satisfied_count = 0
    dissatisfied_count = 0

df = pd.read_csv("./dataset/Invistico_Airline.csv")

# survey_filled = df[df['survey_filled'] == True]  
comfort_features = [
    "Seat comfort", "Inflight wifi service", "Inflight entertainment", 
    "Food and drink", "Leg room service"
]

# Filter data yang sudah mengisi rating
survey_filled = df[df[comfort_features].notnull().all(axis=1)]

# Hitung rata-rata rating
average_rating = survey_filled[comfort_features].mean().mean()


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

                # Navbar horizontal
                selected = option_menu(
                    menu_title=None,
                    options=["Overview", "Analysis", "Setting"],
                    icons=['database', 'graph-up', 'gear'],
                    menu_icon="cast",
                    default_index=0,
                    orientation="horizontal"
                )
                
                # Metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric(label="Total Pengguna Isi Survei", value=survey_count)
                with col2:
                    st.metric(label="Total Satisfied", value=satisfied_count)
                with col3:
                    st.metric(label="Total Dissatisfied", value=dissatisfied_count)
                with col4:
                    st.metric(label="Average Rating", value=f"{average_rating:.2f}")
                # with col5:
                #     st.metric(label="Satisfaction Rate", value=data["Satisfaction Rate"])   
                

                if selected == "Overview":
                    st.title("Overview")
                    st.header("Deskripsi Data")
                    st.text(f"Total Jumlah Data: {df.shape[:0]}")
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