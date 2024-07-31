import redis

REDIS_CONNECTION = None

def init_redis(host='localhost', port=6379,db=0):
    global REDIS_CONNECTION
    if not REDIS_CONNECTION:
        REDIS_CONNECTION = redis.Redis(host=host, port=port,db=db)
    return REDIS_CONNECTION

def set_redis_keys_from_cmd_list(cmd_list:list):
    redis_connection = init_redis()
    # clear the recent value of key cmds
    print("Deleting previous cmds from database")
    val = redis_connection.delete("CMDS")
    print(val)

    print("Adding keys into database : CMDS array")
    for cmd in cmd_list:
        redis_connection.rpush("CMDS",cmd)
    
    print("checking keys from database : CMDS array")
    val = redis_connection.lrange("CMDS",0,-1)
    new_val = [v.decode('utf-8') for v in val]
    for i,cmd in enumerate(new_val):
        print(f"{i} : {cmd}")
    
    
     

def test():
    redis_connection = redis.Redis(host='localhost', port=6379,db=0)
    redis_connection.set('my_test_key', "my_test_value")
    value = redis_connection.get('my_test_key')
    value = value.decode("UTF-8")
    print(value)
    print(redis_connection.keys('*'))


if __name__=='__main__':
    test()
    
