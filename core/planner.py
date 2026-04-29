import json

class Planner:
    def __init__(self):
        self.tasks=[]

    def add(self,task):
        self.tasks.append({
            "task":task,
            "status":"pending"
        })

    def next(self):
        for t in self.tasks:
            if t["status"]=="pending":
                return t
        return None

    def done(self,task):
        task["status"]="done"

planner=Planner()
