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

class Messages(object):
    """docstring for Messages"""
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
                ret_val = rds.lpush("users:%s:message:%s" % (msg['to'], msg['from']),
                    json.dumps(santinizedMsg))
                rds.lpush("users:%s:messages:%s:unread" % (msg['to'], msg['from']), 
                    json.dumps(santinizedMsg))
                rds.sadd("users:%s:messages:new" % msg['to'], msg['from'])
            except Exception, e:
                return (0, str(e))

            return (ret_val, msg['text'])

    @staticmethod
    def get_unread(from_id, to_id):
            #print id
            unread_message = rds.rpop("users:%s:messages:%s:unread" % (from_id, to_id))
            if unread_message:
                return unread_message
            else:
                return '{}'

    @staticmethod
    def get_friend_ids_for_new_message(id):
            #print id
            friend_ids = rds.smembers("users:%s:messages:new" % id)
            rds.delete("users:%s:messages:new" % id)
            return json.dumps(list(friend_ids), 
                sort_keys=True,
                indent=4, 
                separators=(',', ': ')) 