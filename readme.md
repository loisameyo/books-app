[![Build Status](https://travis-ci.org/loicemeyo/books-app.svg?branch=development)](https://travis-ci.org/loicemeyo/books-app)
[![Coverage Status](https://coveralls.io/repos/github/loisameyo/books-app/badge.svg?branch=development)](https://coveralls.io/github/loicemeyo/books-app?branch=development)
<a href="https://codeclimate.com/github/loicemeyo/books-app/maintainability"><img src="https://api.codeclimate.com/v1/badges/9000718b9ae0e8661a9c/maintainability" /></a>

# Hello Books

Hello Books is a simple API that implements CRUD functionalities. Two knids of users can use this API. A normal user (non-admin) can register to be a user, login, view all books available, borrow a book and logout. The admin, in addition to what the normal user can do is also able to create a new book, edit or delete an existing book. 

# Functionalities

The following are functionalities enabled with this API:

-[View here ](https://hellobooks12.docs.apiary.io/) a documentation on how to use this API.  

|Endpoints and methods               | Functionality              |Authorization criteria|
|------------------------------------|----------------------------|---------------------
|/api/v1/books (POST)                |Add a book                  | Admin only               
|/api/v1/books/*bookId*(PUT)         |Modify a book’s information | Admin only
|/api/v1/books/*bookId*(DELETE)      |Remove a book               | Admin only
|/api/v1/books(GET)                  |Retrieves all books         | Everybody
|/api/v1/books/*book_id*(GET)        |Get a book                  | Everybody
|/api/v1/users/books/*book_id*(POSt) |Borrow a book               | logged in User and Admin
|/api/v1/auth/register(POST)         |Register a user             | Everybody
|/api/v1/auth/register(PUT)          |Upgrade a user to admin     | Admin only
|/api/v1/auth/register(GET)          |Get registered users        | Admin only
|/api/v1/auth/login(POST)            |Login a user                | Registered user
|/api/v1/auth/logout(POST)           |Logout a user               | Loggged in user
|/api/v1/auth/reset-password(POST)   |Reset a user Password       | Registered user
|/api/v1/users/books/*book_id*(POST) |Borrow a books              |Logged in user
|/api/v1/users/books/*book_id*(PUT)  |Return a books              |Logged in user
|/api/v1/users/books(GET)            |Get user borrowing history  |Logged in user

**Prequisites**
```
Python - version 3.6.5
Postgress database
postman - To run various endponts
```


## Installation & Setup

1. Download & Install Python
 	* Download python from it's main site i.e (https://www.python.org/downloads/) and download it's latest version 3.6
    * Install it and it's required packages. This guide will help a lot to set that: (http://docs.python-guide.org/en/latest/starting/installation/)

2. Clone the repository in which the project resides into your local machine
 	* This is the clone link from the repository on github: (https://github.com/loisameyo/books-app.git)

3. Virtual Environment Installation
 	* Install the virtual environment by typing: `pip install virtualenv` on your terminal
4. Create a virtual environment by running `virtualenv venv`. This will create the virtual environment in which you can run the project.
5. Activate the virtual environment by running `venv/Scripts/activate`
6. Enter the project directory by running `cd Desktop\books-api\books-app`
7. Once inside the directory install the required modules
 * Run `pip install -r requirements.txt`


8. Inside the application folder run the run.py file:
 * On the terminal type `python run.py` to start the application

## Testing
Hello-Books API makes use of unittest to ascertain that the enpoints work as expected. To run the tests activate the virtual environment and then run: 

* nosetests -v

## Authors

* **Loice Meyo**

## First publication

* **2018**
