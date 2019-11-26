# A Strada di u Core
Web platform for cardiology service's patients
*http://www.astradadiucore.fr/*

Goals
=====

**Accessibility**
This project seeks to help patients find useful and legit medical knowledge without the need to come and consult a doctor.
Patients come from all backgrounds, and as such, the site must be easily understood by everyone, regardless of their technical expertise
on medical on informatic subjects.
The cardiology service's staff will also be users of the site's administration, which must be just as intuitive and ergonomic.

**Improvement**
The project is currently at its first iteration, and shall be frequently updated during the months following its release.
An easy to use administration interface is mandatory to add new content to the existing apps.
It is also deemed important to continously improve already existing content. Several features allows users to give feedback.
The staff can then easily access this feedback to increase the variety and relevance of the provided services.

Features
========
Two apps are presents on the platform : the faq, and the recipes

**F.A.Q.**
The F.A.Q.'s goal is to help patients find answers to common questions.
A simple search field allows the patient to simply type their question, as they would do on any search engine.
Using a tag system, the platform finds relevant answers created by the medical team.
The patient can then consult the detailed answers of the frequently asked questions displayed by the search engine, and notify
the staff whether the suggested answers were relevant or not. DB entries keep track of user feedback thus collected.

**Recipes**
The Recipes app's goal is to generate full meals for the patient, where each course is a certified healthy recipe created by the staff.
The user simply states how many meals they want to generate, and what course should appear in each one them. 
The resulting meals and associated recipes can be downloaded for offline reference. Grocery list is automatically generated for added ergonomy.

Local configuration
===================
Should you wish to download this project and run it locally, make sure to follow these steps :

**Dependencies**
All packages and dependencies are handled through pipenv. You can download it through the command `pip install pipenv`.
Once pipenv is installed, move inside the root folder and simply run `pipenv install` to install all dependencies.

**Database**
This project uses postgresql. Create a database and add it to the main settings file (stradacore/stradacore/settings/__init__.py) before running the server.

**Local variables**
Before running the project, make sure to create a .env file in root folder and set the *SECRET_KEY* variable.
If you wish to use the mailing system, change the mailing variables at the end of the main settings file to match the parameters of your own box.

**That's it !**
Run the server using `pipenv run python manage.py runserver` from the root folder. The site should be accessible through your localhost.
