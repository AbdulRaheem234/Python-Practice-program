def fibonacci_iterative(n):
    if n <= 0:
        return "Input should be a positive integer"
    elif n == 1:
        return 0
    elif n == 2:
        return 1

    a, b = 0, 1
    for _ in range(3, n+1):
        a, b = b, a + b
    return b


# Example usage
n = 10
print(f"The {n}th term in Fibonacci series (iterative) is:",
      fibonacci_iterative(n))
