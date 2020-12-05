# Welcome!
this is a certified bruh moment

## How to configure
1.  Clone project and login
```bash
git clone https://github.com/nakamarusun/OrgaDB.git
cd OrgaDB
```
2.  Create a virtual environment for Python 3 (Google if don't know :<zero-width space>( )
```bash
python -m venv venv
```

3. Activate the virtual environment, and install libs
```bash
venv/Scripts/activate
pip install -r requirements.txt
```

4. Make environment variable for flask app
Windows:
```bash
set FLASK_APP=EMS
set FLASK_ENV=development
```
Linux / Mac:
```bash
export FLASK_APP=EMS
export FLASK_ENV=development
```

5. Copy and rename EMS/db_config.py_template to db_config.py and configure it by yourself
6. Initialize the tables using the command
```bash
<UNFINISHED>
```
6. Run the flask project, and access using http://127.0.0.1:5000/
```bash
flask run
```
