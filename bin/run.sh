#!/usr/bin/env bash
export APP_ENV="dev"

function start () {
    source .venv/bin/activate
    gunicorn --workers=1  --worker-class="sync" --log-level=debug --timeout=1000 -b 127.0.0.1:5000 --reload app.main:application
}

function stop () {
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
    echo "Usage: run.sh {start|stop}"
    exit 1
esac
