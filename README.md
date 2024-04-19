# **PawfectMatch API**

The PawfectMatch API is a Django API for [PawfectMatch](https://github.com/Julia-Wagner/PawfectMatch), a platform to connect shelters with loving homes for their dogs. Shelters can register and post their dogs, share stories and photos. Future dog owners can register to look for dogs.

# **Table of Contents**

<!-- TOC -->
* [**PawfectMatch API**](#pawfectmatch-api)
* [**Table of Contents**](#table-of-contents)
* [**Planning**](#planning)
  * [**User Stories**](#user-stories)
    * [**Epic: User Authentication**](#epic-user-authentication)
    * [**Epic: General UX**](#epic-general-ux)
    * [**Epic: Profile**](#epic-profile)
    * [**Epic: User Interaction**](#epic-user-interaction)
    * [**Epic: Posts**](#epic-posts)
    * [**Epic: Dog Posts**](#epic-dog-posts)
    * [**Epic: Notifications and Communication**](#epic-notifications-and-communication)
* [**Deployment**](#deployment)
  * [**Create Repository**](#create-repository)
  * [**Project Setup**](#project-setup)
  * [**Database Setup**](#database-setup)
  * [**Cloudinary Setup**](#cloudinary-setup)
  * [**File Changes**](#file-changes)
  * [**JWT Setup**](#jwt-setup)
  * [**Heroku Setup**](#heroku-setup)
  * [**Final Changes**](#final-changes)
  * [**Forking**](#forking)
* [**Packages**](#packages)
<!-- TOC -->

# **Planning**

I detailed planning process using the 5 UX planes is described in the [PawfectMatch repository](https://github.com/Julia-Wagner/PawfectMatch?tab=readme-ov-file#planning).

## **User Stories**

I created separate user stories for the API from the user stories defined for the frontend part of the project using the same epics to group them.

I also decided to add these stories to the [project board](https://github.com/users/Julia-Wagner/projects/4) in the main repo instead of creating a separate backend board. This way the entire development process is visible in one board.

### **Epic: User Authentication**

| User Story                                                                                                                                                          | Priority       |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| As a **developer**, I want to **access an API endpoint for registration**, so that I can **create users and profiles**.                                             | **MUST HAVE**  |
| As a **developer**, I want to **access an API endpoint for login**, so that I can **authenticate users**.                                                           | **MUST HAVE**  |
| As a **developer**, I want to **access an API endpoint for the feed without providing a logged-in user**, so that I can **access the feed without authentication**. | **MUST HAVE**  |

### **Epic: General UX**

| User Story                                                                                                                                                            | Priority      |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| As a **developer**, I want to **get appropriate error messages from the API in response to failed requests**, so that I can **provide users with detailed feedback**. | **MUST HAVE** |

### **Epic: Profile**

| User Story                                                                                                                          | Priority       |
|-------------------------------------------------------------------------------------------------------------------------------------|----------------|
| As a **developer**, I want to **perform CRUD operations for profiles**, so that I can **allow users to edit their profiles**.       | **MUST HAVE**  |
| As a **developer**, I want to **edit and get the profile status**, so that I can **show or hide profiles**.                         | **COULD HAVE** |

### **Epic: User Interaction**

| User Story                                                                                                                         | Priority        |
|------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **access follow API endpoints**, so that I can **allow users to follow each other**.                 | **SHOULD HAVE** |
| As a **developer**, I want to **perform CRUD operations for comments**, so that I can **allow users to add comments to profiles**. | **COULD HAVE**  |
| As a **developer**, I want to **define banned words**, so that I can **ensure appropriate comments**.                              | **COULD HAVE**  |

### **Epic: Posts**

| User Story                                                                                                                                 | Priority        |
|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **perform CRUD operations for posts**, so that I can **allow users to post content**.                        | **MUST HAVE**   |
| As a **developer**, I want to **access an API endpoint for saving a post**, so that I can **provide the user with a list of saved posts**. | **SHOULD HAVE** |

### **Epic: Dog Posts**

| User Story                                                                                                                             | Priority        |
|----------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **have a special type of post for dogs**, so that I can **distinguish dog posts from other posts**.      | **MUST HAVE**   |
| As a **developer**, I want to **define requirements for dogs**, so that I can **use them for filtering**.                              | **COULD HAVE**  |
| As a **developer**, I want to **mark a dog as adopted**, so that I can **correctly show posts**.                                       | **SHOULD HAVE** |
| As a **developer**, I want to **receive dogs from the API based on defined criteria**, so that I can **allow filtering and matching**. | **SHOULD HAVE** |

### **Epic: Notifications and Communication**

| User Story                                                                                                                       | Priority        |
|----------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **receive notifications from the API**, so that I can **alert the user**.                          | **COULD HAVE**  |
| As a **developer**, I want to **perform CRUD operations for chat messages**, so that I can **allow users to exchange messages**. | **COULD HAVE**  |

# **Features/Apps**

The features of the PawfectMatch API can be broken down to apps. Here is a short summary of each app. All apps include automated testing, further described in the [Testing](#testing) section.

## **Comments App**

Instead of adding comments to posts, my project allows comments for profiles. Logged in users can create comments and edit and delete their own comments. 

Besides the **Comment** model, I added a **BannedWord** model. This allows superusers to add banned words in the admin panel. Banned words are enforced in comments to ensure appropriate usage. If a comment contains a bad word, it will not be posted and the user gets an error message.

**API Endpoints:**
- `/comments/`: to list (**GET**) or create (**POST**) comments.
- `/comments/:id/`: to show (**GET**), update (**PUT**) or delete (**DELETE**) a comment.

## **Dogs App**

Dogs can only be managed by users with the profile type *shelter*. To ensure this, I added the custom permission **IsShelterOrReadOnly**. Logged in shelters can create dogs and edit or delete their own dogs.

Besides the **Dog** model, I added a **DogCharacteristic** model. Characteristics can also be created, edited, and deleted by shelter users. Existing characteristics can be linked to dogs.

I created a custom **DogFilter** to allow filtering dogs by their characteristics and other fields.

**API Endpoints:**
- `/dogs/`: to list (**GET**) or create (**POST**) dogs.
- `/dogs/:id/`: to show (**GET**), update (**PUT**) or delete (**DELETE**) a dog.
- `/dogs/characteristics/`: to list (**GET**) or create (**POST**) dog characteristics.
- `/dogs/characteristics/:id/`: to show (**GET**), update (**PUT**) or delete (**DELETE**) a dog characteristic.

# **Testing**

# **Deployment**

Here is the [link to the deployed project](https://pawfect-api-dacc0c5bf00c.herokuapp.com/).

## **Create Repository**

The first step is to create a new repository, using the [Code Institute Template](https://github.com/Code-Institute-Org/ci-full-template). After creating the repository, you can open it in the IDE of your choice.

If you choose to work in a local IDE, it is important to create a **virtual environment** before continuing. I am using PyCharm, where the local environment can be conveniently set up by adding a new interpreter. Another way is by typing `python -m venv .venv` in the terminal.

## **Project Setup**

1. Install **Django**:
   - `pip install 'django<4'`
2. Create a Django project:
   - `django-admin startproject <name>`
3. Install supporting **libraries**:
   - `pip install django-cloudinary-storage`
   - `pip install Pillow`
4. Create **requirements.txt** file:
   - `pip freeze --local > requirements.txt`
   
## **Database Setup**

You can use a database of your choice, following are the instructions if you use [ElephantSQL](https://customer.elephantsql.com/).

1. Log in to your account
2. Click *Create New Instance*
3. Give the instance a name and select the plan of your choice, *Tiny Turtle* is the free plan.
4. Click *Select Region* and choose a data center near you
5. Click *Review* and if the details are correct click *Create instance*
6. Click on the created instance and copy the database URL

## **Cloudinary Setup**

1. Log in to your [Cloudinary](https://console.cloudinary.com/) account
2. At the dashboard, copy the link from the **API Environment variable**

## **File Changes**

1. In the **settings.py** file add this code:
    ```
    import os
    import dj_database_url
   
    if os.path.isfile("env.py"):  
        import env
    
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = "DEVELOPMENT" in os.environ
   
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
    ```
2. In the **env.py** file add this code and ensure the file is added to *.gitignore*:
    ```
    import os

    os.environ["SECRET_KEY"] = "addSecretKeyHere"
    os.environ["DEVELOPMENT"] = "TRUE"
    os.environ["DATABASE_URL"]= "copiedDatabaseURL"
    os.environ["CLOUDINARY_URL"] = "copiedCloudinaryURL"
    ```
3. After these changes, run `python manage.py migrate` to migrate your database structure to the ElephantSQL database.
4. In the **settings.py** file add this code to link to Cloudinary:
    ```
    INSTALLED_APPS = [...
      'cloudinary_storage',
      'django.contrib.staticfiles',
      'cloudinary',
    ...]
   
    # NOTE: the second line should already be in the file, add the line above and below, the order is important)
   
    STATIC_URL = 'static/'
    STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = '/media/'
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    ```

## **JWT Setup**

1. Install **dj-rest-auth**:
   - `pip install dj-rest-auth==2.1.9`
2. Add INSTALLED_APPS in **settings.py**:
   - `'rest_framework'`
   - `'rest_framework.authtoken'`
   - `'dj_rest_auth'`
   - `'django.contrib.sites'`
   - `'allauth'`
   - `'allauth.account'`
   - `'allauth.socialaccount'`
   - `'dj_rest_auth.registration'`
3. Add urls to main app **urls.py**:
   - `path('dj-rest-auth/', include('dj_rest_auth.urls'))`
   - `path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))`
4. Set SITE_ID in **settings.py**:
   - `SITE_ID = 1`
5. Install **simplejwt**:
   - `pip install djangorestframework-simplejwt`
6. Add JWT to **settings.py**:
    ```
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [(
            'rest_framework.authentication.SessionAuthentication'
            if 'DEV' in os.environ
            else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
        )],
        'DEFAULT_PAGINATION_CLASS':
            'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
        'DATETIME_FORMAT': '%d.%m.%Y',
    }
    if 'DEV' not in os.environ:
        REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
            'rest_framework.renderers.JSONRenderer',
        ]
    
    REST_USE_JWT = True
    JWT_AUTH_SECURE = True
    JWT_AUTH_COOKIE = 'my-app-auth'
    JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
    JWT_AUTH_SAMESITE = 'None'
    ```
7. Migrate database:
   - `python manage.py migrate`
   
## **Heroku Setup**

1. Log in to your [Heruko](https://www.heroku.com/) account
2. On the dashboard click *New* - *Create new app*
3. Give the app a unique name
4. Select the region closest to you and click *Create app*
5. Select your created app and open the *Settings* tab 
6. At the *Config Vars* section click *Reveal Config Vars* and add the following:
   - **DATABASE_URL** with the copied URL from ElephantSQL
   - **SECRET_KEY** with your secret key
   - **CLOUDINARY_URL** with the copied URL from Cloudinary
   - **DISABLE_COLLECTSTATIC** with the value 1
   - **ALLOWED_HOST** with the value of your deployed Heroku application URL

## **Final Changes**

1. Add `ALLOWED_HOSTS = ["PROJECT_NAME.herokuapp.com", "localhost"]` in **settings.py**
2. Create a **Procfile** file in the base directory
3. Add to **Procfile**:
    - `release: python manage.py makemigrations && python manage.py migrate`
    - `web: gunicorn <name>.wsgi`
4. In your **Heroku app**: 
   - Go to the *Deploy tab* and connect your GitHub repository
   - Click on *Deploy Branch* at the bottom of the page

## **Forking**

Forking creates a copy of the project on GitHub. Follow these steps to fork this repository:
1. Log in to your GitHub account and navigate to [the PawfectMatch-API repository](https://github.com/Julia-Wagner/PawfectMatch-API).
2. Click the **Fork** button on the top right of the repository.
3. You can now open the forked copy of this project as your own repository.
4. Follow the above steps to work on the project.

# **Packages**

- [cloudinary](https://pypi.org/project/cloudinary/) and [django-cloudinary-storage](https://pypi.org/project/django-cloudinary-storage/) -  integrate the application with Cloudinary.
- [gunicorn](https://pypi.org/project/gunicorn/) - Python WSGI HTTP Server for UNIX.
- [psycopg2](https://pypi.org/project/psycopg2/) - PostgreSQL database adapter.
- [Pillow](https://pypi.org/project/Pillow/) - Python Imaging Library.
- [django-allauth](https://docs.allauth.org/en/latest/) - authentication, registration, account management.
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/) - REST API endpoints.
- [django-cors-headers](https://pypi.org/project/django-cors-headers/) - adds Cross-Origin-Resource Sharing (CORS) headers to responses.
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - JSON web token authentication.
- [django-countries](https://github.com/SmileyChris/django-countries) - provides country choices.
- [python-magic](https://github.com/ahupp/python-magic#dependencies) - necessary to upload videos to cloudinary.
- [coverage](https://coverage.readthedocs.io/en/7.4.4/) - to measure testing coverage.
- [django-filters](https://django-filter.readthedocs.io/en/stable/) - to implement filter functionality.
