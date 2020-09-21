#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# exec command: ipmitool sdr type "Power Supply"

import sys

lost = False

def main(argv):
    if lost:
        print("""Total_Power      | 2Ch | ok  | 23.0 | 165 Watts
PSU0_Supply      | 66h | ok  | 10.0 | Presence detected
PSU1_Supply      | 67h | ok  | 10.1 | Presence detected, Power Supply AC Lost""")
    else:
        print("""Total_Power      | 2Ch | ok  | 23.0 | 165 Watts
PSU0_Supply      | 66h | ok  | 10.0 | Presence detected
PSU1_Supply      | 67h | ok  | 10.1 | Presence detected""")

if __name__ == "__main__":
    main(sys.argv)
