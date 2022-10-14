# With Secure Coding Challenge
# Nilotpal Sarkar

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
    return json_dict


# This function returns the next event based on the following algorithm. The next hex is ensured using 2-step process
# Step - 1.
# A difference of numbers in sequence is calculated. That is : hex sequence- 0x154, 0x150, 0x14A, 0x144 Diff
# sequence- -4, -6, -6 Now, the next difference in the sequence could be either of 4, 6, 8 etc. This difference is
# confirmed with the hint given and we move to the next step.

# Step - 2.
# The hint says - Hello, try XOR with 0x17F
# So we, start XOR'ng each number in sequence with 0x17F
# and we get the following sequence - 43, 47, 53, 59.
# Difference of xor'ed sequence - 4, 6, 6

# We see a similar sequence getting generated and so for the next step, we take this difference and match with step 1.
# If the difference matches, we confirm the hex number and return.
def get_next_event(prev_hex_number: int, current_hex_number: int, hint_hex: int):
    prev_dec_number = int(prev_hex_number, 16)
    current_dec_number = int(current_hex_number, 16)
    diff_of_decimals = current_dec_number - prev_dec_number
    possible_next_number = current_dec_number + diff_of_decimals

    prev_xor = int(prev_hex_number, 16) ^ int(hint_hex, 16)
    current_xor = int(current_hex_number, 16) ^ int(hint_hex, 16)

    diff_between_xors = current_xor - prev_xor
    possible_next_number_from_plain_difference = current_dec_number + diff_of_decimals

    # Final step that makes use of the hint
    possible_next_number_from_plain_difference_XOR_hint = possible_next_number_from_plain_difference ^ int(hint_hex, 16)
    if possible_next_number_from_plain_difference_XOR_hint - current_xor == diff_between_xors:
        # In this case we find the difference from 2 different calculations merging to the same difference. 
        # Hense assuming the difference is correct and we proceed for the next item(5th) with
        # this difference.
        return hex(possible_next_number)
