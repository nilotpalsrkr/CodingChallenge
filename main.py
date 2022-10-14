# open text file in read mode
import base64
import json

from JsonConverter import parse_and_convert_to_json, get_next_event

# Take inputs from the file.
text_file = open("event_data.txt", "r")

# read whole file to a string
data = text_file.read()

# close file
text_file.close()
dict_result = parse_and_convert_to_json(data)
print(f"\nThe following string \n {data} \nJson converted to : \n{json.dumps(dict_result, indent=3)}")

# The hint is base64 encoded. This after decode gives - Hello, try XOR with 0x17F
# The trailing split operation is just fancy and may not be a maintainable one.
hint = base64.b64decode(dict_result['hint'].encode('ascii')).decode('utf-8').split(' ')[4]
fifth_hex = get_next_event(dict_result['three'], dict_result['four'], hint)

dict_result['five'] = fifth_hex

print(f"\n\nWe add the fifth key using the hint : {hint} and get another event : \n {json.dumps(dict_result, indent=2)}")