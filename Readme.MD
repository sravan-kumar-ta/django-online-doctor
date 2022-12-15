# Online Doctor
[![Generic badge](https://img.shields.io/badge/build-Success-<COLOR>.svg)](https://shields.io/)


>This is a light-weight online-doctor application built on a **Python Django**. In this application users can login as a doctor or patient. Users can access this application with their **social accounts** such as **google** and **github**. Patients can choose the date&time and book an appointment. Appointments are made only after payment via **PayPal**. Patients can **real time chat** with booked doctors. Doctors can create posts and every user can read and like them.
* API
> It also provided api endpoints. It have a well api documentaion with the help of **swagger** (drf-yasg). **JWT** is used for authentication. and also provided **Google-auth**. In this project we provided token refreshing in every minutes and these tokens will be blacklisted after refreshing. **Pagination** is implemented in some api endponits.

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

## Screen Shots
* Home
<img src="https://user-images.githubusercontent.com/95027726/207891635-c62a4eb0-1df5-4348-9ebf-97c2f05b11b4.png" alt="home" width="80%"/>

* Auth
<div>
<img src="https://user-images.githubusercontent.com/95027726/207893251-9c35c5bc-4f72-4fcd-bf63-b6f8c8acfc22.png" alt="login" width="30%"/>
<img src="https://user-images.githubusercontent.com/95027726/207893289-5d8ac4ef-a4a4-4ce2-be6d-b587e11edbb6.png" alt="register" width="30%"/>
<img src="https://user-images.githubusercontent.com/95027726/207893306-fb0296a7-dff4-4002-919c-cc739851ca9d.png" alt="password" width="30%"/>
</div>

* Profile
<img src="https://user-images.githubusercontent.com/95027726/207894625-4a65c2b4-9510-4aa1-8792-e772b10e3529.png" alt="profile" width="80%"/>

* Appointment and chating
<div>
<img src="https://user-images.githubusercontent.com/95027726/207894883-74e0b8e9-51f5-4a7e-9337-6018a44a6df1.png" alt="appointment" width="45%"/>
<img src="https://user-images.githubusercontent.com/95027726/207894980-6d1811c3-74b4-40a4-9345-a7f6f4bfa923.png" alt="chating" width="45%"/>
</div>

* Blogs
<img src="https://user-images.githubusercontent.com/95027726/207895377-0483db0f-b65d-44e8-aadd-24f95b2c1e70.png" alt="blogs" width="80%"/>

* Swagger API documentation
<img src="https://user-images.githubusercontent.com/95027726/207895623-e2bebc9c-6fe8-45dc-9649-901400b403bb.png" alt="blogs" width="50%"/>

----------
[![Generic badge](https://img.shields.io/badge/Python-3.10.8-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Django-4.0.6-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Rest-3.13.1-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Django-4.0.6-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/channels-3.0.5-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/PyJWT-2.4.0-blue.svg)](https://shields.io/)
