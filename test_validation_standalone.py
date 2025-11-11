import re

def validate_input(text):
    """
    Validate input text for Vietnamese sentiment analysis.
    Returns (is_valid, error_message)
    """
    if not text or text.strip() == "":
        return False, "❌ Vui lòng nhập văn bản!"

    text = text.strip()

    # Check minimum length (after stripping)
    if len(text) < 3:
        return False, "❌ Văn bản quá ngắn! Vui lòng nhập ít nhất 3 ký tự."

    # Check maximum length
    if len(text) > 500:
        return False, "❌ Văn bản quá dài! Vui lòng nhập dưới 500 ký tự."

    # Check for Vietnamese characters (must contain at least some Vietnamese chars)
    vietnamese_chars = 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ'
    has_vietnamese = any(char in vietnamese_chars for char in text)

    if not has_vietnamese:
        return False, "❌ Vui lòng nhập văn bản bằng tiếng Việt!"

    # Calculate meaningful characters ratio
    total_chars = len(text)
    meaningful_chars = sum(1 for char in text if char.isalnum() or char in vietnamese_chars or char in ' .,;!?')
    meaningful_ratio = meaningful_chars / total_chars

    if meaningful_ratio < 0.3:  # Less than 30% meaningful characters
        return False, "❌ Văn bản có quá nhiều ký tự đặc biệt! Vui lòng nhập văn bản có nghĩa."

    # Check for keyboard mashing (repeated characters)
    if re.search(r'(.)\1{4,}', text):  # 5+ repeated characters
        return False, "❌ Phát hiện ký tự lặp lại! Vui lòng nhập văn bản có nghĩa."

    # Check for excessive consecutive consonants (likely spam)
    consonants = 'bcdfghjklmnpqrstvwxyzđ'
    max_consonant_streak = max(len(match) for match in re.findall(f'[{consonants}]+', text.lower()))
    if max_consonant_streak > 8:
        return False, "❌ Văn bản có vẻ như spam! Vui lòng nhập câu tiếng Việt có nghĩa."

    # Additional spam detection: random keyboard patterns
    keyboard_patterns = [
        r'qwer', r'asdf', r'zxcv', r'1234', r'qwerty', r'asdfgh', r'zxcvbnm',
        r'qaz', r'wsx', r'edc', r'rfv', r'tgb', r'yhn', r'ujm', r'ik,', r'ol.',
        r'p;/', r'[\[\]{}|\\:;"<>?]', r'[=-_+`~]'
    ]
    text_lower = text.lower()
    spam_score = 0
    for pattern in keyboard_patterns:
        if re.search(pattern, text_lower):
            spam_score += 1

    # If multiple keyboard patterns detected, likely spam
    if spam_score >= 3:
        return False, "❌ Phát hiện pattern bàn phím spam! Vui lòng nhập văn bản có nghĩa."

    return True, "✅ Văn bản hợp lệ!"

# Test cases
test_cases = [
    ("", "Empty string"),
    ("a", "Single character"),
    ("ááááááááá", "Repeated Vietnamese chars"),
    ("hello world", "English text"),
    ("ádascxzcsaf qwer asdf zxcv", "Spam keyboard mashing"),
    ("123456789", "Numbers only"),
    ("!@#$%^&*()", "Special chars only"),
    ("hi", "Short word"),
    ("Sản phẩm này rất tốt", "Valid Vietnamese"),
    ("Tôi thích sản phẩm này lắm", "Valid Vietnamese long"),
    ("qwertyuiopasdfghjklzxcvbnm", "Keyboard pattern spam"),
]

print("Testing validate_input function:")
print("=" * 50)

for i, (text, description) in enumerate(test_cases, 1):
    is_valid, message = validate_input(text)
    status = "✅ PASS" if not is_valid else "❌ FAIL"
    print(f"Test {i}: {description}")
    print(f"  Input: '{text}'")
    print(f"  Result: {status} - {message}")
    print()