# Send e Poem

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
python src/routes.py
```

The endpoints for access the API are at the [requests.json](./endpoints/requests.json) file. You can import this file with [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/download/).

