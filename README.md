## Django REST API Assessment - Book Management

### Objective:
Django REST API for managing books, users, and reading lists

### Installation:

Clone the repository.
Set up a virtual environment.
Install dependencies using pip (pip install -r requirements.txt).
Run migrations to create the database schema.
Start the development server. (python manage.py runserver)

### Usage:

Access the admin interface to manage vendor profiles and purchase orders.
Utilize RESTful APIs for integrating with other systems or building custom interfaces.



#### POST /api/users/register/
for user registration
Sample Data : 
{
    "first_name":"Arun",
    "last_name":"Krishna",
    "email":"arunkvb98@gmail.com",
    "password":"arun@1998"
}

### GET /api/users/login/
for loging in
Sample Data : 
{
    "username":"arunkvb98@gmail.com",
    "password":"arun@1998"
}


Set Authorization Header:
Open Postman and create a new request or open an existing one.
In the request headers section, add a new header with the key Authorization.
Set the value of the header to Token <your_authentication_token_here>, replacing <your_authentication_token_here> with the actual token you obtained While Loging in /api/users/login/.
Send Request:
Once you have set the Authorization header, you can send the request as usual.
Postman will include the token in the request headers, and your Django application will authenticate the request accordingly.



#### Add New Books
POST /api/books/add-book/
Sample Data: 
{
    "title":"Rich Dad Poor Dad",
    "authors":"Robert Kiyosaki, Sharon Lechter",
    "genre":"Personal finance",
    "publication_date":"2000-04-21"
}


#### Get all Books
GET api/books/retrieve-books/

### Create Reading List
POST /api/books/readinglist/
Sample Data:
{
    "name": "Reading List Name"
}

### Retrieve Reading List
GET /api/books/readinglist/

### Manage Reading List

To Add a book to Reading List
PATCH api/books/createreadinglist/<readinglist_id>/?book_id=2&order=2&action=add

To remove a book from Reading List
PATCH api/books/createreadinglist/<readinglist_id>/?book_id=2&order=2&action=remove