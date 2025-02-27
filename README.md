🏨 Hotel & Food Booking Web App

This is a Django-based web application that allows users to book hotel rooms and order food online. The platform features a user-friendly interface, authentication system, and an admin panel for managing bookings and orders.

🚀 Features
User Features
✅ Register/Login with Email & Password  
✅ Social Authentication (Google, Facebook, LinkedIn)  
✅ Book hotel rooms online  
✅ Order food from nearby hotels  
✅ View booking history  

Admin Features
✅ Manage room availability  
✅ Manage food menu & orders  
✅ View customer bookings & orders  
✅ Dashboard with statistics  

---

 🏗️ Tech Stack
- Backend: Django, Django REST Framework  
- Frontend: HTML, CSS, JavaScript  
- Database: SQLite (Can be switched to PostgreSQL/MySQL)  
- Authentication: Django AllAuth (Google, Facebook, LinkedIn)  
- Deployment: Gunicorn, Nginx  

📂 Folder Structure
hotel_booking/
│── users/                   # User authentication system
│── bookings/                # Hotel room booking logic
│── food_orders/             # Food ordering system
│── templates/               # HTML templates
│── static/                  # CSS, JavaScript, Images
│── media/                   # Uploaded files
│── manage.py                # Django management file
│── requirements.txt         # Dependencies
│── README.md                # Project documentation
```


 🔧 Installation & SetupStep 1: Clone the Repository
sh
git clone https://github.com/your-username/hotel-booking.git
cd hotel-booking

Step 2: Create & Activate Virtual Environment
sh
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

Step 3: Install Dependencies
sh
pip install -r requirements.txt

Step 4: Apply Migrations
sh
python manage.py migrate

Step 5: Create a Superuser
sh
python manage.py createsuperuser
Follow the prompts to create an admin account.

Step 6: Run the Server
sh
python manage.py runserver
Your app will be live at: **http://127.0.0.1:8000**

🔐 Authentication Setup (Google, Facebook, LinkedIn)
Google OAuth Setup
1. Go to [Google Developers Console](https://console.cloud.google.com/)
2. Create a new project & enableGoogle+ API
3. Configure OAuth consent screen & generate Client ID & Secret
4. Add these credentials to your `.env` file:
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret

Hotel Booking Page!
[Booking Page](https://via.placeholder.com/800x400?text=Booking+Page)

Food Ordering Page
![Food Page](https://via.placeholder.com/800x400?text=Food+Ordering)

