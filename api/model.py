import sys
import time
import json
import redis

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

class Message(object):
    """docstring for Message"""
    def __init__(self):
            pass

    '''
    return a tuple 
    if success return (lengn_of_list, msg text)
    else return (0, error message)
    '''
    @staticmethod
    def save(json_msg):
        msg = {}
        try:
            msg = json.loads(json_msg)
        except ValueError, e:
            print e
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        if msg:
            santinizedMsg = {}
            santinizedMsg['text'] = msg['text']
            santinizedMsg['time'] = time.time()
            try:
                ret_val = rds.lpush("users:%s:msgbox:%s" % (msg['to'], msg['from']),
                    json.dumps(santinizedMsg))
            except Exception, e:
                return (0, str(e))

            return (ret_val, msg['text'])