# Challenger TESTING
## Author
Malia Havlicek
>## Table of Contents
>- [Back to README](https://github.com/maliahavlicek/ms4_challenger#wireframes)
# Testing

Validation, manual unit, cross browser/cross device, accessibility, travis, coverage, this app has a dash of everything test related.

## Validation Testing
- [CSS Validator](https://jigsaw.w3.org/css-validator/) Note, any error associated with root: color variables were ignored. 
- [HTML Validator](https://validator.w3.org/)  - validation of HTML with Django is pretty useless as all {{}} bracketed values raise errors. I ran only a few files through the validator and instead relied heavily upon pycharm's IDE to identify mismatched tags and closing Django directives.
- [django-extensions](https://pypi.org/project/django-extensions/) - used for validating templates from the command line ```python manage.py validate_templates```
- [JavaScript Validator](http://beautifytools.com/javascript-validator.php) Note any errors for let, variables set in other .js files, and constants were ignored. I also used a more [ES6 friendly checker](https://www.piliapp.com/syntax-check/es6/) and there were no errors for main.js
- [Pycharm IDE](https://www.jetbrains.com/pycharm/download) - PyCharm has inline validation for many file types. Python, CSS, HTML, DJANGO files were continuously tested for validity when using this IDE.

## Unit Testing

## Cross Browser/Cross Device Verification

## Accessibility Testing

## Regression Testing

## Automated Testing
If you want to run these tests, make sure you have cloned this project form [github](https://github.com/maliahavlicek/ms4_challenger) by following the steps in the [local deployment section](https://github.com/maliahavlicek/ms4_challenger#deployment) of the README.md file.

### Django Tests
Tests were written for Django views, forms, models. These files are located in each application specific folder and named:

- test_forms.py
- test_models.py
- test_views.py

[django-nose](https://pypi.org/project/django-nose/) was used to help configure and run tests with coverage output. The configurations are stored in the [.coveragerc] (https://github.com/maliahavlicek/ms4_challenger/blob/master/.coveragerc) file.

To run these tests go to the command terminal and:
1. ```python manage.py test```
2. type ```yes``` if prompted to clear the testdatabase
3. Generate a report ```coverage report```
4. Generate the HTML ```coverage html```
5. Open the newly created test_coverage directory in the root of your project folder.
6. Open the index.html file inside it.
7. Run the file in the browser to see the output.

### Travis
Travis was used throughout the unit testing of this project to provide continuous integration with the deployed site. Travis basically runs the command python manage.py test against a python 3.7 environment and the requirements.txt file. It's configured via the [.travis.yml](https://github.com/maliahavlicek/ms4_challenger/blob/master/.travis.yml) file.

Heroku settings for this project were configured to only allow deployment when the travis build tests had passed the latest push to the master branch on GitHub. 

### Defect Tracking

#### Noteworthy Bugs

#### Outstanding Defects

- [Back to README](https://github.com/maliahavlicek/ms4_challenger#wireframes)