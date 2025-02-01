def factorial(num):
    count = 1
    for n in range(1, num + 1):
        count *= n
    return count


def common_divisor(num1, num2):
    if num1 % num2 == 0:
        return num2
    else:
        return common_divisor(num2, num1 % num2)



