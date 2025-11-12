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

    # Calculate meaningful characters ratio
    total_chars = len(text)
    meaningful_chars = sum(1 for char in text if char.isalnum() or char in 'àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ .,;!?' )
    meaningful_ratio = meaningful_chars / total_chars

    if meaningful_ratio < 0.3:  # Less than 30% meaningful characters
        return False, "❌ Văn bản có quá nhiều ký tự đặc biệt! Vui lòng nhập văn bản có nghĩa."

    # Check for keyboard mashing (repeated characters)
    if re.search(r'(.)\1{4,}', text):  # 5+ repeated characters
        return False, "❌ Phát hiện ký tự lặp lại! Vui lòng nhập văn bản có nghĩa."

    # Check for excessive consecutive consonants (likely spam)
    consonants = 'bcdfghjklmnpqrstvwxyzđ'
    matches = re.findall(f'[{consonants}]+', text.lower())
    max_consonant_streak = max(len(match) for match in matches) if matches else 0
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

    # Check for Vietnamese content (support both accented and unaccented Vietnamese)
    def is_vietnamese_text(text):
        """Check if text contains Vietnamese words (accented or unaccented)"""
        # Common Vietnamese words (both accented and unaccented forms)
        vietnamese_words = {
            # Basic words
            'va', 'ma', 'la', 'duoc', 'khong', 'co', 'nguoi', 'di', 'den', 'tu',
            'trong', 'tren', 'duoi', 'sang', 'phai', 'trai', 'len', 'xuong',
            'nhu', 'neu', 'thi', 'hay', 'hoac', 'luc', 'khi', 'sau', 'truoc',
            # Common verbs
            'lam', 'an', 'uong', 'di', 'den', 've', 'noi', 'nghe', 'thay', 'biet',
            'muon', 'can', 'nen', 'phai', 'duoc', 'co', 'la', 'duoc', 'khong',
            # Common adjectives
            'tot', 'xau', 'dep', 'hai', 'vui', 'buon', 'lon', 'nho', 'cao', 'thap',
            'nhanh', 'cham', 'dung', 'sai', 'dung', 'sach', 'rong', 'hep',
            # Common nouns
            'nha', 'truong', 'cong', 'xe', 'duong', 'thanh pho', 'que huong',
            'nguoi', 'con', 'me', 'bo', 'anh', 'chi', 'em', 'ban', 'co',
            'san pham', 'hang', 'tien', 'gia', 'mua', 'ban', 'lam viec',
            # Question words
            'gi', 'ai', 'o dau', 'sao', 'tai sao', 'khi nao', 'bao nhieu',
            # With accents (common ones)
            'và', 'mà', 'là', 'được', 'không', 'có', 'người', 'đi', 'đến', 'từ',
            'trong', 'trên', 'dưới', 'sang', 'phải', 'trái', 'lên', 'xuống',
            'như', 'nếu', 'thì', 'hay', 'hoặc', 'lúc', 'khi', 'sau', 'trước',
            # Additional common words
            'rat', 'rat', 'rất', 'cũng', 'cung', 'thì', 'thi', 'đây', 'day',
            'đó', 'do', 'này', 'nay', 'kia', 'no', 'nó', 'ta', 'tao', 'mình',
            'tôi', 'toi', 'ban', 'bạn', 'anh', 'chị', 'chi', 'em', 'ông', 'ba',
            'họ', 'ho', 'chúng tôi', 'chung toi', 'chúng ta', 'chung ta'
        }

        text_lower = text.lower()
        words = text_lower.split()

        # Count Vietnamese words
        vietnamese_word_count = 0
        total_words = len(words)

        for word in words:
            # Remove punctuation for checking
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word in vietnamese_words:
                vietnamese_word_count += 1

        # Consider Vietnamese if >20% words are Vietnamese (lowered threshold)
        if total_words > 0:
            vietnamese_ratio = vietnamese_word_count / total_words
            return vietnamese_ratio >= 0.2  # Lowered threshold

        return False

    # Check for Vietnamese content
    if not is_vietnamese_text(text) and len(text) > 10:
        # Return as valid but surface a non-blocking warning so callers can
        # proceed with classification while informing the user the text may
        # not be Vietnamese or may be missing diacritics.
        return True, "⚠️ Không chắc chắn đây là tiếng Việt — kết quả có thể không chính xác. Nếu văn bản là tiếng Việt không dấu, bạn có thể tiếp tục."

    return True, "✅ Văn bản hợp lệ!"