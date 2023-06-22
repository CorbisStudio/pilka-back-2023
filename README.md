# 1. PRODUCTION ENVIRONMENT
- SERVER: Instancia EC2 en AWS 
- PUBLIC DNS: ec2-35-80-211-93.us-west-2.compute.amazonaws.com
- PATH: /srv/pilka/

## 1.1. Components
Implementado con contenedores Docker:
- Nginx
- Django Application

## 1.2. Environment Variables
Environment variables are stored at:
```/srv/pilka/config/env/env.prod```


## 1.3. To Start the App:
```bash
ssh -i "~/.ssh/corbis-pilka.pem" ubuntu@ec2-35-80-211-93.us-west-2.compute.amazonaws.com

cd /srv/pilka

sudo docker-compose up -d
```


## 1.4. Update the App

Connect to the server:
```bash
ssh -i "~/.ssh/corbis-pilka.pem" ubuntu@ec2-35-80-211-93.us-west-2.compute.amazonaws.com
```

Download updates from Bitbucket:
```bash
cd /srv/pilka

git pull origin
```

Execute database migrations:
```bash
sudo docker exec -it pilka_django_pilka_1 /bin/bash

python manage.py migrate
```

Restart the containers:
```bash
sudo docker-compose restart 
```


#
# 2. DEVELOPMENT

## Steps to use the app

- Clone the repo to your machine
```
git clone https://borbotonc@bitbucket.org/pyma/pilka.git
```
- Create a virtual environment
```
virtualenv -p=python3 <name_env>
```
- Activate the virtual environment
```
source /<name_env>/bin/activate
```
- Install requirements
```
pip install -r requirements.txt
```
- Make migrations for each app (users, facilities, matches, reservations)
```
./manage.py makemigrations <app name>
```
- Run migrations
```
./manage.py migrate
```
- Create admin user
```
./manage.py createsuperuser
```
- Run the server locally
```
./manage.py runserver
```

#### First time
```
python manage.py makemigrations users
python manage.py makemigrations facilities
python manage.py makemigrations reservations
python manage.py makemigrations matches
python manage.py makemigrations draw
python manage.py makemigrations health
python manage.py makemigrations tournaments
python manage.py migrate
```

### Restore bakcup
```
python manage.py loaddata api/users/fixtures/initial.json --app api.users
python manage.py loaddata api/facilities/fixtures/initial.json --app api.facilities
python manage.py loaddata api/users/fixtures/user_roles.json --app api.users
python manage.py loaddata api/reservations/fixtures/initial.json --app api.reservations
python manage.py loaddata api/matches/fixtures/initial.json --app api.matches
python manage.py loaddata api/draw/fixtures/initial.json --app api.draw
python manage.py loaddata api/health/fixtures/initial.json --app api.health
python manage.py loaddata api/tournaments/fixtures/initial.json --app api.tournaments
python manage.py loaddata api/users/fixtures/users-roles.json --app api.users
```

#### Backup Or Dump data
```
python manage.py dumpdata users --indent 4 > api/users/fixtures/initial.json
python manage.py dumpdata facilities --indent 4 > api/facilities/fixtures/initial.json
python manage.py dumpdata reservations --indent 4 > api/reservations/fixtures/initial.json
python manage.py dumpdata matches --indent 4 > api/matches/fixtures/initial.json
python manage.py dumpdata draw --indent 4 > api/draw/fixtures/initial.json
python manage.py dumpdata health --indent 4 > api/health/fixtures/initial.json
python manage.py dumpdata tournaments --indent 4 > api/tournaments/fixtures/initial.json
```
##### All Data
python manage.py dumpdata --all --indent 4 > api/initial.json
```


#### INSTALLATION EN ELASTIC BEANSTALK
1. Crear la app EBS
2. Instalar el cliente EB Cli en la máquina local
3. Hacer el EB Init para configurarlo (ver tema de seguridad)
4. eb config para setear wsgi.py path
5. Conexión a RDS externo (setear env variables en Configuration/Software)


## Acceso al shell con EB Cli
```
eb ssh <entorno>
source /opt/python/run/venv/bin/activate
source /opt/python/current/env
cd /opt/python/current/app
python manage.py shell
```

> \<entorno> = pilka-prod-2 | pilka-test


source /opt/python/run/venv/bin/activate && source /opt/python/current/env && cd /opt/python/current/app

## Despliegue
```
eb deploy <entorno>
```