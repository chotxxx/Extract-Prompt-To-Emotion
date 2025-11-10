class RuleBasedSentiment:
    def __init__(self):
        # Vietnamese Sentiment Lexicon (VSL) - scores from -5 to 5
        self.sentiment_lexicon = {
            # Positive words
            "tốt": 4, "tot": 4, "ngon": 4, "hay": 3, "tuyệt": 5, "tuyet": 5, "tuyệt vời": 5, "tuyet voi": 5,
            "vui": 3, "hạnh phúc": 4, "hanh phuc": 4, "yêu": 4, "yeu": 4, "thích": 3, "thich": 3,
            "đẹp": 3, "dep": 3, "xinh": 3, "đáng yêu": 4, "dang yeu": 4, "thú vị": 4, "thu vi": 4,
            "hào hứng": 4, "hao hung": 4, "phấn khích": 4, "phan khich": 4, "kiên nhẫn": 3, "kien nhan": 3,
            "lạc quan": 3, "lac quan": 3, "tích cực": 4, "tich cuc": 4, "hài lòng": 3, "hai long": 3,
            "ưng ý": 3, "ung y": 3, "thoải mái": 3, "thoai mai": 3, "bình yên": 3, "binh yen": 3,
            "ổn định": 3, "on dinh": 3, "an toàn": 3, "an toan": 3, "tự hào": 4, "tu hao": 4,
            "hoàn hảo": 5, "hoan hao": 5, "xuất sắc": 5, "xuat sac": 5, "tinh tế": 3, "tinh te": 3,
            "tốt lành": 3, "tot lanh": 3,
            # Negative words
            "tệ": -4, "te": -4, "xấu": -3, "xau": -3, "ghét": -4, "ghet": -4, "buồn": -3, "buon": -3,
            "tức giận": -4, "tuc gian": -4, "giận": -4, "gian": -4, "khó chịu": -3, "kho chiu": -3,
            "thất vọng": -4, "that vong": -4, "lo lắng": -3, "lo lang": -3, "sợ hãi": -4, "so hai": -4,
            "đau khổ": -5, "dau kho": -5, "tuyệt vọng": -5, "tuyet vong": -5, "căng thẳng": -3, "cang thang": -3,
            "mệt mỏi": -3, "met moi": -3, "chán nản": -3, "chan nan": -3, "phiền muộn": -3, "phien muon": -3,
            "bực bội": -3, "buc boi": -3, "cáu kỉnh": -3, "cau kinh": -3, "tức tối": -4, "tuc toi": -4,
            "điên tiết": -5, "dien tiet": -5, "khinh bỉ": -4, "khinh bi": -4, "ghê tởm": -4, "ghe tom": -4,
            "kinh hoàng": -5, "kinh hoang": -5, "tồi tệ": -5, "toi te": -5, "đáng sợ": -4, "dang so": -4,
            "khủng khiếp": -5, "khung khiep": -5, "tiêu cực": -4, "tieu cuc": -4, "bất mãn": -3, "bat man": -3,
            "không hài lòng": -3, "khong hai long": -3,
            # Toxic/Profanity words (highly negative)
            "dcm": -5, "đcm": -5, "vl": -5, "vcl": -5, "cc": -5, "cl": -5, "địt": -5, "dit": -5,
            "chó": -4, "cho": -4, "mẹ": -4, "me": -4, "đồ ngu": -4, "do ngu": -4, "thằng ngu": -4, "thang ngu": -4,
            "con đĩ": -5, "con di": -5, "lồn": -5, "lon": -5, "cặc": -5, "cac": -5, "buồi": -5, "buoi": -5,
            "nguyền rủa": -5, "nguyen rua": -5, "chửi thề": -5, "chui the": -5, "toxic": -4,
            # Neutral or context-dependent - adjusted scores
            "bình thường": 0, "binh thuong": 0, "ổn": 0.5, "on": 0.5, "được": 0.5, "duoc": 0.5, "không": 0, "khong": 0,
            # Additional neutral words and phrases with lower positive scores
            "ổn thôi": 0.3, "on thoi": 0.3, "được đấy": 0.3, "duoc day": 0.3, "tương đối ổn": 0.3, "tuong doi on": 0.3,
            "cũng được": 0.3, "cung duoc": 0.3, "không tệ": 0.2, "khong te": 0.2, "tạm ổn": 0.2, "tam on": 0.2,
            "đáng tiền bối": 0.5, "dang tien boi": 0.5,  # Often sarcastic or mixed
            # Additional neutral words and phrases
            "có": 0, "co": 0, "là": 0, "la": 0, "đã": 0, "da": 0, "sẽ": 0, "se": 0, "đang": 0, "dang": 0,
            "tôi": 0, "toi": 0, "bạn": 0, "ban": 0, "chúng tôi": 0, "chung toi": 0, "họ": 0, "ho": 0,
            "sản phẩm": 0, "san pham": 0, "dịch vụ": 0, "dich vu": 0, "công ty": 0, "cong ty": 0,
            "cung cấp": 0, "cung cap": 0, "sử dụng": 0, "su dung": 0, "mua": 0, "mua": 0, "bán": 0, "ban": 0,
            "giá": 0, "gia": 0, "tiền": 0, "tien": 0, "hàng": 0, "hang": 0, "giao hàng": 0, "giao hang": 0,
            "nhanh": 0, "nhanh": 0, "chậm": 0, "cham": 0, "tốt": 0, "tot": 0, "xấu": 0, "xau": 0,  # Override with neutral context
            "chất lượng": 0, "chat luong": 0, "hỗ trợ": 0, "ho tro": 0, "khách hàng": 0, "khach hang": 0,
            "thông tin": 0, "thong tin": 0, "liên hệ": 0, "lien he": 0, "đặt hàng": 0, "dat hang": 0,
            "thanh toán": 0, "thanh toan": 0, "vận chuyển": 0, "van chuyen": 0, "bảo hành": 0, "bao hanh": 0,
            "hợp lý": 0, "hop ly": 0, "phù hợp": 0, "phu hop": 0, "đáp ứng": 0, "dap ung": 0,
            "cần": 0, "can": 0, "muốn": 0, "muon": 0, "có thể": 0, "co the": 0, "nên": 0, "nen": 0,
            "tại": 0, "tai": 0, "ở": 0, "o": 0, "từ": 0, "tu": 0, "đến": 0, "den": 0,
            "như": 0, "nhu": 0, "theo": 0, "theo": 0, "với": 0, "voi": 0, "cho": 0, "cho": 0,
            "và": 0, "va": 0, "hoặc": 0, "hoac": 0, "nhưng": 0, "nhung": 0, "mặc dù": 0, "mac du": 0,
            "tuy nhiên": 0, "tuy nhien": 0, "vì": 0, "vi": 0, "nếu": 0, "neu": 0, "khi": 0, "khi": 0,
            "thì": 0, "thi": 0, "sau": 0, "sau": 0, "trước": 0, "truoc": 0, "giữa": 0, "giua": 0,
            "trên": 0, "tren": 0, "dưới": 0, "duoi": 0, "bên": 0, "ben": 0, "ngoài": 0, "ngoai": 0,
            "bên trong": 0, "ben trong": 0, "gần": 0, "gan": 0, "xa": 0, "xa": 0, "lớn": 0, "lon": 0,
            "nhỏ": 0, "nho": 0, "mới": 0, "moi": 0, "cũ": 0, "cu": 0, "đầy": 0, "day": 0, "trống": 0, "trong": 0,
            "màu": 0, "mau": 0, "kích thước": 0, "kich thuoc": 0, "trọng lượng": 0, "trong luong": 0,
            "số lượng": 0, "so luong": 0, "thời gian": 0, "thoi gian": 0, "ngày": 0, "ngay": 0, "tháng": 0, "thang": 0,
            "năm": 0, "nam": 0, "giờ": 0, "gio": 0, "phút": 0, "phut": 0, "giây": 0, "giay": 0,
        }

        # Negation words
        self.negations = {"không", "chẳng", "chưa", "đừng", "khỏi"}

        # Intensifiers/Diminishers
        self.intensifiers = {"rất": 1.5, "cực kỳ": 2.0, "quá": 1.2, "hơi": 0.5, "khá": 1.2}

        # Neutral indicators - expanded
        self.neutral_indicators = {"?", "có", "là", "đã", "sẽ", "có thể", "nên", "tại", "ở", "từ", "đến", "như", "theo", "với", "cho",
                                  "hoặc", "hoac", "hay", "tùy", "tuy", "có lẽ", "co le", "có thể", "co the", "tôi nghĩ", "toi nghi",
                                  "bạn nghĩ", "ban nghi", "tôi tự hỏi", "toi tu hoi", "tôi không biết", "toi khong biet",
                                  "trung lập", "trung lap", "bình thường", "binh thuong", "ổn thôi", "on thoi", "tương đối", "tuong doi",
                                  "cũng được", "cung duoc", "không tệ", "khong te", "không tốt", "khong tot", "có lẫn không", "co lan khong",
                                  "tích cực và", "tieu cuc va", "tốt nhưng", "tot nhung", "tuyệt vời nhưng", "tuyet voi nhung"}

    def is_neutral_context(self, text):
        """Check if text has neutral context indicators"""
        text_lower = text.lower()
        words = text_lower.split()

        # Count neutral indicators
        neutral_count = sum(1 for word in words if word in self.neutral_indicators)

        # Check for question marks
        question_mark = "?" in text

        # Check for mixed sentiments (positive AND negative words/phrases)
        has_positive = False
        has_negative = False

        # Check phrases first (longer matches)
        for length in range(min(3, len(words)), 0, -1):
            for i in range(len(words) - length + 1):
                phrase = ' '.join(words[i:i+length])
                if phrase in self.sentiment_lexicon:
                    score = self.sentiment_lexicon[phrase]
                    if score > 0:
                        has_positive = True
                    elif score < 0:
                        has_negative = True

        # Also check single words
        for word in words:
            if word in self.sentiment_lexicon:
                score = self.sentiment_lexicon[word]
                if score > 0:
                    has_positive = True
                elif score < 0:
                    has_negative = True

        mixed_sentiment = has_positive and has_negative

        # Check for contrastive words
        contrastives = ["nhưng", "tuy nhiên", "mặc dù", "hoặc", "hay", "tuy", "dù"]
        has_contrastive = any(contrastive in text_lower for contrastive in contrastives)

        # Consider neutral if: many neutral words, question, mixed sentiment, contrastive, or long factual text
        return (neutral_count >= 2 or question_mark or mixed_sentiment or has_contrastive or
                len(words) > 12)  # Long descriptions often factual

    def analyze_sentiment(self, text):
        """Compute rule-based sentiment score S_Rule with improved negation handling"""
        words = text.lower().split()
        score = 0.0
        i = 0
        negation_scope = 0  # How many words negation affects
        while i < len(words):
            multiplier = 1.0

            # Check for intensifier
            if words[i] in self.intensifiers and i + 1 < len(words):
                multiplier *= self.intensifiers[words[i]]
                i += 1

            # Find the longest matching phrase starting from i
            phrase_score = None
            phrase_length = 0
            for length in range(min(3, len(words) - i), 0, -1):  # from longest to shortest
                phrase = ' '.join(words[i:i+length])
                if phrase in self.sentiment_lexicon:
                    phrase_score = self.sentiment_lexicon[phrase]
                    phrase_length = length
                    break

            if phrase_score is not None:
                # Apply negation if in scope
                negate = negation_scope > 0
                if negate:
                    phrase_score = -phrase_score
                    negation_scope -= phrase_length  # reduce scope by phrase length
                else:
                    negation_scope = max(0, negation_scope - phrase_length)

                score += phrase_score * multiplier
                i += phrase_length
            else:
                # Check for negation
                if words[i] in self.negations:
                    negation_scope = 3  # Affect next 3 words
                i += 1

        # Adjust for neutral context - more aggressive reduction
        if self.is_neutral_context(text):
            if abs(score) <= 2:
                score *= 0.1  # Nearly zero for low scores
            elif abs(score) <= 4:
                score *= 0.3  # Strong reduction for medium scores
            else:
                score *= 0.5  # Moderate reduction for high scores

        return score

    def get_label(self, score):
        """Convert score to label"""
        if score > 0:
            return "POSITIVE"
        elif score < 0:
            return "NEGATIVE"
        else:
            return "NEUTRAL"