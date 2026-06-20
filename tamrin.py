
"""Tamrin 1"""
number = input("Enter a number: ")
if len(number) != 4 or not number.isnumeric():
    print("Please enter a number")
else:
    zero_count = number.count("0")
    print("zero counts:", zero_count)


"""Tamrin 2"""
number = input("Enter a number: ")

even_count = 0
odd_count = 0

for digit in number:
    if digit.isdigit():
        if int(digit) % 2 == 0:
            even_count +=1
        else:
            odd_count += 1

print("Even Digits:", even_count)
print("Odd Digits:", odd_count)


"""Tamrin 3"""
text = input("Enter: ")
print("*" * len(text))



"""Tamrin 4"""

def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

number = int(input("Enter a number: "))
if is_prime(number):
    print(f"{number} is a prime number")
else:
    print(f"{number} is not a prime number")


"""Tamrin 5"""

number = input("Enter input: ")

if len(number) % 2 != 0:
    print("the length of the number is odd:", len(number))
    print("Your input:", number)


