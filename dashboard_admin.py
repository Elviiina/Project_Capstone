import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, Admin  
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

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
                    st.subheader("Deskripsi Data")
                    st.text(f"Total Jumlah Data: {df.shape[0]}")
                    st.text(f"Jumlah Fitur: {df.shape[1]}")
                    st.text("Dataset:")
                    st.dataframe(df)

                    st.subheader("Distribusi Kepuasan Pelanggan")
                    satisfaction_counts = df['satisfaction'].value_counts()
                    fig1 = px.pie(satisfaction_counts, 
                                names=satisfaction_counts.index, 
                                values=satisfaction_counts.values, 
                                title="Distribusi Kepuasan Pelanggan",
                                color=satisfaction_counts.index,  
                                color_discrete_map={"satisfied": "blue", "dissatisfied": "red"})  
                    st.plotly_chart(fig1)

                    st.subheader("Informasi Jenis Pelanggan")
                    customer_type_counts = df['Customer Type'].value_counts()
                    fig2 = px.bar(customer_type_counts, 
                                x=customer_type_counts.index, 
                                y=customer_type_counts.values, 
                                title="Informasi Jenis Pelanggan", 
                                color=customer_type_counts.index,
                                color_discrete_map={"Loyal Customer": "#1E90FF", "disloyal Customer": "#D9534F"},
                                labels={"Customer Type":"Jenis Pelanggan", "y":"Jumlah"})  
                    st.plotly_chart(fig2)

                    st.subheader("Distribusi Fitur Demografis")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        gender_counts = df['Gender'].value_counts()
                        fig3 = px.bar(gender_counts, 
                                    x=gender_counts.index, 
                                    y=gender_counts.values, 
                                    title="Distribusi Gender",
                                    color=gender_counts.index,
                                    color_discrete_map={"Male": "#1E90FF", "Female": "#FF69B4"},
                                    category_orders={"Gender": ["Male", "Female"]},
                                    labels={"Gender":"Jenis Kelamin", "y":"Jumlah"}) 
                        st.plotly_chart(fig3)

                    with col2:
                        fig4 = px.histogram(df, x='Age', nbins=20, title="Distribusi Usia", marginal="box")
                        fig4.update_layout(
                            xaxis_title="Usia", 
                            yaxis_title="Jumlah"
                        )
                        st.plotly_chart(fig4)

                    st.subheader("Distribusi Kelas Penerbangan")
                    class_counts = df['Class'].value_counts()
                    fig5 = px.bar(class_counts, 
                                x=class_counts.index, 
                                y=class_counts.values, 
                                title="Distribusi Kelas Penerbangan", 
                                color=class_counts.index, 
                                color_discrete_map={"Eco": "#A9A9A9", "Eco Plus": "#006400", "Business": "#1F4E79"},
                                category_orders={"Class": ["Business", "Eco Plus", "Eco"]},
                                labels={"Class":"Kelas Penerbangan", "y":"Jumlah"})
                    st.plotly_chart(fig5)

                    st.subheader("Rata-rata Rating Kenyamanan")
                    comfort_features = ["Seat comfort", "Food and drink", "Inflight wifi service", "Inflight entertainment", "Leg room service"]
                    comfort_ratings = df[comfort_features].mean()
                    fig6 = px.bar(comfort_ratings, 
                                x=comfort_ratings.index, 
                                y=comfort_ratings.values, 
                                title="Rata-rata Rating Kenyamanan",
                                color=comfort_ratings.values,
                                color_continuous_scale="Blues", range_color=[2, 4],
                                labels={"index":"Fitur Kenyamanan", "y":"Rata-rata"}) 
                    st.plotly_chart(fig6)

                elif selected == "Analysis":
                    st.title("Analysis")

                    st.subheader("Analisis Kepuasan Berdasarkan Kelas Penerbangan")
                    satisfaction_by_class = df.groupby(['Class', 'satisfaction']).size().unstack()
                    fig7 = px.bar(satisfaction_by_class, 
                                barmode='group', 
                                title="Kepuasan Berdasarkan Kelas Penerbangan", 
                                color=satisfaction_by_class.index,
                                color_discrete_map={"Eco": "#A9A9A9", "Eco Plus": "#006400", "Business": "#1F4E79"},
                                category_orders={"Class": ["Business", "Eco Plus", "Eco"]},
                                labels={"Class":"Kelas Penerbangan", "value":"Jumlah Kepuasan"})  
                    st.plotly_chart(fig7)

                    st.subheader("Analisis Tipe Perjalanan Terhadap Kepuasan")
                    satisfaction_by_travel = df.groupby(['Type of Travel', 'satisfaction']).size().unstack()
                    fig8 = px.bar(satisfaction_by_travel, 
                                barmode='group', 
                                title="Tipe Perjalanan Terhadap Kepuasan", 
                                color=satisfaction_by_travel.index,
                                color_discrete_map={"Personal Travel": "#ADD8E6", "Business travel": "#2C3E50"},
                                labels={"Type of Travel":"Tipe Perjalanan", "value":"Jumlah Kepuasan"})  
                    st.plotly_chart(fig8)

                    st.subheader("Korelasi Antar Fitur Numerik")
                    numeric_features = ["Flight Distance", "Departure Delay in Minutes", "Arrival Delay in Minutes", "Seat comfort", "Inflight wifi service", "Inflight entertainment"]
                    correlation_matrix = df[numeric_features].corr()
                    fig9 = px.imshow(correlation_matrix, text_auto=True, title="Korelasi Antar Fitur Numerik", color_continuous_scale="RdBu")
                    st.plotly_chart(fig9)

                    st.subheader("Pengaruh Keterlambatan pada Kepuasan")
                    fig10 = px.scatter(df, 
                                    x="Departure Delay in Minutes", 
                                    y="Arrival Delay in Minutes", 
                                    color="satisfaction", 
                                    title="Pengaruh Keterlambatan pada Kepuasan",
                                    color_discrete_map={"satisfied": "blue", "dissatisfied": "red"})  
                    st.plotly_chart(fig10)

                    st.subheader("Pengaruh Fitur Kenyamanan terhadap Kepuasan")
                    comfort_features = ["Seat comfort", "Inflight wifi service", "Inflight entertainment", "Food and drink", "Leg room service"]
                    for feature in comfort_features:
                        fig11 = px.box(df, 
                                    x="satisfaction", 
                                    y=feature, 
                                    title=f"Pengaruh {feature} terhadap Kepuasan",
                                    color="satisfaction",
                                    color_discrete_map={"satisfied": "#A3C9FF", "dissatisfied": "#F4A6A6"})  
                        st.plotly_chart(fig11)

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
