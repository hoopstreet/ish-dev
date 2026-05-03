#!/bin/sh
spinner() {
    local pid=$1
    local msg=$2
    local spin='🧠⚙️🔧💻🔄✅🌟🏀'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % ${#spin} ))
        printf "\r${spin:$i:1} $msg... "
        sleep 0.15
    done
    printf "\r✅ $msg done    \n"
}

run_with_spinner() {
    local msg="$1"
    shift
    "$@" &
    spinner $! "$msg"
}
