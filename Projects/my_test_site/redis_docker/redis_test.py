import redis
import json5
import re

REDIS_CONNECTION = None

def init_redis(host='localhost', port=6379,db=0):
    global REDIS_CONNECTION
    if not REDIS_CONNECTION:
        REDIS_CONNECTION = redis.Redis(host=host, port=port,db=db,decode_responses=True)
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
    
    




def extract_json(text):
    json_objects = []
    # json_pattern = re.compile(r'\{.*?\}|\[.*?\]', re.DOTALL)
    """Extracts JSON content from a given text."""
    # json_pattern = re.compile(r'\{.*?\}|\[.*?\]', re.DOTALL)
    # This pattern looks for JSON objects that end with a quote then a closing brace.
    json_pattern = re.compile(r'\{.*?"\}|\[.*?\]', re.DOTALL)

    for match in json_pattern.findall(text):
        try:
            parsed_json = json5.loads(match)  # json5 handles more flexible JSON formats
            json_objects.append(parsed_json)
        except Exception as e:
            print("Exception = ",e)
            print("input was = ", match)
            continue  # Skip invalid JSON structures
    chat_content = ""
    for i,obj in enumerate(json_objects):
        print(i," json_obj = ", obj)  # Extracted JSON objects
        if 'v' in obj:
            chat_content += str(obj['v'])

    chat_content = chat_content.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")
    print("final chat content = ", chat_content)

    return chat_content

     

def test():
    redis_connection = redis.Redis(host='localhost', port=6379,db=0,decode_responses=True)
    redis_connection.set('my_test_key', "my_test_value")
    redis_connection.set('chat_input', "java 8 examples")
    value = redis_connection.get('my_test_key')
    # value = value.decode("UTF-8")
    print(value)
    keys = redis_connection.keys('*')
    print(keys)
    # for i,key in enumerate(keys):
    #     print(i, " ",key, ' = ', redis_connection.get(key))
    value = redis_connection.get('chat_response')
    print("content = " ,value)
    json_data = extract_json(value)

    


if __name__=='__main__':
    test()
    
