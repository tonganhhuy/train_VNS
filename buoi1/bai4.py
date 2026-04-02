# Kiểm tra chuỗi Palindrome
def is_palindrome_simple(text: str) -> bool:
    """Kiểm tra Palindrome bằng cách đảo ngược chuỗi (Slicing)."""
    return text == text[::-1]
# Test
print(is_palindrome_simple("radar"))  
print(is_palindrome_simple("python"))