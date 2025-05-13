# *** Makefile for building and managing Docker services

.PHONY: build-db build-server build-webapp build-webviz up-default \
				adm build-admin up-admin \
        build-test-db up-test-db upgrade-test-db \
        test

FLASK_APP := app.main
TEST_DATABASE_PORT := 5431

# *** Default targets, production like build (end user only, no admin module)
default: build-db server build-webapp build-webviz up-default

build-db:
	docker compose build db

build-server:
	docker compose build server

build-webapp:
	docker compose build webapp

build-webviz:
	docker compose build webviz

up-default:
	@echo "Starting default services..."
	docker compose up db webapp webviz -d

# *** Admin module and dependencies. 
adm: build-db build-server build-admin up-admin

build-admin:
	docker compose build admin

up-admin:
	@echo "Starting admin service and dependencies..."
	docker compose up db server admin -d

# *** Full demo in dedicated docker-stack
# *** To keep a local fully functional version of the application while developing
demo: build-demo up-demo

build-demo:
	docker compose build db
	docker build --tag boto/webapp:demo-1.0 ./webapp
	docker build --tag boto/webviz:demo-1.0 ./seismic-webviz
	docker build --tag boto/admin:demo-1.0 ./admin
# docker build --tag boto/server:demo-1.0 ./server

up-demo:
	docker compose -p boto-safe-demo up webapp webviz admin

# *** get test database ready
test: build-test-db up-test-db upgrade-test-db

build-test-db:
	docker compose build db-test

up-test-db: build-test-db
	docker compose up db-test

upgrade-test-db: up-test-db
	@echo "Applying database migrations..."
	cd server && FLASK_APP=$(FLASK_APP) DATABASE_PORT=$(TEST_DATABASE_PORT) flask db upgrade
	@echo "Database migrations applied successfully."
