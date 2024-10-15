import subprocess
import threading

from app import app 

def run_flask():
    app.run(port=5000)  

def run_streamlit_admin():
    subprocess.run(["streamlit", "run", "dashboard_admin.py", "--server.port=8501", "--server.headless=true"])  

def run_streamlit_user():
    subprocess.run(["streamlit", "run", "dashboard_users.py", "--server.port=8502", "--server.headless=true"])  

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()  

    admin_thread = threading.Thread(target=run_streamlit_admin)
    user_thread = threading.Thread(target=run_streamlit_user)
    
    admin_thread.start()
    user_thread.start()

#test
