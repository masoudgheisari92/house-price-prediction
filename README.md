# <center>Housing Price Prediction</center>

[![Python Version](https://img.shields.io/badge/python-3.9-brightblue.svg)](https://python.org)
![Django version](https://img.shields.io/badge/Django-4.1-0?colorB=blue)

# About

This is a project to scrape the data of the houses (title, description, region, price, year of construction, area, number of rooms) from https://divar.ir and save them in database (sqlite) afte preprocessing.

By using machine learning (Decision Tree), a model is trained to predict house prices.

# APIs

- `/scrape` scrape the data of the houses of a selected city.
- `/predict` predict the price of a house based of its city, region, year of construction, area and the number of rooms.

# Clone and Initialize the Responsitories

1. Clone the repository:

   ```bash
   git clone https://github.com/masoud2685/house_price_prediction.git
   ```

2. Configure the environment variables

   - make a `.env` file in `house_price_prediction` directory
   - The new `.env` file should contain all the following environment variables:
     ```bash
     DJANGO_SECRET_KEY=""
     DJANGO_DEBUG=True
     DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
     ```

# Run Project

1. Create virtual environment and install required packages:

   ```bash
   # create virtual environment
   python -m venv venv
   # activate virtual environment
   venv/Scripts/activate
   # install required packages
   pip install -r project/requirements.txt
   ```

2. Run the migrations

   ```bash
   cd project
   python manage.py migrate
   ```

3. Create superuser (admin)

   ```bash
   python manage.py createsuperuser
   ```

4. Run server
   ```bash
   python manage.py runserver
   ```

# Contact

### Masoud Gheisari

- linkedin: [https://linkedin.com/in/masoud-gheisari](https://linkedin.com/in/masoud-gheisari)
- email: masoud.gh20@gmail.com
