import redis
import json

rds = redis.StrictRedis(host='localhost', port=6379, db=0)

class Users(object):
    """docstring for Users"""
    def __init__(self):
            pass

    @staticmethod
    def get_friends(id):
            #print id
            friends = []
            friend_ids = rds.smembers('users:' + id + ':friends')

            for friend_id in friend_ids:
                friend = rds.hgetall('users:' + friend_id)
                friends.append(friend)

            return json.dumps(friends, 
                sort_keys=True,
                indent=4, 
                separators=(',', ': '))