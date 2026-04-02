from typing import Dict

def filter_students(data: Dict[str, float]) -> Dict[str, float]:
    return {name: score for name, score in data.items() if score >= 8}

# Test
print(filter_students({"An": 7, "Binh": 8.5, "Chi": 9}))