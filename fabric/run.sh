#!/usr/bin/env bash

DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $DIR
source venv/bin/activate

################### STATUS BAR ###################
uwsm app -a fabric_status_bar -- python status_bar.py

#################### LAUNCHER ####################
uwsm app -a fabric_launcher -- python launcher.py
