import numpy as np

def hex_to_binary_string(hex_string):
    bit_chars = [format(int(h, 16), "04b") for h in hex_string]
    return("".join(bit_chars))


def literal_packet_value(literal_packet_str):
    value = ""
    remainder = ""
    done = False
    for start_pos in np.arange(0, len(literal_packet_str), 5):
        if done:
            remainder = literal_packet_str[start_pos:]
            break

        prefix = literal_packet_str[start_pos]
        value_group = literal_packet_str[start_pos + 1:start_pos + 5]
        value += value_group
        if prefix == '0':
            done = True

    return((int(value, 2), remainder))

def get_packet_metadata(packet_str):
    version = packet_str[:3]
    version_int = int(version, 2)
    packet_type = packet_str[3:6]
    packet_type_int = int(packet_type, 2)
    #print("version", version_int, "type", packet_type_int)
    return((version_int, packet_type_int))

def parse_packets(packet_str, version_sum):
        
    version_int, packet_type_int = get_packet_metadata(packet_str)
    remainder = packet_str[6:]
    #print("version", version_int, "type", packet_type_int)
    #print(remainder)
    #print(version_sum)
    version_sum += version_int

    if packet_type_int == 4:
        # literal
        _, remainder = literal_packet_value(remainder)

        # Just return the version number
        return((version_sum, remainder))

    else:
        
        length_type = remainder[0]
        #print("Length type", length_type)
        remainder = remainder[1:]
        if length_type == '0':
            length_bin = remainder[:15]
            sub_packets_len = int(length_bin, 2)
            remainder = remainder[15:]
            #print("Sub packet len", sub_packets_len)
            #print("remainder len", len(remainder))
            sub_packets_remainder = remainder[:sub_packets_len]
            ## get packets
            while sub_packets_remainder != "":
                version_sum, sub_packets_remainder = parse_packets(sub_packets_remainder, version_sum)

            remainder = remainder[sub_packets_len:]
            #print("New remainder len", len(sub_packets_remainder))
        elif length_type == '1':
            num_sub_packets = int(remainder[:11], 2)
            remainder = remainder[11:]
            
            for _ in range(num_sub_packets):
                version_sum, remainder = parse_packets(remainder, version_sum)

        #version_sum += version_int
        return((version_sum, remainder))

with open("Day16/input_AJRF.txt", "r") as f:
    packet_hex = f.readline().strip()

#packet_hex = "8A004A801A8002F478"
#packet_hex = "620080001611562C8802118E34"
#packet_hex = "C0015000016115A2E0802F182340"
#packet_hex = "A0016C880162017C3686B18A3D4780"

packet_str = hex_to_binary_string(packet_hex)

#packet_str = "110100101111111000101000"
#packet_str = "00111000000000000110111101000101001010010001001000000000"
#packet_str = "11101110000000001101010000001100100000100011000001100000"

version_sum, remainder = parse_packets(packet_str, 0)
print("Version sum", version_sum)

## Part 2

## Product function: np.prod() uses modular maths so will just wrap round with big numbers
## leading to odd results.
## THIS TOOK ME AGES TO REALISE!  Python 3.8 has a built-in math.prod()
def prod(iterable):
    product = np.prod([float(item) for item in iterable])
    return(product)


def parse_packets_properly(packet_str):
        
    _, packet_type_int = get_packet_metadata(packet_str)
    remainder = packet_str[6:]

    if packet_type_int == 4:
        # literal
        value, remainder = literal_packet_value(remainder)

        # Just return the version number
        return((value, remainder))

    else:
 
        length_type = remainder[0]

        remainder = remainder[1:]
        values = []
        if length_type == '0':
            length_bin = remainder[:15]
            sub_packets_len = int(length_bin, 2)
            remainder = remainder[15:]
            sub_packets_remainder = remainder[:sub_packets_len]
            ## get packets
            while sub_packets_remainder != "":
                value, sub_packets_remainder = parse_packets_properly(sub_packets_remainder)
                values.append(value)

            remainder = remainder[sub_packets_len:]
        elif length_type == '1':
            num_sub_packets = int(remainder[:11], 2)
            remainder = remainder[11:]
            
            for _ in range(num_sub_packets):
                value, remainder = parse_packets_properly(remainder)
                values.append(value)
        
        if packet_type_int == 0:
            result = sum(values)
        elif packet_type_int == 1:
            result = prod(values)
        elif packet_type_int == 2:
            result = min(values)
        elif packet_type_int == 3:
            result = max(values)
        elif packet_type_int == 5:
            result = [0,1][values[0] > values[1]]
        elif packet_type_int == 6:
            result = [0,1][values[0] < values[1]]
        elif packet_type_int == 7:
            result = [0,1][values[0] == values[1]]
        else:
            raise ValueError(packet_type_int)

        print("Type", packet_type_int, "values", "".join([str(value)+"," for value in values]), "result", result)

        return((result, remainder))

with open("Day16/input_AJRF.txt", "r") as f:
    packet_hex = f.readline().strip()

# packet_hex = "C200B40A82" # finds the sum of 1 and 2, resulting in the value 3.
# packet_hex = "04005AC33890" #finds the product of 6 and 9, resulting in the value 54.
# packet_hex = "880086C3E88112" #finds the minimum of 7, 8, and 9, resulting in the value 7.
# packet_hex = "CE00C43D881120" #finds the maximum of 7, 8, and 9, resulting in the value 9.
# packet_hex = "D8005AC2A8F0" #produces 1, because 5 is less than 15.
# packet_hex = "F600BC2D8F" #produces 0, because 5 is not greater than 15.
# packet_hex = "9C005AC2F8F0" #produces 0, because 5 is not equal to 15.
# packet_hex = "9C0141080250320F1802104A08" # produces 1, because 1 + 3 = 2 * 2.

packet_str = hex_to_binary_string(packet_hex)

value, remainder = parse_packets_properly(packet_str) 
print("Final value", value)
