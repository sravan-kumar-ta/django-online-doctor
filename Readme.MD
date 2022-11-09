# Online Doctor
[![Generic badge](https://img.shields.io/badge/build-Success-<COLOR>.svg)](https://shields.io/)


>This is a light-weight online-doctor application built on a **Python Django**. In this application users can login as a doctor or patient. Users can access this application with their **social accounts** such as **google** and **github**. Patients can choose the date&time and book an appointment. Appointments are made only after payment via **PayPal**. Patients can **real time chat** with booked doctors. Doctors can create posts and every user can read and like them.
* API
> It also provided api endpoints. It have a well api documentaion with the help of **swagger** (drf-yasg). **JWT** is used for authentication. and also provided **Google-auth**. In this project we provided token refreshing in every minutes and these tokens will be blacklisted after refreshing. **Pagination** is implemented in some api endponits.
* Hosting
>Project deployed on **Heroku** and using **AWS S3** to store static assets and file uploads.
>### Live Project :point_right: [online-doctor-x.herokuapp.com](https://online-doctor-x.herokuapp.com/home/)
>### API documentation using Swagger :point_right: [Online doctor API](https://online-doctor-x.herokuapp.com/swagger/)

<br>

## Getting Started

* Clone this repo :
  ```
  git clone https://github.com/sravan-kumar-ta/django-online-doctor.git
  cd django-online-doctor
  ```
* Create a virtual environment to install dependencies in and activate it:

  ```
  python -m venv venv
  venv\scripts\activate.bat
  ``` 
* Then install the dependencies:
  ```
  pip install -r requirements.txt
  ```
* Create database
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
* then create a super-user and add some data to the `Specialities` table in our db.
* Run the project
  ```
  python manage.py runserver
  ```
* And navigate to `http://localhost:8000/` for interacting with this app :relaxed:

## Tech Stack: 
* *Python Django*
* *Channels*
* *WebSocket*
* *django-allauth*
* *django-rest-framework*
* *djangorestframework-simplejwt*
* *drf-yasg*

## Services used:
  * *PayPal Payment gateway*
  * *Social authentication*
----------
[![Generic badge](https://img.shields.io/badge/Python-3.10.8-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Django-4.0.6-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Rest-3.13.1-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Django-4.0.6-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/channels-3.0.5-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/PyJWT-2.4.0-blue.svg)](https://shields.io/)
