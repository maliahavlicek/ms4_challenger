# Challenger

Challenger  - an app to help bring the next level of competition to your group.

[![Build Status](https://travis-ci.org/maliahavlicek/ms4_challenger.svg?branch=master)](https://travis-ci.org/maliahavlicek/ms4_challenger)

## Author
Malia Havlicek


## Project Overview

Challenger provides a way for small groups to test each other with friendly competitions based on common skill sets and interests. Whether you are teaching music lessons, coaching a soccer team or just a group of friends trying to top each other, this forum allows you to quickly set up a group, designate a master of ceremonies and define the limits of the challenge. Members then can load up a video or image of their results. The master of ceremonies can privately grade submissions and peers can upvote each others' efforts. Members with a subscription service provide private links to families and fiends of their videos. 

### How to use


## Table of Contents

## UX

### Goals
#### Challenge Member Goals

The largest user group for the Challenger website will be those who are challenge members. 
These users are people who want to highlight their talents and skills. They can be students of a music school, members of a sports team, people learning a new language or those that want to share new found skills with like minded peers.

Challenge Member Goals are:
 - Easily see a list of active challenges I belong to
 - Submit a file as a challenge submission
 - Look at peers' challenge submissions
 - Rate a peer's submission
 - Receive an email when a challenge is opened
 - Receive a reminder email when a challenge is nearing closure
 - Review past challenges and their submissions
 - Send a link to friends and family that are not members so they can watch my submissions

#### Master of Ceremonies Goals

Masters of Ceremonies are user that own a challenge. 

Challenge Master Goals are:
- Initiate a challenge to a group of people via email
- Update an existing challenge
- Delete a challenge so I don't have to spend more money if I hit my challenge limit
- Upgrade my account so I can run more challenges
- Be notified when a submission has been made
- Approve Submissions before rest of team can see them
- Provide private constructive criticism to challenge members about their submissions

#### Business Goals
- Provide a professional forum that allows users to challenge each other and interact online in a respectful, positive manner
- Provide a safe environment where privacy is key such that younger audience can interact with peers online
- Connect like minded peers 
- Keep track of user self-tagging to inform future cross selling
- Keep track of user feature requests to make informed decisions on improvements

### User Stories
As a member of Challenger's website, I expect/want/need:
- To find a challenge easily, I want the email I receive to take me to the correct challenge immediately
- To easily see my peer's submissions for a challenge and any ratings
- To rate my peer's submissions
- To easily see all the challenges I belong to
- To know which challenges I am the master of and those that I am a member of
- To share a private link of my submission to my friends and family
- To easily set up my account
- To upgrade my account once I know I like the product and am willing to pay for a higher tier
- To be able to tell what my account settings are
- To see what Service Level tiers exist
- To pay for a Service Level securely
- To set up a challenge
- To delete a challenge
- To update an existing challenge

### Wireframes

### Design Choices

The intent is to provide a clean, intuitive design to users with subtle imagery and animation to spice up the pages in order to keep users engaged.

#### Color Choice
To provide a striking contrast between the header and footer vs the body of the page, onyx and white with bold highlighting colors were picked. 
[![Final Palette](documentation/challenger_color_palete.png "color palette App")](https://coolors.co/ffffff-007bff-12eccb-343a40-ec4646)

To provide a deeper contrast, the background color of the headers/footers versus the body are inverted. For headers and footers onyx is the background color while white is the background color for the body.

Turquoise is a green tone which represents forward action and is used for navigation links and buttons.

Salsa Red is used for warnings.
 
Azure blue was picked to represent textual links to aide older users by staying true to original html link coloration.

#### Typography

The target age group for this site is rather wide. Children from the ages of 10 to octogenarians and beyond could make use of the application. With that in mind, the base font size is 18px to make it easy to read. 

The purpose of the site is to allow peers to interact in friendly challenges from wherever they are geographically. Since the tasks depicted as challenges are aimed to highlight the talents and skills one possesses as well as encourage users to try new things, a futuristic font was chosen to roughly match the feel of star trek, and encourage participants to boldly go where they haven't gone before.

Several Google Fonts were explored and only those without any lower case l and upper case i differentiation issues were chosen.

##### Title Font

[Orbitron](https://fonts.google.com/?query=orbitron&selection.family=Orbitron) 

![Orbitron](documentation/Orbitron-Title-Font.png "Orbitron")

Titles, navigation links and buttons use the title font. Headings use a base font of 32px and size down.

##### Base Font

[Exo](https://fonts.google.com/?query=orbitron&selection.family=Exo) 

![Exo](documentation/Exo-Base-Font.png "Exo")

The base font size is 18px to accommodate for a wider age range of users. Exo is a bit easier to read than Orbitron but it has a futuristic feel to it to help carry out the space travel theme. 

#### Image Choice

This site is to be used by people aged 10 to 80 and beyond. Images were picked in an attempt to be colorful with high contrast and within the chosen color palette.

##### Service Levels
Large iconic imagery was selected with bold red colors to help users easily identify with product levels and the price commitment associated with such.

The Free product tier is represented by a balloon:

<img src="https://github.com/maliahavlicek/ms4_challenger/blob/master/documentation/products/hot-air-balloon.png?raw=true" width="150" height="auto" alt="Hot air balloon for free product" />

The Blast Off (Medium Tier) Product is represented by a 1960's rocket ship:

<img src="https://github.com/maliahavlicek/ms4_challenger/blob/master/documentation/products/startup.png?raw=true" width="150" height="auto" alt="Rocket Ship for medium product" />

The Interstellar (High End Tier) Product is represented by a futuristic space ship:

<img src="https://github.com/maliahavlicek/ms4_challenger/blob/master/documentation/products/clipart-rocket-red-rocket-17.png?raw=true" width="150" height="auto" alt="Futuristic Rocket Ship for high end product" />

#### Animations & Transitions

Due to the vast age diversity of users targeted for this website, animations are subtle and slower than average.
If viewed on desktop the rails are filled with a star field image that slowly transitions up and to the left to tie into the space travel/futuristic theme of the website.

## Features

### Implemented Features

#### Page Components 
The wire-frame process identified the need for the following User Interface Components:

#### Home Page

#### Products Page

#### Login Page

#### Register Page

#### Profile Page

#### Logout Page

#### Checkout Page

#### Challenges Page

#### Challenge Detail Page

#### Submission Page

#### Contact Page

#### Terms and Conditions Page

#### Forgot Password Page

#### Reset Password Page

### Features Left to Implement

## Information Architecture

### Database Choice

### Data Models

#### User
#### Profile
#### Tag
#### ServiceLevel
#### Challenge
#### Submission
#### Rating

## Technologies Used

### Programming Languages

### Framework & Extensions
- [bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)

### Fonts

### Tools
- [favicon generator](https://favicon.io/favicon-generator/) - free site to help in website icon generation

### APIs

## Defensive Programming

## Testing

### Validation Testing

### Unit Testing

### Cross Browser/Cross Device Verification

### Accessibility Testing

### Regression Testing

### Automated Testing

### Defect Tracking

#### Noteworthy Bugs

#### Outstanding Defects

## Deployment

### Requirements
If any of the following are unfamiliar, please click on their associated links as they are necessary when setting the environmental variables required to run this application:

 - an IDE such as [pycharm](https://www.jetbrains.com/pycharm/download) - a tool to help develop software
 - [PIP](https://pip.pypa.io/en/stable/installing/) - coordinates python installation packages
 - [python 3](https://www.python.org/downloads/) - Python is a programming language that lets you work more quickly and integrate your systems more effectively.
 - [git](https://gist.github.com/derhuerst/1b15ff4652a867391f03) -  version control system for code source
 - a [gmail accoount](https://accounts.google.com/signup) with less secure app access turned on use [this link](https://myaccount.google.com/lesssecureapps?pli=1) after you are signed into the gmail account - allows system to send email notifications such as password reset and user registration links
 - a [stripe account](https://stripe.com/) - used to securely collect payments, testing API's level is fine unless you want collect payments for real
 - [AWS-S3 (Amazon Web Services - Simple Storay Storage Account](https://docs.aws.amazon.com/AmazonS3/latest/gsg/SigningUpforS3.html) - web based cloud storage service for online backup of website assets
 - [S3 Bucket](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html) - a cloud storage resource which is similar to file folders on a computer's hard drive


### Local
1. Save a copy of the github repository located at https://github.com/maliahavlicek/ms4_challenger by clicking the 'download.zip' button at the top of the page and extracting the zip file to your chosen folder. If you have Git installed on your system, you can clone the repository with the following command:
   ```bash
   $ git clone https://github.com/maliahavlicek/ms4_challenger.git
   ```
1. Open your preferred IDE, then open a terminal session in the unzip folder or cd to the correct location.
1. Set up a virtual environment via this command in the terminal session:
   ```bash 
   python -m .venv venv
   ``` 
   > NOTE: The ```python``` prefix of this command and other steps below assumes you are working with a mac and pycharm's IDE. Your command may differ, such as ```python3 manage.py ...``` or ```py manage.py ...``` or ```.\manage.py ...```
1. Activate the .venv with the command:
   ```bash 
   .venv\Scripts\activate
   ```
   > Again this command may differ depending on your operating system, please check the Python Documentation on [virtual environments](https://docs.python.org/3/library/venv.html) for further instructions.
1. If needed, Upgrade pip locally with:
   ```bash
   pip install --upgrade pip
   ```
1. Install all required modules with the command:
   ```bash
   pip -r requirements.txt
   ```
1. Create a new file at the base ms4_challenge directory level called env.py:
   ```python
   touch env.py
   ```
1. Copy the following into the env.py file:
    ```python
    import os
    
    os.environ.setdefault('HOSTNAME', '<your value>')
    os.environ.setdefault('STRIPE_PUBLISHABLE', '<your value>')
    os.environ.setdefault('STRIPE_SECRET', '<your value>')
    os.environ.setdefault('SECRET_KEY', '<your value>')
    os.environ.setdefault('AWS_STORAGE_BUCKET_NAME', '<your value>')
    os.environ.setdefault('AWS_S3_REGION_NAME', '<your value>')
    os.environ.setdefault('AWS_ACCESS_KEY_ID', '<your value>')
    os.environ.setdefault('AWS_SECRET_ACCESS_KEY', '<your value>')
    os.environ.setdefault('EMAIL_USER', '<your value>')
    os.environ.setdefault('EMAIL_PASS', '<your value>')
    ```
1. Replace <your value> with the values from your own accounts
    - HOSTNAME - should be the local address for the site when running within your own IDE.
    - STRIPE_PUBLISHABLE - From Developer's API on (stripe dashboard)[https://dashboard.stripe.com/test/apikeys]
    - STRIPE_SECRET - From Developer's API on (stripe dashboard)[https://dashboard.stripe.com/test/apikeys]
    - SECRET_KEY -is a django key a long random string of bytes. For example, copy the output of this to your config: 
        ```bash
       python -c 'import os; print(os.urandom(16))'
        ```
    - AWS_STORAGE_BUCKET_NAME - can be found on your [bucket dashboard ](https://console.aws.amazon.com/s3/home)
    - AWS_S3_REGION_NAME - can be found your [bucket dashboard ](https://console.aws.amazon.com/s3/home), note, the interface has some textual description prefacing the region, the region is after the closing parenthesis descriptor. For Example ```US East(N. Virginia) us-east-1```, the region is ```us-east-1```
    - 
1. Set up the databases by running the following management command in your terminal:
    ```bash
    python manage.py migrate
    ```
   > If you restarted your machine to activate your environment variables, do not forget to reactivate your virtual environment with the command used at step 4.
1. Create the superuser so you can have access to the django admin, follow the steps necessary to set up the username, email and password by running the following management command in your terminal:
    ```bash
    python manage.py createsuperuser
    ```
1. Preload products and tags. To match starter projects and user profile tags to the original concept, run the following commands from your IDE's terminal:
    ```bash
    python manage.py loaddata servicelevel.json
    python manage.py loaddata tag.json
    ```

1. Start your server by running the following management command in your terminal:
    ```bash
    python manage.py runserver
    ```
1. If you make changes to CSS or Javascript files, be sure to run the management command to collect the static files so they are pulled into the AWS storage:
    ```bash
    python manage.py collectstatic
    ```

### Heroku

To run this application in a cloud environment to allow visibility to external users, you can deploy the code to Heroku. If you wish to do the same, follow the steps below. Please note this section assumes you have succeeded at running the application in your local environment first.


1. Login to Heroku and set up a new app with a unique name (something like ```<yourname>-challenger```)
1. On the Resources tab, in the Add-ons field type ``` Heroku Postgres``` select the default Hobby Dev - Free tier, then click the Provision button:
![Heroku Postgres](documentation/heroku-postgres.png "Heroku Postgres")
 This will provision a Postgres Database for you and automatically add a ```DATABASE_URL``` Config var.
1. Go to the Settings tab, click Reveal Config Vars and copy the DATABASE_URL value into your local memory.
1. In your IDE, open the env.py file add the following line to the file and paste in your DATABASE_URL value:
    ```python
    os.environ.setdefault('DATABASE_URL','<your DATABASE_URL value>')
    ```
1. In heroku for your newly created app, go back to the Settings tab, and click Reveal Config Vars. This time you will be copying the values from your env.py file into heroku. Make sure you load following:
    
    |           Key           |      Value     |
    |:-----------------------:|:--------------:|
    | HOSTNAME                | < your value > |
    | STRIPE_PUBLISHABLE      | < your value > |
    | STRIPE_SECRET           | < your value > |
    | SECRET_KEY              | < your value > |
    | AWS_STORAGE_BUCKET_NAME | < your value > |
    | AWS_S3_REGION_NAME      | < your value > |
    | AWS_ACCESS_KEY_ID       | < your value > |
    | AWS_SECRET_ACCESS_KEY   | < your value > |
    | EMAIL_USER              | < your value > |
    | EMAIL_PASS              | < your value > |
    | DATABASE_URL            | < your value > |
    | DISABLE_COLLECTSTATIC   | 1              |

1. Because this is a new database, you will to set up the databases by running the following management command in your terminal:
    ```bash
    python manage.py migrate
    ```
   > If you restarted your machine to activate your environment variables, do not forget to reactivate your virtual environment with the command used at step 4.
1. Create the superuser for the postgres database so you can have access to the django admin, follow the steps necessary to set up the username, email and password by running the following management command in your terminal:
    ```bash
    python manage.py createsuperuser
    ```
1. Preload products and tags. To match starter projects and user profile tags to the original concept, run the following commands from your IDE's terminal:
    ```bash
    python manage.py loaddata servicelevel.json
    python manage.py loaddata tag.json
    ```

1. In the event packages have been updated, it's best to re-create the requirements.txt file using the terminal command prompt: 
    ```bash
    pip freeze > requirements.txt
    ```
1. Create a Procfile:
    ```bash
    echo web: gunicorn ms4_challenger.wsgi:application > Procfile
    ```
1. Add the files if they changed and push to git hub:
    ```bash
   git commit add Procfile
   git commit add requirements.txt
   git commit-m 'getting ready to deploy to heroku'
   git push -u origin
   ``` 
1. From the heroku dashboard of your newly created application, click on the "Deploy" tab, then scroll down to the "Deployment method" section and select GitHub.
1. Use the github linking and type in the name of the repository ex:) ms4_challenger and click the search button. Then connect the heroku app to the desired GitHub repository.
1. On the Deployment Tab, scroll a bit further down to the "Manual Deploy" section, select the master branch then click "Deploy Branch".
1. If you have errors, look at the logs for your application, most common errors are forgetting to add the hostname and  disabling collectstatic.
1. Once your application is running, you may want to update the Deployment method from Manual to Automatic.


## Credits

### Content

### Media
- [flavicon](https://www.google.com/url?sa=i&url=https%3A%2F%2Fclipartix.com%2Frocket-clipart-image-11754%2F&psig=AOvVaw3osFDBKQwlWi5l_ED0kzix&ust=1588579579787000&source=images&cd=vfe&ved=0CA0QjhxqFwoTCKifqZ6el-kCFQAAAAAdAAAAABAD) rocket falvicon image before recoloring and rotation 
- [interstellar product image](https://www.stickpng.com/img/cartoons/little-einsteins/little-einsteins-rocket-ship
) - futuristic space craft
- [blast off product image](https://www.flaticon.com/free-icon/startup_639373?term=rocket&page=1&position=23) - 1970's rocket ship
- [free product image'](https://www.flaticon.com/free-icon/hot-air-balloon_2233035?term=hot%20air%20balloon&page=1&position=27) - hot air balloon

### Acknowledgements
- [ragoli](https://codemyui.com/parallax-pixel-stars-using-pure-css/) star background
- [coderwall](https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata) for examples on how to dump data and load it which saves a bunch of time when deploying the application from a local database to a hosted database



