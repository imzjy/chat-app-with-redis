import os
import redis

data_path = os.path.join(os.path.dirname(__file__), "data.txt")

rds = redis.StrictRedis(host='localhost', port=6379, db=0)

with open(data_path, 'rU') as f:
  for cmd in f:
  	cmd = cmd.strip()
  	if cmd:
  		print cmd
  		print rds.execute_command(*cmd.split(' '))