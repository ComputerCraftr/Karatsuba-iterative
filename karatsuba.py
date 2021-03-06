"""
Copyright (c) 2021-2022 John "ComputerCraftr" Studnicka

Iterative Karatsuba multiplication algorithm
"""

from collections import deque

number_base_bit_shift = 16
number_base = 1 << number_base_bit_shift  # 65536


# Base 65536 is two bytes per digit
def integer_digits_base_n(number):
    digits = 0

    # Divide by the base until the number is rounded down to zero
    while number > 0:
        digits += 1
        number >>= number_base_bit_shift  # Right shifting by 16 bits is equivalent to dividing by 65536

    return digits


def karatsuba_split_inputs(multiplicand, multiplier):
    # m2 is half of the number of digits in the smaller multi
    m2 = min(integer_digits_base_n(multiplicand), integer_digits_base_n(multiplier)) >> 1  # m // 2

    # Calculate powers of the base to restore the proper number of digits to split numbers
    m2_digit_shift_bits = m2 * number_base_bit_shift
    m_digit_shift_bits = m2_digit_shift_bits << 1  # double m2 bits
    # 1 << (16 * m2) = 2 ** (16 * m2) = 65536 ** m2

    # Split the numbers to have half of the number of digits in the smaller multi - divide and conquer
    # Remove the low digits using truncated division or right shifts
    high1 = multiplicand >> m2_digit_shift_bits  # multiplicand // 65536 ** m2
    high2 = multiplier >> m2_digit_shift_bits
    # Remove the high digits using modulo or subtraction
    low1 = multiplicand - (high1 << m2_digit_shift_bits)  # multiplicand % 65536 ** m2
    low2 = multiplier - (high2 << m2_digit_shift_bits)

    return [m_digit_shift_bits, m2_digit_shift_bits, high1, low1, high2, low2]


def karatsuba_multiply_iterative(multiplicand, multiplier):
    # The node stack holds the input arguments to the Karatsuba multiplication function along with the branch of each
    # node in the tree with respect to its parent
    node_stack = deque([[multiplicand, multiplier, 0]])  # Assign root node with left branch 0

    # These stacks hold the results of lower depth calculations and maintain information about which higher order
    # calculations they belong to
    branch_path = deque()
    m_stack = deque()
    z_stack = [deque(), deque(), deque()]
    leaf_count = 0

    # Perform the depth first tree traversal and calculate the results - since the recursive Karatsuba multiplication
    # function calls itself three times, this will be a ternary tree
    while node_stack:
        current_node = node_stack.pop()
        multiplicand_temp = current_node[0]
        multiplier_temp = current_node[1]
        branch = current_node[2]

        # Note: every node here is guaranteed to have 3 children if it is not a leaf
        if multiplicand_temp >= number_base and multiplier_temp >= number_base:
            intermediate_results = karatsuba_split_inputs(multiplicand_temp, multiplier_temp)

            m_digit_shift_temp = intermediate_results[0]
            m2_digit_shift_temp = intermediate_results[1]

            high1 = intermediate_results[2]
            low1 = intermediate_results[3]
            high2 = intermediate_results[4]
            low2 = intermediate_results[5]

            # The last appended values here are traversed first due to the last in first out nature of stacks
            node_stack.append([high1, high2, 2])  # z2 - right
            node_stack.append([low1 + high1, low2 + high2, 1])  # z1 - center
            node_stack.append([low1, low2, 0])  # z0 - left

            # The branch path and m stacks implicitly keep track of node depth while we are performing calculations
            branch_path.append(branch)
            m_stack.append([m_digit_shift_temp, m2_digit_shift_temp])
            leaf_count = 0
        else:
            # Leaf nodes are all single digit multiplications
            # Calculate multiplicand * multiplier
            z_stack[leaf_count].append(multiplicand_temp * multiplier_temp)

            # We take advantage of the fact that, while the child nodes can have additional branches at lower depths on
            # the center or center and right nodes, the left node will always be a leaf
            if leaf_count != 2:
                leaf_count += 1

        # We only need to check if the z2 stack is not empty here because the right z2 branch is always traversed last
        # and this implies that the z0 and z1 stacks are also not empty, meaning there are still calculations to perform
        while z_stack[2]:
            last_branch = branch_path.pop()
            m_pair = m_stack.pop()

            m_digit_shift_bits = m_pair[0]
            m2_digit_shift_bits = m_pair[1]

            z0 = z_stack[0].pop()
            z1 = z_stack[1].pop()
            z2 = z_stack[2].pop()

            # print('z0 = ' + str(z0) + ' z1 = ' + str(z1) + ' z2 = ' + str(z2))
            result = (z2 << m_digit_shift_bits) + ((z1 - z2 - z0) << m2_digit_shift_bits) + z0
            z_stack[last_branch].append(result)

    # The final result is pushed onto the left z0 stack, so we return it here
    return z_stack[0][0]


def karatsuba_multiply_recursive(multiplicand, multiplier):
    # Calculate multiplicand * multiplier
    if multiplicand < number_base or multiplier < number_base:
        return multiplicand * multiplier

    intermediate_results = karatsuba_split_inputs(multiplicand, multiplier)

    m_digit_shift_bits = intermediate_results[0]
    m2_digit_shift_bits = intermediate_results[1]

    high1 = intermediate_results[2]
    low1 = intermediate_results[3]
    high2 = intermediate_results[4]
    low2 = intermediate_results[5]

    z0 = karatsuba_multiply_recursive(low1, low2)
    z1 = karatsuba_multiply_recursive(low1 + high1, low2 + high2)
    z2 = karatsuba_multiply_recursive(high1, high2)

    # print('z0 = ' + str(z0) + ' z1 = ' + str(z1) + ' z2 = ' + str(z2))
    return (z2 << m_digit_shift_bits) + ((z1 - z2 - z0) << m2_digit_shift_bits) + z0
