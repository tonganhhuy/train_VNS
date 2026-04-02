# Gom nhóm các từ theo độ dài
from typing import List, Dict
def group_by_length_comp(words: List[str]) -> Dict[int, List[str]]:
    """Gom nhóm từ theo độ dài sử dụng Comprehension lồng nhau."""
    unique_lengths = {len(word) for word in words}
    return {
        length: [word for word in words if len(word) == length]
        for length in unique_lengths
    }
# Test
input_words = ['apple', 'bat', 'cat', 'banana', 'dog', 'elephant']
print(group_by_length_comp(input_words))