def factorial(num: int) -> int:
    """
    Calculates the factorial of a number.

    Parameters:
    num (int): The number for which the factorial is to be calculated.

    Returns:
    int: The factorial of the number `num`.
    """

    count = 1
    for n in range(1, num + 1):
        count *= n
    return count


def common_divisor(num1: int, num2: int) -> int:
    """
    Calculates the greatest common divisor (GCD) of two numbers using the Euclidean algorithm.

    Parameters:
    num1 (int): The first number.
    num2 (int): The second number.

    Returns:
    int: The greatest common divisor (GCD) of `num1` and `num2`.
    """

    if num1 % num2 == 0:
        return num2
    else:
        return common_divisor(num2, num1 % num2)



