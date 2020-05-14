# Send a Poem

This is the repository for the application Send a Poem, an application for publish poems and follow others poets, to see our their poems and send to friends on Whatsapp or Email. 

To clone this repository, execute the follow command on terminal:
```bash
git clone https://github.com/mateus-oliveira/sendapoem.git
``` 
After clone, go to sendapoem directory:
```bash
cd sendapoem
```

## Database

After run the APi server, create the database sendapoem on your MySQL database. To create the database, execute the query in [sendapoem.sql](./db/sendapoem.sql) file.

Do you can use the [Workbench](https://www.mysql.com/products/workbench/) for see the MySQL with a GUI.

Change the credentials in the [config.py](./src/database/config.py) file to your MySQL database credentials. 

## Backend

Before run the API, install the dependencies for this Python project with the commands bellow.

```bash
pip install virtualenv
mkdir ~/venv
virtualenv ~/venv/sendapoem
source ~/venv/sendapoem/bin/activate
pip install -r requirements.txt
```

After this, you can server the API and access the urls. Execute:

```bash
python app.py
```
And the server is started
```python
# * Serving Flask app "src.server" (lazy loading)
# * Environment: production
#   WARNING: This is a development server. Do not use it in a production deployment.
#   Use a production WSGI server instead.
# * Debug mode: on
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
# * Restarting with stat
# * Debugger is active!
# * Debugger PIN: 181-032-871
```

The endpoints for access the API are at the [requests.json](./endpoints/requests.json) file. You can import this file with [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/download/).

