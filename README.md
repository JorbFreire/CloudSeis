# CloudSeis

CloudSeis is a cloud-based seismic data processing software based on the desktop app [BotoSeis](https://github.com/botoseis/BotoSeis)
<br />
CloudSeis is mainly a wrapper for [SeismicUnix](https://github.com/JohnWStockwellJr/SeisUnix)

## Getting Started

### Dependencies

 - [Python](https://www.python.org/) v3.10.8 or above
 - [Node.js](https://nodejs.org/en) v16 or above
 - [yarn](https://yarnpkg.com/) v1.22.19 or above

### Run the server

Once inside the `server` folder, install its dependencies and run the dev environment as shown below.
```bash
pip3 install -r requirements.txt
```
```bash
flask run
```


#### Database
To create an SQLite database for dev env run:
```bash
flask db migrate
``` 
It will return an error because there is no change to create a new migration, 
but it shall create a ``db.sqlite3`` file if not already existent.
<br />
<br />

*(not sure if the next step is required)*

To run the migrations, run on your terminal in the server folder:
```bash
flask db upgrade
```
To create a new migration:
```bash
flask db migrate -m 'Nigration Name'
```

### Run the Webapp

Once inside the `Webapp` folder, install its dependencies and run the dev environment as shown below.
```bash
yarn
```
```bash
yarn dev
```

## Architecture and database modeling

