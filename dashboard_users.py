import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, User  

def show_error(message):
    st.error(message)

try:
    with app.app_context():
        params = st.query_params
        session_token = params.get('sessionToken', [None])
        
        if not session_token:
            show_error("Tidak ada sesi yang ditemukan. Akses tidak diizinkan.")
        else:
            user = User.query.filter_by(token=session_token).first()  
            if user:
                # Judul Aplikasi
                st.title("Isi Data Penerbangan dan Survei")

                # Formulir Data Penerbangan
                st.subheader("Isi Data Penerbangan")

                flight_number = st.text_input("Flight Number")
                airline_name = st.text_input("Airline Name")
                departure_city = st.text_input("Departure City")
                arrival_city = st.text_input("Arrival City")
                flight_duration = st.text_input("Flight Duration")
                class_type = st.selectbox("Class", ["Economy", "Business", "First Class"])

                # Formulir Survei
                st.subheader("Isi Survei")

                gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])
                age = st.number_input("Age", min_value=1, max_value=120)
                travel_type = st.selectbox("Type of Travel", ["Bisnis", "Liburan", "Keluarga"])

                st.write("Catatan: 1 - Sangat Tidak Puas, 2 - Tidak Puas, 3 - Cukup, 4 - Puas, 5 - Sangat Puas")

                # Skala Penilaian
                seat_comfort = st.radio("Seat Comfort", [1, 2, 3, 4, 5])
                food_and_drink = st.radio("Food and Drink", [1, 2, 3, 4, 5])
                departure_arrival_time = st.radio("Departure/Arrival time convenient", [1, 2, 3, 4, 5])
                gate_location = st.radio("Gate location", [1, 2, 3, 4, 5])
                inflight_wifi_service = st.radio("Inflight wifi service", [1, 2, 3, 4, 5])
                inflight_entertainment = st.radio("Inflight entertainment", [1, 2, 3, 4, 5])
                online_support = st.radio("Online support", [1, 2, 3, 4, 5])
                ease_online_booking = st.radio("Ease of Online booking", [1, 2, 3, 4, 5])
                onboard_service = st.radio("On-board service", [1, 2, 3, 4, 5])
                leg_room_service = st.radio("Leg room service", [1, 2, 3, 4, 5])
                baggage_handling = st.radio("Baggage handling", [1, 2, 3, 4, 5])
                checkin_service = st.radio("Checkin service", [1, 2, 3, 4, 5])
                cleanliness = st.radio("Cleanliness", [1, 2, 3, 4, 5])
                online_boarding = st.radio("Online boarding", [1, 2, 3, 4, 5])

                # Tombol untuk melakukan prediksi
                if st.button("Predict Now"):
                    st.success("Hasil Survei akan ditampilkan di sini.")
                    
                    # Menampilkan hasil survei
                    st.write("**Ringkasan Hasil Survei**")
                    st.write(f"Flight Number: {flight_number}")
                    st.write(f"Airline Name: {airline_name}")
                    st.write(f"Departure City: {departure_city}")
                    st.write(f"Arrival City: {arrival_city}")
                    st.write(f"Flight Duration: {flight_duration}")
                    st.write(f"Class: {class_type}")
                    st.write(f"Gender: {gender}")
                    st.write(f"Age: {age}")
                    st.write(f"Type of Travel: {travel_type}")
                    st.write(f"Seat Comfort: {seat_comfort}")
                    st.write(f"Food and Drink: {food_and_drink}")
                    st.write(f"Departure/Arrival time convenient: {departure_arrival_time}")
                    st.write(f"Gate location: {gate_location}")
                    st.write(f"Inflight wifi service: {inflight_wifi_service}")
                    st.write(f"Inflight entertainment: {inflight_entertainment}")
                    st.write(f"Online support: {online_support}")
                    st.write(f"Ease of Online booking: {ease_online_booking}")
                    st.write(f"On-board service: {onboard_service}")
                    st.write(f"Leg room service: {leg_room_service}")
                    st.write(f"Baggage handling: {baggage_handling}")
                    st.write(f"Checkin service: {checkin_service}")
                    st.write(f"Cleanliness: {cleanliness}")
                    st.write(f"Online boarding: {online_boarding}")
            else:   
                show_error("Token tidak valid. Akses tidak diizinkan.")
except Exception as e:
    show_error(f"Terjadi kesalahan pada url anda!")
