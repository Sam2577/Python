


def sum_a_list(a_list):
    number = None
    if len(a_list) == 1:
        return a_list[0]
    number = a_list.pop()
    return number + sum_a_list(a_list)

print(sum_a_list([1,2,3,4,5]))
