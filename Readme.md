# Summary:
Old project. A Python Rest service written in Flask.

## Example Requests:
```````
curl -i -H "Content-Type: application/json" -X POST -d '{"first_name":"fancy_user", "last_name":"my_last_name", "userid":"fancyuser"}' http://127.0.0.1:5000/users/fancyuser


curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"moo_group", "users":["fancyuser"]}' http://127.0.0.1:5000/groups/moo_group

curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/users/fancyuser

```````

## Step 1 - Install dependencies:
```````
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
```````

## Step 2 - Run:
````
export APP_SETTINGS='config.DevelopmentConfig'
python app.py
````

### To run tests:
````
export APP_SETTINGS='config.TestConfig'
python test.py
````

#### To blow away everything and restart:
`````
deactivate
rm -rf dev.db test.db migrations venv

virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt

export APP_SETTINGS='config.DevelopmentConfig'
python db_create.py
python manage.py db init
python manage.py db migrate
python db_seed.py
`````
