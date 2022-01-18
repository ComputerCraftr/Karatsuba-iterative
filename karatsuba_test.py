"""
Copyright (c) 2021-2022 John "ComputerCraftr" Studnicka

Multiplication tests and benchmarks
"""

import karatsuba
import random
import time

# Generate deterministic random testing data
random.seed(2)
multi_list = []
iterative_results = []
recursive_results = []

max_digits = 801
for j in range(2, max_digits, 1):
    multi_list.append([random.randint(10, 10 ** j), random.randint(10, 10 ** j)])

start = time.process_time()
for multi_pair in multi_list:
    iterative_results.append(karatsuba.karatsuba_multiply_iterative(multi_pair[0], multi_pair[1]))
end = time.process_time()
print('Iterative algo time elapsed:', end - start)

start = time.process_time()
for multi_pair in multi_list:
    recursive_results.append(karatsuba.karatsuba_multiply_recursive(multi_pair[0], multi_pair[1]))
end = time.process_time()
print('Recursive algo time elapsed:', end - start)

true_results = []
for multi_pair in multi_list:
    true_results.append(multi_pair[0] * multi_pair[1])
print('Results match:', iterative_results == recursive_results)
print('Iterative results accurate:', iterative_results == true_results)

test_element = max_digits // 4
print(str(multi_list[test_element][0]) + ' * ' + str(multi_list[test_element][1]) + ' =')
print('Long multiplication:', multi_list[test_element][0] * multi_list[test_element][1])
print('Karatsuba iterative:', karatsuba.karatsuba_multiply_iterative(multi_list[test_element][0],
                                                                     multi_list[test_element][1]))
print('Karatsuba recursive:', karatsuba.karatsuba_multiply_recursive(multi_list[test_element][0],
                                                                     multi_list[test_element][1]))
