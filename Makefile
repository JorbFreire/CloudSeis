# *** Makefile for building and managing Docker services

.PHONY: build-db build-server build-webapp up-default \
        build-test-db up-test-db upgrade-test-db \
        test

FLASK_APP := app.main
TEST_DATABASE_PORT := 5431

# *** Default targets, full demo or production
default: build-db build-server build-webapp up-default

build-db:
	docker-compose build db

build-server:
	docker-compose build server

build-webapp:
	docker-compose build webapp

up-default:
	@echo "Starting default services..."
	docker-compose up db server webapp -d

# *** get test database ready
test: build-test-db up-test-db upgrade-test-db

build-test-db:
	docker-compose build db-test

up-test-db: build-test-db
	docker-compose up db-test #-d

upgrade-test-db: up-test-db
	@echo "Applying database migrations..."
	cd server && FLASK_APP=$(FLASK_APP) DATABASE_PORT=$(TEST_DATABASE_PORT) flask db upgrade
	@echo "Database migrations applied successfully."
