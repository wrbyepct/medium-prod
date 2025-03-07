#!/usr/bin/env bash

countdown() {
    declare desc="Simple countdown function."

    local seconds="$1"
    local t=$(($(date +%s) + seconds ))
    
    while [[ t -gt $(date +%s) ]]; do

        # echo no newline and interpret special backslash code
        # which moves the cursor back to the beginning, effectively overwriting the previous output
        echo -ne "$(date -u --date @$((t - $(date +%s))) +%H:%M:%S)\r"
        sleep 1
    done


}
