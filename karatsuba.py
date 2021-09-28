"""
Copyright (c) 2021 John "ComputerCraftr" Studnicka
Distributed under the MIT software license, see the accompanying
file COPYING or http://www.opensource.org/licenses/mit-license.php.

Iterative Karatsuba multiplication algorithm
"""


def karatsuba_calculation_inner(multiplicand, multiplier):
    m = min(len(str(multiplicand)), len(str(multiplier)))
    m2 = m // 2
    # If m is odd then subtract one to make it equal to 2 * m2 for use in the final calculation
    if m & 1:
        m -= 1

    # Use hash map instead of repeatedly calculating powers of 10
    if m in karatsuba_calculation_inner.power_map:
        m_digit_shift = karatsuba_calculation_inner.power_map[m][0]
        m2_digit_shift = karatsuba_calculation_inner.power_map[m][1]
    else:
        m_digit_shift = 10 ** m
        m2_digit_shift = 10 ** m2
        karatsuba_calculation_inner.power_map[m] = (m_digit_shift, m2_digit_shift)

    high1 = multiplicand // m2_digit_shift
    low1 = multiplicand % m2_digit_shift
    high2 = multiplier // m2_digit_shift
    low2 = multiplier % m2_digit_shift

    return [m_digit_shift, m2_digit_shift, high1, low1, high2, low2]


# Declare static dictionary variable for function above
karatsuba_calculation_inner.power_map = dict()


def karatsuba_multiply_iterative(multiplicand, multiplier):
    # Calculate multiplicand * multiplier
    if multiplicand < 10 or multiplier < 10:
        return multiplicand * multiplier

    # The first stack holds the input arguments to the Karatsuba multiplication function along with the branch of each
    # node in the tree with respect to its parent
    first_stack = [[multiplicand, multiplier, 0]]  # Assign root node with left branch 0
    # The second stack also holds the function input arguments and some intermediary results to avoid performing repeat
    # calculations below along with the branch of the node
    second_stack = []

    # Perform the tree traversal using two stacks - since the recursive Karatsuba multiplication function calls itself
    # three times, this will be a ternary tree
    while first_stack:
        current_node = first_stack.pop()
        multiplicand_temp = current_node[0]
        multiplier_temp = current_node[1]
        branch = current_node[2]
        second_stack.append([multiplicand_temp, multiplier_temp, 0, 0, branch])

        # Note: every node here is guaranteed to have 3 children if it is not a leaf
        if multiplicand_temp >= 10 and multiplier_temp >= 10:
            result = karatsuba_calculation_inner(multiplicand_temp, multiplier_temp)

            second_stack[-1][2] = result[0]  # m_digit_shift
            second_stack[-1][3] = result[1]  # m2_digit_shift

            high1 = result[2]
            low1 = result[3]
            high2 = result[4]
            low2 = result[5]

            # The last appended values here are traversed first due to the last in first out nature of stacks
            first_stack.append([high1, high2, 2])  # z2 - right
            first_stack.append([low1 + high1, low2 + high2, 1])  # z1 - center
            first_stack.append([low1, low2, 0])  # z0 - left

    branch_path = []
    m_stack = []
    z_stack = [[], [], []]
    leaf_count = 0

    for k in range(len(second_stack)):
        current_node = second_stack[k]
        m_temp = current_node[2]
        branch = current_node[4]

        # m is nonzero for every node which has children (non leaf nodes)
        if m_temp != 0:
            # The branch path and m stacks implicitly keep track of node depth while we are performing calculations
            branch_path.append(branch)
            m_stack.append(current_node[2:4])
            leaf_count = 0
        else:
            # Leaf nodes are all single digit multiplications
            # Calculate multiplicand * multiplier
            z_stack[leaf_count].append(current_node[0] * current_node[1])

            # We take advantage of the fact that, while the child nodes can have additional branches at lower depths on
            # the center or center and right nodes, the left node will always be a leaf
            leaf_count = min(leaf_count + 1, 2)

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
    if multiplicand < 10 or multiplier < 10:
        return multiplicand * multiplier

    result = karatsuba_calculation_inner(multiplicand, multiplier)

    m_digit_shift = result[0]
    m2_digit_shift = result[1]

    high1 = result[2]
    low1 = result[3]
    high2 = result[4]
    low2 = result[5]

    z0 = karatsuba_multiply_recursive(low1, low2)
    z1 = karatsuba_multiply_recursive(low1 + high1, low2 + high2)
    z2 = karatsuba_multiply_recursive(high1, high2)

    # print('z0 = ' + str(z0) + ' z1 = ' + str(z1) + ' z2 = ' + str(z2))
    return (z2 * m_digit_shift) + ((z1 - z2 - z0) * m2_digit_shift) + z0


# Compare results
multi_list = [[189, 811], [716751, 643108], [5629806318, 846726235]]

for j in range(len(multi_list)):
    print(str(multi_list[j][0]) + ' * ' + str(multi_list[j][1]) + ' =')
    print('Long multiplication:', multi_list[j][0] * multi_list[j][1])
    print('Karatsuba recursive:', karatsuba_multiply_recursive(multi_list[j][0], multi_list[j][1]))
    print('Karatsuba iterative:', karatsuba_multiply_iterative(multi_list[j][0], multi_list[j][1]))