# Lọc số chẵn và bình phương
def filter_and_square(numbers):
    result = []
    for num in numbers:
        if num % 2 == 0:
            result.append(num ** 2) 
    return result
