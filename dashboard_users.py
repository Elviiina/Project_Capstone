import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, User, Admin
import time
import pandas as pd
import pickle

st.set_page_config(page_title="Aerosite for User", page_icon=":airplane:", layout="wide")

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
        
        if not session_token:
            show_error("Tidak ada sesi yang ditemukan. Akses tidak diizinkan.")
        else:
            user = User.query.filter_by(token=session_token).first()  
            if user:
                open_model = open("model/model_satisfaction.sav", "rb")
                model = pickle.load(open_model)
                if user.survey:
                    st.session_state.step = 1
                else:
                    st.session_state.step = 0

                with st.sidebar:
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col2:
                        st.image("static/images/logowarna.png", width=150)
                    st.markdown('<br>', unsafe_allow_html=True)    
                    selected = option_menu("Menu", ["Survei Penerbangan", "Hasil Survei", "Pengaturan"],
                                        icons=['airplane-engines', 'bar-chart', 'gear'],
                                        menu_icon="list", default_index=0)

                if selected == "Survei Penerbangan":
                    if st.session_state.step == 0:
                        with st.form("flight_form", border=False):
                            st.title("Isi Data Penerbangan")
                            with st.container(border=True):
                                st.write("Masukkan Data Penerbangan")
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    gender = st.selectbox("Gender", options=["Male", "Female"], help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                    flight_distance = st.number_input("Flight Distance", min_value=0, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                
                                with col2:
                                    age = st.number_input("Age", min_value=0, max_value=120, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                    departure_delay = st.number_input("Departure Delay in Minutes", min_value=0, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                
                                with col3:
                                    travel_type = st.selectbox("Type of Travel", options=["Business travel", "Personal Travel"], help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                    arrival_delay = st.number_input("Arrival Delay in Minutes", min_value=0, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                
                                with col4:
                                    flight_class = st.selectbox("Class", options=["Eco", "Eco Plus", "Business"], help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)

                            st.title("Isi Survei")
                            with st.container(border=True):
                                st.markdown("<p style='font-style: italic; font-size: 13px'>Note: 0 untuk sangat tidak puas; 5 untuk sangat puas</p>", unsafe_allow_html=True)
                                questions = {
                                    "Seat Comfort": "Seat Comfort",
                                    "Food and Drink": "Food and Drink",
                                    "Departure/Arrival Time Convenience": "Departure/Arrival Time Convenience",
                                    "Gate Location": "Gate Location",
                                    "Inflight Wifi Service": "Inflight Wifi Service",
                                    "Inflight Entertainment": "Inflight Entertainment",
                                    "Online Support": "Online Support",
                                    "Ease of Online Booking": "Ease of Online Booking",
                                    "On-board Service": "On-board Service",
                                    "Leg Room Service": "Leg Room Service",
                                    "Baggage Handling": "Baggage Handling",
                                    "Check-in Service": "Check-in Service",
                                    "Cleanliness": "Cleanliness",
                                    "Online Boarding": "Online Boarding"
                                }

                                survey_responses = {}

                                question_keys = list(questions.keys())
                                for i in range(0, len(question_keys), 3):
                                    cols = st.columns(3)

                                    for j, col in enumerate(cols):
                                        if i + j < len(question_keys):
                                            question = question_keys[i + j]
                                            with col:
                                                st.write(questions[question])
                                                survey_responses[question] = st.radio("Skala 1-5", options=[1, 2, 3, 4, 5], key=question, horizontal=True, help='*required')

                                    st.markdown("---")

                            submit_button = st.form_submit_button("Submit")

                            if submit_button:
                                with st.spinner("Mengirim survei..."):
                                    data_new_record = pd.DataFrame({
                                        'Gender': [1 if gender == "Male" else 0], 
                                        'Age': [age],
                                        'Type of Travel': [1 if travel_type == "Business travel" else 0],
                                        'Class': [2 if flight_class == "Business" else (1 if flight_class == "Eco Plus" else 0)],
                                        'Flight Distance': [flight_distance],
                                        'Seat comfort': [survey_responses["Seat Comfort"]],
                                        'Departure/Arrival time convenient': [survey_responses["Departure/Arrival Time Convenience"]],
                                        'Food and drink': [survey_responses["Food and Drink"]],
                                        'Gate location': [survey_responses["Gate Location"]],
                                        'Inflight wifi service': [survey_responses["Inflight Wifi Service"]],
                                        'Inflight entertainment': [survey_responses["Inflight Entertainment"]],
                                        'Online support': [survey_responses["Online Support"]],
                                        'Ease of Online booking': [survey_responses["Ease of Online Booking"]],
                                        'On-board service': [survey_responses["On-board Service"]],
                                        'Leg room service': [survey_responses["Leg Room Service"]],
                                        'Baggage handling': [survey_responses["Baggage Handling"]],
                                        'Checkin service': [survey_responses["Check-in Service"]],
                                        'Cleanliness': [survey_responses["Cleanliness"]],
                                        'Online boarding': [survey_responses["Online Boarding"]],
                                        'Departure Delay in Minutes': [departure_delay],
                                        'Arrival Delay in Minutes': [arrival_delay]
                                    })

                                    satisfaction_prediction = model.predict(data_new_record)
                                    prediction_text = "satisfied" if satisfaction_prediction[0] == 1 else "dissatisfied"
                                    
                                    data_new_record['satisfaction'] = prediction_text
                                    data_new_record['Customer Type'] = None
                                    data_new_record['Gender'] = data_new_record['Gender'].replace({1: 'Male', 0: 'Female'})
                                    data_new_record['Type of Travel'] = data_new_record['Type of Travel'].replace({1: 'Business travel', 0: 'Personal Travel'}) 
                                    data_new_record['Class'] = data_new_record['Class'].replace({2: "Business", 1: 'Eco Plus', 0: 'Eco'})

                                    st.success(f"Prediksi Kepuasan: {prediction_text}")
                                    
                                    df = pd.read_csv("./dataset/Invistico_Airline.csv")
                                    df_concated = pd.concat([df, data_new_record], ignore_index=True) 
                                    df_concated.to_csv("./dataset/Invistico_Airline.csv", index=False)

                                    user.survey = True
                                    admin = Admin.query.first()
                                    admin.survey_count += 1
                                    if satisfaction_prediction[0] == 1:
                                        admin.satisfied_count += 1
                                    else:
                                        admin.dissatisfied_count += 1
                                    db.session.commit()
                                    time.sleep(2)
                                st.rerun()

                    elif st.session_state.step == 1:
                        st.title("Thanks for your feedback!")
                        st.markdown("<h1 style='text-align: left; color: #4CAF50;'>🎉 Terima Kasih!</h1>", unsafe_allow_html=True)
                        st.markdown("<p style='text-align: left; font-size: 20px;'>Kami menghargai umpan balik Anda.</p>", unsafe_allow_html=True)
                        
                        st.balloons()

                        st.markdown("<p style='text-align: left; font-size: 24px; color: #FFA500;'>✨ Survey Anda telah terkirim dengan sukses!</p>", unsafe_allow_html=True)
                
                elif selected == "Hasil Survei":
                    st.title("Hasil Survei")

                elif selected == "Pengaturan":
                    st.title("Pengaturan")
                    if st.button("Log Out", key='logout_button', icon=':material/logout:'):
                        if "session_token" in st.session_state:
                            del st.session_state["session_token"]
                        user.token = None
                        db.session.commit()
                        st.write(st.markdown("<meta http-equiv='refresh' content='0; url=http://localhost:5000/logout'>", unsafe_allow_html=True))
                        
            else:   
                show_error("Token tidak valid. Akses tidak diizinkan.")
                
except Exception as e:
    show_error(f"Error! Hubungi Admin jika menurut anda ini adalah kesalahan. INFO: {e}")

