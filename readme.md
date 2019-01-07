# Google Maps Data Monitoring

Monitor Places, and Establishement Information on background. Get notified via email when someone updated the place information.

### Installation

Requires [Redis-Server](https://redis.io) v4.0.9 to run.

Clone the repository and do master branch checkout

```sh
$ git clone https://romart27@bitbucket.org/romart27/mapsdatamonitoring.git
$ cd mapsdatamonitoring/
~/mapsdatamonitoring$ 
~/mapsdatamonitoring$ git checkout master
~/mapsdatamonitoring$ cd MapsDataMonitoring/
```

Install and Setup Python Environment

```sh
$ sudo apt-get install python3-venv
$ python3 -m venv venv
```

Activate python environment and install app requirements

```sh
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Build the database and create user

```sh
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py createsuperuser # Fill in the required fields.
```

Before running the server add GMail Credentials to settings.py and turn-on [Less Secure Feature](https://myaccount.google.com/u/1/lesssecureapps?pageId=none&pli=1) to allow backend email access.

```py
...
EMAIL_HOST_USER = 'your_email@mail.com' 
EMAIL_HOST_PASSWORD = 'your_email_password'
...
```

Run Server

```sh
$ ./runserver.sh
```

To access the server goto http://localhost:8000/admin
