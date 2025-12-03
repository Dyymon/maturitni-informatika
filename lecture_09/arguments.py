import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-str", "--input_string", type=str, help="any kind of string")
parser.add_argument("-int", "--input_int", type=int, default=0, help="any kind of int, default is zero")
parser.add_argument("-bool", '--bool_flag', action='store_true')

args = parser.parse_args()

print(args.input_string)
print(args.input_int)
print(args.bool_flag)