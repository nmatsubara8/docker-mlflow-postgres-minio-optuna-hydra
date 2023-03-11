## ENVs
# basic
export PWD=`pwd`
# docker
export CONTAINER_NAME=mlf
# dockerfileのあるディレクトリ
export DIR_DOCKER=./

export DOCKERFILE_NAME=Dockerfile
export COMPOSEFILE_NAME=docker-compose.yaml
export CONTAINER_ID=`docker ps --format {{.ID}}`
# --------------------------------------------------------
init:
	docker-compose build --no-cache
build:
	docker-compose build
up:
	docker-compose up -d
down:
	docker-compose down
con:
	docker-compose exec app /bin/bash
# --------------------------------------------------------
# docker commands
export NONE_DOCKER_IMAGES=`docker images -f dangling=true -q`
export STOPPED_DOCKER_CONTAINERS=`docker ps -a -q`
export RUNNING_DOCKER_CONTAINERS=`docker ps -f status=running -q`
rm: ## rm running container
	docker-compose -f $(DIR_DOCKER)/$(COMPOSEFILE_NAME) down
	docker rm -f $(RUNNING_DOCKER_CONTAINERS)
clean: ## clean images/containers
	docker-compose -f $(DIR_DOCKER)/$(COMPOSEFILE_NAME) down
	-@make clean-images
	-@make clean-containers
clean-images:
	docker rmi $(NONE_DOCKER_IMAGES) -f
clean-containers:
	docker rm -f $(STOPPED_DOCKER_CONTAINERS)
# help
help: ## this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'