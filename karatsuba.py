"""
Copyright (c) 2021 John "ComputerCraftr" Studnicka
Distributed under the MIT software license, see the accompanying
file COPYING or http://www.opensource.org/licenses/mit-license.php.

Iterative Karatsuba multiplication algorithm
"""

number_base = 256


# Base 256 is one byte per digit
def integer_digits_base256(number):
    digits = 0

    # Divide by 256 until the number is rounded down to zero
    while number > 0:
        digits += 1
        number >>= 8  # Right shifting by 8 bits is equivalent to dividing by 256

    return digits


def karatsuba_split_inputs(multiplicand, multiplier):
    m2 = min(integer_digits_base256(multiplicand), integer_digits_base256(multiplier)) // 2  # m // 2

    # Use hash map instead of repeatedly calculating powers of number_base
    if m2 in karatsuba_split_inputs.power_map:
        m_digit_shift = karatsuba_split_inputs.power_map[m2][0]
        m2_digit_shift = karatsuba_split_inputs.power_map[m2][1]
    else:
        m2_digit_shift = 1 << (8 * m2)  # 1 << (8 * m2) = 2 ** (8 * m2) = 256 ** m2
        m_digit_shift = 1 << (16 * m2)  # m2_digit_shift * m2_digit_shift
        karatsuba_split_inputs.power_map[m2] = (m_digit_shift, m2_digit_shift)

    high1 = multiplicand // m2_digit_shift
    low1 = multiplicand % m2_digit_shift
    high2 = multiplier // m2_digit_shift
    low2 = multiplier % m2_digit_shift

    return [m_digit_shift, m2_digit_shift, high1, low1, high2, low2]


# Declare static dictionary variable for function above
karatsuba_split_inputs.power_map = dict()


def karatsuba_multiply_iterative(multiplicand, multiplier):
    # The node stack holds the input arguments to the Karatsuba multiplication function along with the branch of each
    # node in the tree with respect to its parent
    node_stack = [[multiplicand, multiplier, 0]]  # Assign root node with left branch 0

    # These stacks hold the results of lower depth calculations and maintain information about which higher order
    # calculations they belong to
    branch_path = []
    m_stack = []
    z_stack = [[], [], []]
    leaf_count = 0

    # Perform the tree traversal and calculate the results - since the recursive Karatsuba multiplication function calls
    # itself three times, this will be a ternary tree
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

            m_digit_shift = m_pair[0]
            m2_digit_shift = m_pair[1]

            z0 = z_stack[0].pop()
            z1 = z_stack[1].pop()
            z2 = z_stack[2].pop()

            # print('z0 = ' + str(z0) + ' z1 = ' + str(z1) + ' z2 = ' + str(z2))
            result = (z2 * m_digit_shift) + ((z1 - z2 - z0) * m2_digit_shift) + z0
            z_stack[last_branch].append(result)

    # The final result is pushed onto the left z0 stack, so we return it here
    return z_stack[0][0]


def karatsuba_multiply_recursive(multiplicand, multiplier):
    # Calculate multiplicand * multiplier
    if multiplicand < number_base or multiplier < number_base:
        return multiplicand * multiplier

    intermediate_results = karatsuba_split_inputs(multiplicand, multiplier)

    m_digit_shift = intermediate_results[0]
    m2_digit_shift = intermediate_results[1]

    high1 = intermediate_results[2]
    low1 = intermediate_results[3]
    high2 = intermediate_results[4]
    low2 = intermediate_results[5]

    z0 = karatsuba_multiply_recursive(low1, low2)
    z1 = karatsuba_multiply_recursive(low1 + high1, low2 + high2)
    z2 = karatsuba_multiply_recursive(high1, high2)

    # print('z0 = ' + str(z0) + ' z1 = ' + str(z1) + ' z2 = ' + str(z2))
    return (z2 * m_digit_shift) + ((z1 - z2 - z0) * m2_digit_shift) + z0
