# 🏐 Baile Beag GAA – Pitch Booking System

A full-featured Django web application for managing a fictional GAA club’s pitch bookings. The app allows coaches, managers, and club officials to manage team information, request and approve bookings, and receive notifications through a secure, role-based system. Deployed on **Render.com**.

## ✨ Features
- 📅  **Booking Management** – Request, approve, reject, and log bookings for pitches 
- 🏟️ **Astro & Main Pitch Logic** – Separate booking workflows for Astro and Main pitches
- 🧑‍🤝‍🧑 **Role-Based Access** – Permissions for Public, Coaches, Manager, Secretary, and Chairman
- 📬 **Notifications System** – On-site notifications for booking approvals/rejections
- 📑 **Team Management** – Create and list club teams with coaches assigned
- 📊 **Filterable Tables** – JavaScript-enhanced filters for bookings and teams pages
- 🎨 **Polished Frontend** – Bootstrap 5 with custom CSS for club-themed branding
- 🚀 **Live on Render** – Deployed online with environment configuration  

## 🧰 Technologies Used
- **Backend:** Django, Python
- **Frontend:** HTML, CSS (Bootstrap), JavaScript  
- **Deployment:** Render.com  
- **Database:** PostgreSQL
- **Auth:** Django’s built-in authentication with custom role-based permissions


## Setup & Installation
### 1. Clone the Repository
```bash
git clone https://github.com/james-fitz86/baile-beag-gaa.git
cd baile-beag-gaa

```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

#### Activate Virtual Environment
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Create a `.env` file
Create a `.env` file in the root of the project directory to store sensitive configuration values. The following variables are required:

- **SECRET_KEY**: Your Secret Key
- **EMAIL_HOST**: The SMTP host used for sending emails (e.g., `smtp.gmail.com`).
- **EMAIL_USER**: The email address used as the sender account for outgoing emails.
- **EMAIL_PASS**: The app-specific password or SMTP password for the email account.
- **DATABASE_URL**: Provide the connection string for your PostgreSQL database in the format:
`postgresql://your_username:your_password@localhost:5432/your_database_name`

Example `.env` file

```dotenv
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database_name
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```


### 5. Apply Migrations & Create Superuser

```python
python manage.py migrate
python manage.py createsuperuser
```


### 6. Run Locally
```bash
python manage.py runserver
```

Access the website locally at `http://127.0.0.1:8080/`

## Deployment to Render

1. Push your code to **GitHub**  
2. Sign up or log in at [Render.com](https://render.com/)  
3. Click **"New +"** and select **"Web Service"**  
4. Connect your **GitHub repository** and choose the appropriate branch  
5. Fill in the **Web Service** setup:
   - **Name:** e.g., `baile-beag-gaa`
   - **Runtime:** `Python 3`
   - **Build Command:**  
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput

     ```
   - **Start Command:**  
     ```bash
     gunicorn config.wsgi:application
     ```

6. Under the **Environment** tab, set the following environment variables (click **"Add Environment Variable"** for each one):
   - `SECRET_KEY` (generate one)
   - `EMAIL_HOST=smtp.gmail.com`  
   - `EMAIL_USER=your_email@gmail.com`
   - `EMAIL_PASS=your_app_password` 
   - `DATABASE_URL` (you'll set this after creating the database in step 7)

7. Create a PostgreSQL instance on Render and link it with `DATABASE_URL`.

8. Click **"Save Changes"** and then **"Deploy"** your web service  

9. Your app will build and deploy — visit the live link provided by Render when it's complete 🚀

> 🛑 **Important:** Never commit your `.env` file to GitHub — it should be listed in `.gitignore`.


## 🌐 Live Demo

Check out the live version of this project on Render:  
👉 [https://bailebeag-gaa.onrender.com/]