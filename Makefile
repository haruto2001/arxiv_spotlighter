IMAGE_NAME = "arxiv-spotlighter"

build: ./Dockerfile ./entrypoint.sh
	docker build . \
	-t $(IMAGE_NAME) \
	--build-arg PYTHON_VERSION=$(shell cat .python-version)

run: ./pyproject.toml ./requirements.lock ./requirements-dev.lock ./.python-version ./README.md ./src
	docker run -it --rm \
	-e LOCAL_UID=$(shell id -u $(USER)) \
	-e LOCAL_GID=$(shell id -g $(USER)) \
	--env-file $(shell pwd)/.env \
	--mount type=bind,src=./pyproject.toml,dst=/workspace/pyproject.toml \
	--mount type=bind,src=./requirements.lock,dst=/workspace/requirements.lock \
	--mount type=bind,src=./requirements-dev.lock,dst=/workspace/requirements-dev.lock \
	--mount type=bind,src=./.python-version,dst=/workspace/.python-version \
	--mount type=bind,src=./README.md,dst=/workspace/README.md \
	--mount type=bind,src=./src,dst=/workspace/src \
	$(IMAGE_NAME) rye run python src/main.py