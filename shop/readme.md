E-commerce site
=====================


Description
=====================


This repository contains one of my test projects, do not judge too harshly. The site I have written is an electronic goods trading platform. In the models I have designed two categories of products: Laptops and Smartphones.
In Views, some functions have been designed to mark the presence of an SD card for a specific smartphone model. The code is covered in tests. The templates are taken standard.


 Getting Started
 ===============
 
**Make virtualenv**

>On Linux::

   `$ python3.6 -m venv venv`
   `$ . venv/bin/activate`

>On Windows::

   `python -m venv venv`
   `venv/Scripts/activate`

****Install python****

   `install Python 3.6: pyenv install 3.6`

****Clone this repository****

   `git clone git@github.com:Oleksandr015/e-shop.git`
   

****Install requirements****

   `(venv)$ pip install -r requirements.txt`

****Migrate****

   `(venv)$ cd myproject`
   `(venv)$ python manage.py migrate`

****Make admin user****

   `(venv)$ python manage.py createsuperuser`

****Runserver****

   `(venv)$ cd myproject`
   `(venv)$ python manage.py runserver`

