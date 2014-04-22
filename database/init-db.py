'''
config file rules:
    a) '#' started comments, until to the end of line
    b) commands split by the whitespace, multiple whitespaces treated as only one whitespace.
    c) if you want the command with whitespace please use the " to quote it.
    d) if you want use the " or # or \ as a literal, use \ to escape it.

example of data.txt:
    # hset users:1 id 1
    flushall
    hset users:1 name "jerry chou"
    hset users:1 age 30
    hset users:1 title software\ engineer
    hset users:1 base "\"shanghai\""
    hset users:1 salary "\"#9999\""
'''

import os
import redis

data_path = os.path.join(os.path.dirname(__file__), "data.txt")

rds = redis.StrictRedis(host='localhost', port=6379, db=0)

def config_scanner(cmd):
    flags = dict()
    flags["escape"] = False
    flags["quoted"] = False

    cmd_group = []
    cmd_buffer = ""
    for c in get_next_char(cmd):
        if c in ('#', '"', '\\', ' ') and flags["escape"]:
            cmd_buffer += c
            flags["escape"] = False
            continue
        elif c == '#':
            flags["escape"] = False
            break
        elif c == '"':
            flags["quoted"] = True
        elif c == '\\':
            flags["escape"] = True
        elif c == ' ':
            if flags["quoted"]:
                cmd_buffer += c
            else:
                cmd_group.append(cmd_buffer)
                cmd_buffer = ""
        else:
            cmd_buffer += c
            flags["escape"] = False

    if cmd_buffer:
        cmd_group.append(cmd_buffer)

    return cmd_group
    


def get_next_char(cmd):
    for c in cmd:
        yield c


if __name__ == "__main__":
    with open(data_path, 'rU') as f:
      for cmd in f:
        cmd = cmd.strip()
        if cmd:
            cmd_group = config_scanner(cmd)
            print cmd_group
            if cmd_group:
                print rds.execute_command(*cmd_group)