import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import validate_input

def test_validation():
    test_cases = [
        ("", "Empty string"),
        ("a", "Single character"),
        ("ááááááááá", "Repeated characters"),
        ("ádascxzcsaf ádasdtetreyhtryujytj43543%$#%sxzcvxc", "Spam text"),
        ("hello world", "English text"),
        ("Sản phẩm này rất tốt", "Valid Vietnamese"),
        ("a" * 1001, "Too long text"),
        ("123456789", "Numbers only"),
        ("!@#$%^&*()", "Special chars only"),
        ("ok", "Short valid word"),
        ("Tôi thích sản phẩm này", "Valid Vietnamese sentence"),
    ]

    print("🧪 Testing Input Validation Function")
    print("=" * 50)

    for i, (test_input, description) in enumerate(test_cases, 1):
        is_valid, error_msg = validate_input(test_input)
        status = "✅ VALID" if is_valid else "❌ INVALID"

        print(f"Test {i}: {description}")
        print(f"Status: {status}")
        if not is_valid:
            print(f"Error: {error_msg}")
        print(f"Input: '{test_input[:60]}...'" if len(test_input) > 60 else f"Input: '{test_input}'")
        print("-" * 30)

if __name__ == "__main__":
    test_validation()