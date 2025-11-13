#!/bin/bash

RED='\033[0;31m' # red
NC='\033[0m' # no color
LB='\033[0;32m' # light blue

BASE_DIR_DEPLOYMENTS=./.deployments
PATH_DEVELOPMENT=$BASE_DIR_DEPLOYMENTS/development
PATH_STAGING=$BASE_DIR_DEPLOYMENTS/staging
PATH_PRODUCTION=$BASE_DIR_DEPLOYMENTS/production
PATH_TEST=$BASE_DIR_DEPLOYMENTS/test
declare -a COMMANDS=("dev", "stage", "prod", "test")
INPUT_PARAM=$1

if  [[ "$#" -eq 0 ]] ||
    [[ "$#" -gt 1 ]] ||
    [[ ! "${COMMANDS[@]}" =~ "${INPUT_PARAM}" ]]; then
    echo -e "${RED}Unknown parametr. Please use:${NC}
${LB}>>> start [COMMAND] ( dev | stage | prod | test )${NC}"
    exit 1
fi

cp $BASE_DIR_DEPLOYMENTS/entrypoint.sh .

case $INPUT_PARAM in
    dev)
        cp $PATH_DEVELOPMENT/env_example.txt ./.env
        cp -R $PATH_DEVELOPMENT/db_configs .
        cp $PATH_DEVELOPMENT/docker-compose.yml .
        echo "Success"
        exit 1
        ;;

    stage)
        cp $BASE_DIR_DEPLOYMENTS/run.sh .
        # cp -R $BASE_DIR_DEPLOYMENTS/nginx .
        cp $PATH_STAGING/env_example.txt ./.env
        cp $PATH_STAGING/docker-compose.yml .
        cp $PATH_STAGING/Dockerfile .
        echo "Success"
        exit 1
        ;;
    prod)
        cp $BASE_DIR_DEPLOYMENTS/run.sh .
        # cp -R $BASE_DIR_DEPLOYMENTS/nginx .
        cp $PATH_PRODUCTION/env_example.txt ./.env
        cp $PATH_PRODUCTION/docker-compose.yml .
        cp $PATH_PRODUCTION/Dockerfile .
        echo "Success"
        exit 1
        ;;
    test)
        cp $BASE_DIR_DEPLOYMENTS/run.sh .
        cp $PATH_TEST/env_example.txt ./.env
        cp $PATH_TEST/docker-compose.yml .
        cp $PATH_TEST/Dockerfile .
        echo "Success"
        exit 1
        ;;
esac

exec "$@"