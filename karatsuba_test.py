"""
Copyright (c) 2021 John "ComputerCraftr" Studnicka
Distributed under the MIT software license, see the accompanying
file COPYING or http://www.opensource.org/licenses/mit-license.php.

Multiplication tests and benchmarks
"""

import karatsuba
import random
import time

# Generate deterministic random testing data
random.seed(1)
multi_list = []

max_digits = 251
for j in range(2, max_digits, 1):
    multi_list.append([random.randint(10, 10 ** j), random.randint(10, 10 ** j)])
    # Build power map
    karatsuba.karatsuba_multiply_recursive(multi_list[-1][0], multi_list[-1][1])

start = time.process_time()
for multi_pair in multi_list:
    karatsuba.karatsuba_multiply_iterative(multi_pair[0], multi_pair[1])
end = time.process_time()
print('Iterative algo time elapsed:', end - start)

start = time.process_time()
for multi_pair in multi_list:
    karatsuba.karatsuba_multiply_recursive(multi_pair[0], multi_pair[1])
end = time.process_time()
print('Recursive algo time elapsed:', end - start)

test_element = max_digits // 4
print(str(multi_list[test_element][0]) + ' * ' + str(multi_list[test_element][1]) + ' =')
print('Long multiplication:', multi_list[test_element][0] * multi_list[test_element][1])
print('Karatsuba iterative:', karatsuba.karatsuba_multiply_iterative(multi_list[test_element][0],
                                                                     multi_list[test_element][1]))
print('Karatsuba recursive:', karatsuba.karatsuba_multiply_recursive(multi_list[test_element][0],
                                                                     multi_list[test_element][1]))