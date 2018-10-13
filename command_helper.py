import os
import json


class CommandHelper(object):
    def __init__(self):
        self.cmd_dict = self.refresh()

    def set(self, dik):
        self.cmd_dict = dik

    def get(self):
        return self.cmd_dict

    def renew(self):
        self.cmd_dict = self.refresh()

    @staticmethod
    def refresh():
        with open("joins.txt", 'a+') as joinsfile:
            joins = joinsfile.readlines()

        cmddict = {}

        for i in range(len(joins)):
            cmddict.update({joins[i].strip(): ""})
            filepath = joins[i].strip() + "commands"

            if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
                cmddict2 = {joins[i].strip(): json.load(open(filepath, "a+"))}
            else:
                defaultdik = {"!defaultcmd": "defaultaction"}
                json.dump(defaultdik, open(filepath, "a+"))
                cmddict2 = {joins[i].strip(): json.load(open(filepath, "a+"))}

            cmddict.update(cmddict2)

        return cmddict


cmds = CommandHelper()
