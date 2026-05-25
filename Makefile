.PHONY: install dev-install lint typecheck test robot security-scan docker-build \
        docker-up docker-down clean all frontend-install frontend-build \
        go-build rust-build julia-test

SHELL := /bin/bash

install:
	pip install -e .

dev-install:
	pip install -e ".[dev,quantum]"

all-install:
	pip install -e ".[all]"

lint:
	ruff check src/python/ tests/ scripts/
	ruff format --check src/python/ tests/ scripts/

lint-fix:
	ruff check --fix src/python/ tests/ scripts/
	ruff format src/python/ tests/ scripts/

typecheck:
	mypy src/python/

test:
	pytest tests/ -x --timeout=60

test-coverage:
	pytest tests/ --cov=src/python --cov-report=html --cov-report=term-missing

test-quantum:
	pytest tests/ -m quantum -v

robot:
	robot --outputdir robot_output tests/robot/

security-scan:
	bandit -r src/python/ -f json -o bandit_report.json || true
	safety check || true

docker-build:
	docker compose -f docker/docker-compose.yml build

docker-up:
	docker compose -f docker/docker-compose.yml up -d

docker-down:
	docker compose -f docker/docker-compose.yml down

frontend-install:
	cd src/frontend && npm install

frontend-build:
	cd src/frontend && npm run build

frontend-dev:
	cd src/frontend && npm run dev

go-build:
	cd src/go && go build ./...

go-test:
	cd src/go && go test ./...

rust-build:
	cd src/rust && cargo build

rust-test:
	cd src/rust && cargo test

julia-test:
	cd src/julia/SpaceCommsTwin && julia --project -e 'using Pkg; Pkg.test()'

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf __pycache__ */**/__pycache__/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf robot_output/ coverage_html/
	rm -rf bandit_report.json
	find . -name '*.pyc' -delete

all: lint typecheck test security-scan
