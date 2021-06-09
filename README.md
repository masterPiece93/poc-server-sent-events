# poc-server-sent-events
#### This is a basic POC demonstrating the usage and scope of server sent events

## Table of Contents
| Topic | Description |
| ----- | ----------- |
| pre-requisites| pre requisite system requirements |
| How to run project | steps to install and run the repo |

## pre-requisites
python3 ,
gunicorn

## How to run the project
###### installing requiremets.txt : 
`cd poc-server-sent-events/server/sse` 

`pip3 install -r requirements.txt`

###### run server command :
`python3 gunicorn wsgi -b 0:8000 -w 10 -k gevent`

###### run global processes :
open a new terminal in pop-server-sent-event folder
> `python3 global_process_1.py`
This process starts generating integer numbers and prints them on the terminal

open a new terminal in pop-server-sent-event folder
> `python3 global_process_2.py`
This process starts generating floating point numbers and prints them on the terminal
