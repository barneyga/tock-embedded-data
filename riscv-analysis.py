from operator import itemgetter
import matplotlib.pyplot as plt
from collections import defaultdict
# pip3 install mplcursors
import mplcursors


syms = open('lto-on-earl-objects.txt', 'r')
lines = syms.readlines()

byte_ct = 0
d = {}
for line in lines:
    spl = line.split()
    hexed = int(spl[4], 16)
    byte_ct += hexed
    d[spl[0]] = (spl[5], int(hexed))

print(byte_ct)

for k, v in d.items():
    print(k + ' : ' + str(v))

# dictionary of symbol to instruction addresses that they're in...
risc = open('earl_dump_lto-on.txt', 'r')
lines = risc.readlines()
sym_addrs = list(d.keys())
address_d = defaultdict(list)
# could make this faster ofc
for sym in sym_addrs:
    for line in lines:
        spl = line.split()
        if sym in line and sym != spl[0]:
            address_d[sym].append(spl[0][:-1])

for k, v in address_d.items():
    # every value list has at least 1 value (the key itself)
    print(k + ' : ' + str(v))

# translate this address dictionary's values to parent functions


def trace_instruction_to_function(instruction_addr):
    # there are more sophisticated ways to do this, yes.
    most_recent_function = None
    for line in lines:
        if instruction_addr in line:
            return most_recent_function
        if '>:' in line:
            most_recent_function = line[9:-2]


addr_func_d = defaultdict(list)
for k, v in address_d.items():
    # every value list has at least 1 value (the key itself)
    for value in v:
        if value != k:
            addr_func_d[k].append(trace_instruction_to_function(value))

temp_d = {}
for k in sorted(addr_func_d.keys()):
    temp_d[k] = addr_func_d[k]
addr_func_d = temp_d
sym_magnitudes = {}
for k, v in addr_func_d.items():
    sym_magnitudes[k] = len(v)
# for k, v in addr_func_d.items():
#     # every value list has at least 1 value (the key itself)
#     print(k + ' : ' + str(v))

# count all the function names in these value lists

counter = defaultdict(int)
for k, v in addr_func_d.items():
    for value in v:
        counter[value] += 1

# for k, v in counter.items():
#     print(k + ' : ' + str(v))

# find all unreferenced strings
unreferenced = []
for k, v in address_d.items():
    # every value list has at least 1 value (the key itself)
    if len(v) == 1:
        unreferenced.append(k)
# for item in unreferenced:
#     print(d[item])


plt.bar(*zip(*counter.items()))
plt.title('Amount of string references by function, sorted by address')
plt.xlabel('Functions (mangled)')
plt.ylabel('Number of embedded strings')
# plt.xticks(rotation=90)
# todo: would like the yticks to show every number
plt.xticks(ticks=[])
mplcursors.cursor(hover=True)
plt.show()


# bytes as y-axis instead.
byte_counter = defaultdict(int)
for k, v in addr_func_d.items():
    bites = d[k][1]
    for value in v:
        byte_counter[value] += bites
temp_d = {}
for k in counter:
    temp_d[k] = byte_counter[k]
byte_counter = temp_d
plt.bar(*zip(*byte_counter.items()))
plt.title('Function byte usage, sorted by address')
plt.xlabel('Functions (mangled)')
plt.ylabel('Amount of bytes it references')
# plt.xticks(rotation=90)
plt.xticks(ticks=[])
mplcursors.cursor(hover=True)
plt.show()


# sort this one by increasing
sorted_byte_counter = {k: v for k, v in sorted(
    byte_counter.items(), key=itemgetter(1))}
plt.yscale('log')
plt.bar(*zip(*sorted_byte_counter.items()))
plt.title('Functions sorted by byte usage')
plt.xlabel('Functions (mangled)')
plt.ylabel('Amount of bytes (log scale)')
# plt.xticks(rotation=90)
plt.xticks(ticks=[])
mplcursors.cursor(hover=True)
plt.show()

# x-axis being strings (could dereference these strings)
# y-axis being amount of times referenced
plt.bar(*zip(*sym_magnitudes.items()))
plt.title('Amount of times strings are referenced')
plt.xlabel('Strings')
plt.ylabel('Number of references')
# plt.xticks(rotation=90)
plt.xticks(ticks=[])
mplcursors.cursor(hover=True)
plt.show()

# next steps:
# rather than finding the parent function of a string, find the function that
# we are loading this string into a register for. i.e. jalr's,,, maybe beqz's?
# this won't be as fruitful as we'd expect, most likely. As we can still attribute many
# specific embedded strings to panic functions without this.

# after that, working out Lanon vs L__unnamed would be interesting.

# for the reader's sake, could deref each string
# make these graphs interactive by putting them on a notebook.
# I haven't bothered looking at exclusively panic stuff for riscv yet, nor
# have I compiled without the panic handler.
