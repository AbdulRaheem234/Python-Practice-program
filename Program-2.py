def factorial(number):
    if number == 0 or number == 1:
        return 1
    else:
        return number * factorial(number - 1)


def factorialTrailingZeroes(number):
    count = 0

    while number >= 5:
        number = number // 5
        count += number
    return count


if __name__ == '__main__':
    number = int(input("Enter a number: "))

    print(
        f"Number of trailing zeros in {number}! is: {factorialTrailingZeroes(number)}")
