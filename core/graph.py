#!/usr/bin/env python3
import json,os

MEM="/root/ish-dev/memory/graph.json"

def load():
    if not os.path.exists(MEM):
        return {}
    return json.load(open(MEM))

def save(data):
    json.dump(data,open(MEM,"w"))

def update(key,value):
    data=load()
    data[key]=value
    save(data)
