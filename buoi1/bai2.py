from typing import List, Dict

def count_freq(arr: List[str]) -> Dict[str, int]:
    return {x: arr.count(x) for x in set(arr)}

# Test
print(count_freq(['a', 'b', 'a', 'c', 'b']))