#!/bin/bash

pid=0

usage()
{
    echo 'usage: ./entrypoint.sh [-a api ] | [-t 1 ] | [-w 1]'
    echo 'options'
    echo '     -a api, worker      default api        type application'
    echo '     -t number           default 1          number of threads'
    echo '     -w number           default 1          number of workers'
}

api()
{
    workers="$1"
    threads="$2"

    flask db upgrade
    flask bootstrap

    gunicorn -b 0.0.0.0:80 -t 300 -w "$workers" --threads "$threads" --access-logfile - --error-logfile - "better_than_yesterday:create_api()" &
    pid="$!"
}

worker()
{
    workers="$1"
    for (( i=1; i<=$1; i++ ))
    do
        i2="$i"
        celery -A worker:worker worker -l info --concurrency="1" -n "worker$i2" & pid="$!"
    done
}

worker_integration()
{
    python "worker_integration.py" & pid="$!"
}

worker_integration_dl()
{
    python "worker_integration_dl.py"
    pid="$!"
}

worker_nuvem_fiscal()
{
    python "worker_nuvem_fiscal.py" & pid="$!"
}

worker_nuvem_fiscal_dl()
{
    python "worker_nuvem_fiscal_dl.py"
    pid="$!"
}

term_handler()
{
    if [ $pid -ne 0 ]; then
        kill -SIGTERM "$pid"
        wait "$pid"
    fi
    exit 0
}

trap 'kill ${!}; term_handler' SIGHUP SIGINT
trap 'kill ${!}; term_handler' SIGTERM

application_type='api'
number_threads=1
number_workers=1

while [ "$1" != "" ]; do
    case $1 in
        -a )            shift
                        application_type=$1
                        ;;
        -t )            shift
                        number_threads=$1
                        ;;
        -w )            shift
                        number_workers=$1
                        ;;
        -h | --help )   usage
                        exit
                        ;;
        * )             usage
                        exit 1
    esac
    shift
done

if [ "$application_type" != 'api' ] && [ "$application_type" != 'worker' ] && [ "$application_type" != 'worker_integration' ] && [ "$application_type" != 'worker_integration_dl' ] && [ "$application_type" != 'worker_nuvem_fiscal' ] && [ "$application_type" != 'worker_nuvem_fiscal_dl' ]; then
    echo 'for type -a the values allowed are:'
    echo '    api'
    echo '    worker'
    echo '    worker_integration'
    echo '    worker_integration_dl'
    echo '    worker_nuvem_fiscal'
    echo '    worker_nuvem_fiscal_dl'
    exit 1
fi

if [ "$number_threads" -lt 1 ]; then
    echo 'the number of threads need to be positive'
    exit 1
fi

if [ "$number_workers" -lt 1 ]; then
    echo 'the number of workers need to be positive'
    exit 1
fi

if [ "$application_type" == 'api' ]; then
    api $number_workers $number_threads
    pid="$!"
elif [ "$application_type" == 'worker' ]; then 
    worker $number_workers
    pid="$!"
elif [ "$application_type" == 'worker_integration' ]; then
    worker_integration
    pid="$!"
elif [ "$application_type" == 'worker_integration_dl' ]; then
    worker_integration_dl
    pid="$!"
elif [ "$application_type" == 'worker_nuvem_fiscal' ]; then
    worker_nuvem_fiscal
    pid="$!"
elif [ "$application_type" == 'worker_nuvem_fiscal_dl' ]; then
    worker_nuvem_fiscal_dl
    pid="$!"
fi

while true
do
    tail -f /dev/null & wait ${!}
done
