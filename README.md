# CloudSeis

CloudSeis is a cloud-based seismic data processing software based on the desktop app [BotoSeis](https://github.com/botoseis/BotoSeis)
<br />
CloudSeis is mainly a wrapper for [SeismicUnix](https://github.com/JohnWStockwellJr/SeisUnix)

## Getting Started

### Dependencies

 - Main dependencies:
    - [SeismicUnix]() (There is a step to install it bellow)
    - [Docker]() (Necessary for quiky run)
    - [Unix]() Based system (SeismicUnix installationg script only work on [Debia]() based systens)
 - Opcional dependancies, for manual run only (docker handle they)
    - [Python](https://www.python.org/) v3.10.8 or above
    - [Node.js](https://nodejs.org/en) v16 or above
    - [yarn](https://yarnpkg.com/) v1.22.19 or above

#### Installing seismic unix

run the command line bellow on visit the oficial guide to manual install
```bash
bash -c "$(wget -qO- https://gist.githubusercontent.com/botoseis/4ca681cb9ef706c1b8410153c6199cf2/raw/b16ad754839d1ca3657d8e8396db14f5ba791e6b/install_seismic_unix.sh)"
```

### Quicky start
run the `docker-compose.yml` file with `docker-compose` and let docker handle it all. 
```bash
docker-compose -f docker-compose.yml up
```
It shall start all project containers. To run each container individually, run:
```bash
```
to manully run any instance without docker, check each folder `README.md`.




# Manual run
### Run the server

Once inside the `server` folder, install its dependencies and run the dev environment as shown below.
```bash
pip3 install -r requirements.txt
```
```bash
flask run
```


#### Database
To run the migrations, run on your terminal in the server folder:
```bash
flask db upgrade
```
To create a new migration:
```bash
flask db migrate -m 'Migration Name'
```

### Run the Workspace

Once inside the `Workspace` folder, install its dependencies and run the dev environment as shown below.
```bash
yarn
```
```bash
yarn dev
```

## Architecture and database modeling

