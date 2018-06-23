#Hello Books

Hello Books is a simple API that implements CRUD functionalities. Two knids of users can use this API. A normal user (non-admin) can register to be a user, login, view all books available, borrow a book and logout. The admin, in addition to what the normal user can do is also able to create a new book, edit or delete an existing book. 

## Code Integration and Testing

[![Build Status](https://travis-ci.org/loisameyo/books-app.svg?branch=development)](https://travis-ci.org/loisameyo/books-app)
[![Coverage Status](https://coveralls.io/repos/github/loisameyo/books-app/badge.svg?branch=master)](https://coveralls.io/github/loisameyo/books-app?branch=master)
<a href="https://codeclimate.com/github/loisameyo/books-app/maintainability"><img src="https://api.codeclimate.com/v1/badges/9000718b9ae0e8661a9c/maintainability" /></a>

# Functionalities

The following are functionalities enabled with this API:

Functionality                       |Endpoint
------------------------------------|------------------------------
|POST  /api/books                   | add a book                  |
|PUT /api/books/<bookId>            | modify a book’s information |
|DELETE /api//books/<bookId>        | Remove a book               |
|GET  /api/books                    | Retrieves all books         |
|GET  /api/books/<bookId>           | Get a book                  |
|POST  /api/users/books/<bookId>    | Borrow a book               |
|POST /api/auth/register            | Creates a user account      |
|POST /api/auth/login               | Logs in a user              |
|POST /api/auth/logout              | Logs out a user             |
|POST /api/auth/reset-password      | Password reset              |

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
To run the tests for the app, run;

* nosetests -v


## Authors

* **Loice Meyo**

