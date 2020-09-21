#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import time

VERSION = "0.9.9alpha1"
COPYRIGHT_YEAR=2020
AUTHOR="Victor Huang <i@qwq.ren>"
IPMI_POWERSTATE_EXEC = ["/usr/bin/env", "ipmitool", "sdr", "type", "Power Supply"]
# IPMI_POWERSTATE_EXEC = ["/usr/bin/env", "python3", "tools/simulate.py", "--lost", ""] # test usage
SHUTDOWN_BIN = "/sbin/shutdown"
NORMAL_STATE = "Presence detected"
SHUTDOWN_TIMEOUT = 5 # minutes

def getLogTime():
    return "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "] "

def logger(info: str):
    for x in info.split('\n'):
        print(getLogTime() + x)

def getPowerState():
    returnVal = {
        "error": False,
        "error_message": None,
        "power_supplies": []
    }
    try:
        res = subprocess.run(IPMI_POWERSTATE_EXEC, capture_output=True).stdout.decode()
        psList = [x for x in res.split('\n') if x.find("PSU") != -1]
        for i in psList:
            thisPsStates = [x.strip() for x in i.split('|')]    # "PSU0_Supply      | 66h | ok  | 10.0 | Presence detected"
            psName = thisPsStates[0]
            psState = thisPsStates[-1]
            isOK = (psState == NORMAL_STATE)
            returnVal["power_supplies"].append({
                "name": psName,
                "ok": isOK,
                "status": psState
            })
    except Exception as e:
        returnVal["error"] = True
        returnVal["error_message"] = str(e)
    return returnVal

def checkIfHavePowerFailure(values: dict):
    stat = False
    info = ""
    try:
        for x in values["power_supplies"]:
            if not x["ok"]:
                info += "Power Supply %s failed." % (x["name"]) + "\n"
                info += "Info from %s: '%s'" % (x["name"], x["status"]) + "\n"
                stat = True
    except:
        pass
    return (stat, info)

def triggerShutdown(minute: int):
    logger("Scheduled shutdown in %d minute(s)." % (minute))
    return subprocess.run([SHUTDOWN_BIN, "+%d" % (minute)], capture_output=True).returncode

def cancelShutdown():
    logger("Canceled shutdown for AC back.")
    return subprocess.run([SHUTDOWN_BIN, "-c"], capture_output=True).returncode

def main(argv: list):
    isStartedShutdown = checkIfHavePowerFailure(getPowerState())[0]

    print("LYOI Power Controller ver %s" % VERSION)
    print("%d (c) %s\n" % (COPYRIGHT_YEAR, AUTHOR))
    logger("Script started, working hard to control power.")
    while True:
        ps = getPowerState()
        powerFailure = checkIfHavePowerFailure(ps)
        if powerFailure[0]:     # 0 is status
            if not isStartedShutdown:
                logger(powerFailure[1])     # 1 is info
                triggerShutdown(SHUTDOWN_TIMEOUT)
                isStartedShutdown = True
        else:
            if isStartedShutdown:
                cancelShutdown()
                isStartedShutdown = False
        time.sleep(1.0)

if __name__ == "__main__":
    main(sys.argv)
