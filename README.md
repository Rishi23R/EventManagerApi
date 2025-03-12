# EventManagerApi
#  Event Management API (FastAPI)

## Overview
This is a **FastAPI-based Event Management API** that allows users to:
- Create and manage **events** 
- Register **attendees** 
- Check-in attendees 🎟
- Filter events and attendees 

The API is designed using **FastAPI + SQLite** and deployed on **Railway.app**.

---

##  Installation (Local Setup)
### **1Clone the Repository**
```sh
git clone https://github.com/yourusername/EventManagerAPI.git
cd EventManagerAPI
```

### **2 Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate     # Windows
```

### **3 Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4 Initialize the Database**
```sh
python init_db.py
```

### **5 Run the Server**
```sh
uvicorn main:app --reload
```

### **6 Access API Docs**
Open in your browser:
```
http://127.0.0.1:8000/docs
```

---

## **Deploying on Railway**
### **1 Push Code to GitHub**
Ensure your latest code is pushed to GitHub:
```sh
git add .
git commit -m "Initial commit"
git push origin main
```

### **2 Deploy to Railway**
1. Go to [Railway.app](https://railway.app/)
2. Sign up using **GitHub**
3. Click **"New Project"** → **"Deploy from GitHub Repo"**
4. Select your **EventManagerAPI** repo
5. Set **Start Command**:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
6. Click **Deploy** 

### **3 Get Your API URL**
Once deployed, Railway provides a public URL like:
```
https://eventmanagerapi.up.railway.app
```
Use this for API access.

---

## **API Endpoints**

### **1 Event Management**
- **Create Event** (POST): `/events/`
- **Get Events** (GET): `/events/`
- **Filter Events** (GET): `/events?status=ongoing`
- **Update Event** (PUT): `/events/{event_id}`

### **2 Attendee Management**
- **Register Attendee** (POST): `/events/{event_id}/register`
- **Get Attendees** (GET): `/events/{event_id}/attendees`
- **Bulk Check-in (CSV)** (POST): `/events/{event_id}/bulk_checkin`

 **Full API documentation** available at:
```
https://eventmanagerapi.up.railway.app/docs
```

---

## **Testing**
### **1 Run Tests (Pytest)**
```sh
pytest
```
### **2 Postman Testing**
- Import API docs from `/docs`

---

## **Future Improvements**
-  Add PostgreSQL for production
-  Implement user roles (Admin/User)
-  Improve UI for event management

---

##  Contributing
1. Fork the repo 
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m 'Added new feature'`)
4. Push to GitHub (`git push origin feature-branch`)
5. Open a Pull Request 

---

##  Contact
For any issues, feel free to open an **Issue** or reach out via email at: **rishitharudrakshi@gmail.com** 

