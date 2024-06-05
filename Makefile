IMAGE_NAME = "arxiv-spotlighter"

build: ./docker/Dockerfile ./docker/entrypoint.sh
	docker build --rm=true -t $(IMAGE_NAME) ./docker

run: ./src
	docker run -it -e LOCAL_UID=$(id -u $USER) -e LOCAL_GID=$(id -g $USER) --rm --mount type=bind,src=./src,dst=/workspace/src $(IMAGE_NAME) bash
