
<div align="center">
  <img width="80%" src="https://github.com/ojg1993/SaversHaven/assets/61238157/143b6637-6b77-45e9-b330-d6d8bcf3bc33">
  <h1>Saven: Saver's Haven</h1>
  <h3>Eco-friendly choices, Budget friendly prices</h3>
</div>
<br>
Saver's Haven, a Django Rest Framework (DRF)-based backend API server project, serves as a second-hand trading platform. It facilitates connections between users to share pre-loved items, providing affordability for buyers and offering sellers a platform to declutter and earn. Additionally, Saven empowers users to contribute to environmental conservation by reducing waste and promoting the reuse of resources, while also facilitating seamless transactions, real-time communication through live chat, and comprehensive product management features.

## Project Overview
### Tech Stack

- **Backend:** Django(DRF), PostgreSQL, Nginx, Postman
- **Deployment:** Docker, Github Actions, AWS Elastic Beanstalk
- **Version Control:** Git, Github
- **Lint:** flake8, isort, black

### Backend System Architecture
![Saven_architecture](https://github.com/ojg1993/SaversHaven/assets/61238157/ea6f058a-5cd6-4f34-8e7f-2d17d65cd31a)

### Data Modeling

![Data modeling](https://github.com/ojg1993/SaversHaven/assets/61238157/d181927e-a046-40d2-a1ec-44d04713588b)

### Project Demo

<table>
  <tr>
    <td>
      <img src="https://github.com/ojg1993/SaversHaven/assets/61238157/972d67d4-2e96-4443-a0a3-ade5bee50d9d">
    </td>
    <td>
      <img src="https://github.com/ojg1993/SaversHaven/assets/61238157/2d9040f0-fcd3-41a3-a9cb-6ff539b7b5a0">  
    </td>
  </tr>
</table>



### Features

#### Authentication

- **Registration & Email Verification:**
	- Users can register using their email address, password, and other required information. Upon registration, a verification email is sent to the provided email address. Once the user verifies their email, they can log in to their account.
	- Implemented by customizing Django's AbstractBaseUser and utilising functionality from the dj-rest-auth library.
	- Includes functionality to resend the verification email if the original link expires.


- **Login:**
	- Users can log in to their accounts using their email and password, which generates JWT access and refresh tokens.
	- JWT authentication is implemented using the djangorestframework-simplejwt and dj-rest-auth libraries. The access token must be included in the request header with the bearer prefix for certain operations.

- **Social(Google) Registration / Login:**
	- Users have the option to authenticate using their Google account. If the account is not registered, it will automatically create an account and verify the email address.
	- Implemented using the django-allauth library for OAuth 2.0 and customizing the Google callback function process.
 
 - **Password Reset:**
	 - Users can reset their account password by requesting a password reset link sent to their email address.

- **Account management:**
	- Authenticated users can view and modify their account information.


#### Address Management
- **Country, County and City CRUD operations:**
  - Admin users can perform CRUD operations for countries, counties, and cities.
  
- **Address CRUD operations:** 
	- Authenticated users can manage their personal addresses by creating, reading, updating, and deleting them.

#### Category Management
- **Category CRUD operations:**
   - Admin users can perform CRUD operations for categories.
  - Implemented a tree category model using the django-mptt library.

#### Product Management
- **Product CRUD:**
  - Authenticated users can perform CRUD operations for products.
  - Unauthenticated users can only view products.
  - Products can be filtered by category and is_sold status.
  - Implemented a separate product image model with a foreign key relationship to support multiple image uploads.

#### Favorite Management
  - ****Save & Delete Favorite Products:****: Users can save products as favorites for future reference or transactions.

#### Live Chat
  - ****Initiate Chat with Seller****: 
	  - Authenticated users can message sellers to inquire about products or negotiate transactions.
  - **Asynchronous Process with Django Channels**: 
      - Utilized Daphne (ASGI server) for handling HTTP and WebSocket protocols.
      - Initially configured with an in-memory channel layer, which can be replaced with Redis for scalability.
 	  - Implemented chatrooms and message rendering using HTTP request-response and WebSocket connections.

#### Transaction Management
  - **Book a Transaction with the seller**: 
	  - Users can schedule transactions after communicating with sellers, providing location and time information.
	  - Users can modify transaction details and confirm completion.
#### Review Management
  - **Leave Reviews for Transaction Opponents:** 
	  - Users can leave reviews and ratings for transaction opponents, reflecting their satisfaction with the transaction. These reviews can be displayed on user profiles.

## API Documentation

[Click here](API.md) to open API documentation

## Local Deployment

### Pre-requisites
1. Install Python.
2. Install an IDE of your choice, such as PyCharm, Visual Studio Code, or Atom.
3. Install Docker desktop.

### Steps
1.  Clone the project repository:
```
git clone https://github.com/ojg1993/SaversHaven.git

```
2.  Navigate to the project directory:

```
cd SaversHaven

```

3.  Build and run the project using Docker Compose:

```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```
4. Check the application status
```
docker-compose -f docker-compose.prod.yml run --rm backend sh -c "python manage.py test"

```
5. Create a admin user

```
docker-compose -f docker-compose.prod.yml run --rm backend sh -c "python manage.py create superuser"

Email: example
Password: example
```

6.  Open your browser and visit  `http://localhost:80/` or `http://127.0.0.1:80/` to access the application.