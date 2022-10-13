# With Secure Coding Challenge
# Nilotpal Sarkar

# Part A
import json


# This class is to store temporarily, the key and value. An object of this class is instantiated as soon as we
# encounter an key(When the algorithm decides that the last set of charecters is predominantly a 'Key' The 'value'
# property is updated as soon as the algorithm is able to decide the 'value'. At this step, after evaluation of the
# 'value', the key and value of this entry object is flushed to  a root dictionary referred as json_dict in code.


class Entry:
    def __init__(self, key: str):
        self.key = key
        self.value = None

    def setValue(self, value: str):
        self.value = value


def parse_and_convert_to_json(input: str) -> str:
    buffer = []
    key: str = ''
    value: str = ''
    value_quote_started: bool = False
    json_dict = {}

    # Iterate over the string and parse
    for i in range(len(input)):
        current_char = input[i]
        previous_char = input[i - 1]

        # If the current character is a ':' and next char a space,
        # then according to challenge documentation, this marks the end of 'key'.
        if current_char == ':' and input[i + 1] == ' ':
            key = key.join(buffer)

            # Create an entry for the dictionary when we encounter an key.
            # When we parse the value, we would set the value of this entry.
            # Once we get the value, we would flush this entry to dict(json_dict)
            entry: Entry = Entry(key)

            # Set the key and buffer to empty and get ready for the next iterations.
            key = ''
            buffer = []
            continue

        # if quotation for the value is started state(marked simply by value True),
        # Also the current character is a "(quote)
        # And previous character was not escape character,
        # Then according to challenge documentation, this marks the end of value parsing.
        # At this stage, there are set of activities to be completed/flushed.
        #
        # - set the ongoing entry object's value to the value just parsed
        # - flush the entry value to json_dict object
        # - set the value, buffer, value_quote_started to defaults.
        if value_quote_started and current_char == '\"' and previous_char != "\\":
            value = value.join(buffer)
            entry.setValue(value)
            json_dict[entry.key] = entry.value
            value = ''
            buffer = []
            value_quote_started = False
            continue

        if current_char == '"' and previous_char != "\\" and (input[i - 1] is None or previous_char == ' '):
            value_quote_started = True

        # We would continue if the following conditions are met.
        # In these conditions we wouldnt like to append the current charecter to the buffer.
        if (current_char == ':' and input[i + 1] == ' ') \
                or (current_char == ' ' and previous_char == ':') \
                or (current_char == '\"' and previous_char == ' ') \
                or (current_char == ' ' and not value_quote_started):
            continue
        buffer.append(current_char)
    return json.dumps(json_dict, indent=2)


# open text file in read mode
text_file = open("event_data.txt", "r")

# read whole file to a string
data = text_file.read()

# close file
text_file.close()
json_string = parse_and_convert_to_json(data)

print(json_string)
