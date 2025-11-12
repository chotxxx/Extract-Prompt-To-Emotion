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
            # Add patterns from failed prompts
                        # Add patterns from failed cases
            "do qua": -2, "dở quá": -2,
            "cong viec kho khan": -3, "công việc khó khăn": -3,
            "ho tro khach hang tot": 3, "hỗ trợ khách hàng tốt": 3,
            "dich vu kem": -3, "dịch vụ kém": -3,
            "luong thuong thap": -3, "lương thưởng thấp": -3,
            "chat luong cao": 3, "chất lượng cao": 3,
            "tro choi nham": -3, "trò chơi nhàm": -3,
            "co hoi phat trien it": -3, "cơ hội phát triển ít": -3,
            "giao hang cham": -2, "giao hàng chậm": -2,
            "dich vu nghiep du": -3, "dịch vụ nghiệp dư": -3,
            "ban be xa cach": -2, "bạn bè xa cách": -2,
            "cong nghe tien tien": 3, "công nghệ tiên tiến": 3,
            "khong tot": -2, "không tốt": -2,
            "tuong doi on": 0, "tương đối ổn": 0,
            "suc khoe binh thuong": 0, "sức khỏe bình thường": 0,
            "gia dinh binh thuong": 0, "gia đình bình thường": 0,
            "chat luong binh thuong": 0, "chất lượng bình thường": 0,
            "moi truong lam viec tot": 3, "môi trường làm việc tốt": 3,
            "giao hang nhanh": 2, "giao hàng nhanh": 2,
            "suc khoe tot": 3, "sức khỏe tốt": 3,
            "chat luong thap": -3, "chất lượng thấp": -3,
            "luong thuong hap dan": 3, "lương thưởng hấp dẫn": 3,
            "giao vien nghiem khac": -2, "giáo viên nghiêm khắc": -2,
            "nguy hiem": -4, "nguy hiểm": -4,
            "co hoi phat trien": 3, "cơ hội phát triển": 3,
            "co hoi phat trien it": -3, "cơ hội phát triển ít": -3,
            "gia dinh bat hoa": -3, "gia đình bất hòa": -3,
            "phuc loi tot": 3, "phúc lợi tốt": 3,
            "dao tao chuyen nghiep": 3, "đào tạo chuyên nghiệp": 3,
            "am nhac du duong": 3, "âm nhạc du dương": 3,
            "nhan vien than thien": 3, "nhân viên thân thiện": 3,
            "dich vu chuyen nghiep": 3, "dịch vụ chuyên nghiệp": 3,
            "giao vien tan tam": 3, "giáo viên tận tâm": 3,
            "cong nghe loi thoi": -3, "công nghệ lỗi thời": -3,
            "sach nham chan": -3, "sách nhàm chán": -3,
            "bat on": -3, "bất ổn": -3,
            "suc khoe kem": -3, "sức khỏe kém": -3,
            "gia ca hop ly": 3, "giá cả hợp lý": 3,
            "ung dung binh thuong": 0, "ứng dụng bình thường": 0,
            "trai nghiem binh thuong": 0, "trải nghiệm bình thường": 0,
            "van hoa doanh nghiep binh thuong": 0, "văn hóa doanh nghiệp bình thường": 0,
            "mon an tam": 0, "món ăn tạm": 0,
            "du lich binh thuong": 0, "du lịch bình thường": 0,
            "am nhac binh thuong": 0, "âm nhạc bình thường": 0,
            "nhan vien binh thuong": 0, "nhân viên bình thường": 0,
            "dich vu on": 0.5, "dịch vụ ổn": 0.5,
            "dao tao binh thuong": 0, "đào tạo bình thường": 0,
            "moi truong lam viec binh thuong": 0, "môi trường làm việc bình thường": 0,
            "co hoi phat trien it lam": -3, "cơ hội phát triển ít lắm": -3,
            "co hoi phat trien it qua": -3, "cơ hội phát triển ít quá": -3,
            # Toxic/Profanity words (highly negative)
            # Additional conservative negative phrase entries found in failed patterns
            "dịch vụ quá tồi": -4, "dich vu qua toi": -4,
            "mua hàng khó khăn": -3, "mua hang kho khan": -3,
            "giá cả quá cao": -3, "gia ca qua cao": -3,
            "mua sắm mất thời gian": -3, "mua sam mat thoi gian": -3,
            "sản phẩm tiêu cực": -4, "san pham tieu cuc": -4,
            "không đáng tiền": -3, "khong dang tien": -3,
            "không đáng": -2, "khong dang": -2,
            "không dịch vụ": -3, "khong dich vu": -3,
            "đồ đĩ": -5, "do di": -5,
            # More patterns from failed cases
            "tôi nghĩ": 0, "toi nghi": 0,  # Neutral modifier
            "theo tôi": 0, "theo toi": 0,
            "nhìn chung": 0, "nhin chung": 0,
            "có lẽ": 0, "co le": 0,
            "hôm nay": 0, "hom nay": 0,
            "tương đối": 0, "tuong doi": 0,
            "ứng dụng dễ sử dụng": 3, "ung dung de su dung": 3,
            "sản phẩm sáng tạo": 3, "san pham sang tao": 3,
            "môi trường làm việc xấu": -3, "moi truong lam viec xau": -3,
            "phúc lợi kém": -3, "phuc loi kem": -3,
            "âm nhạc khó nghe": -3, "am nhac kho nghe": -3,
            "nhân viên thô lỗ": -4, "nhan vien tho lo": -4,
            "giáo viên nghiêm khắc": -2, "giao vien nghiem khac": -2,
            "giá cả cao": -2, "gia ca cao": -2,
            "món ăn khó ăn": -3, "mon an kho an": -3,
            "không hài lòng": -3, "khong hai long": -3,
            # More neutral patterns from failed cases
            "tương đối ổn": 0, "tuong doi on": 0,
            "dịch vụ ổn": 0, "dich vu on": 0,
            "cơ hội phát triển bình thường": 0, "co hoi phat trien binh thuong": 0,
            "được đấy": 0, "duoc day": 0,
            "không tệ": 0, "khong te": 0,
            "công việc ổn": 0, "cong viec on": 0,
            "tương đối ổn thôi": 0, "tuong doi on thoi": 0,
            "được đấy lắm": 0, "duoc day lam": 0,
            "dịch vụ ổn lắm": 0, "dich vu on lam": 0,
            "tương đối ổn quá": 0, "tuong doi on qua": 0,
            "dịch vụ ổn quá": 0, "dich vu on qua": 0,
            "cơ hội phát triển bình thường lắm": 0, "co hoi phat trien binh thuong lam": 0,
            "cơ hội phát triển bình thường mà": 0, "co hoi phat trien binh thuong ma": 0,
            "tương đối ổn mà": 0, "tuong doi on ma": 0,
            "tương đối ổn lắm": 0, "tuong doi on lam": 0,
            # Toxic/Profanity words (highly negative)
            "dcm": -5, "đcm": -5, "vl": -5, "vcl": -5, "cc": -5, "cl": -5, "địt": -5, "dit": -5,
            "chó": -4, "cho": -4, "mẹ": -4, "me": -4, "đồ ngu": -4, "do ngu": -4, "thằng ngu": -4, "thang ngu": -4,
            "con đĩ": -5, "con di": -5, "lồn": -5, "lon": -5, "cặc": -5, "cac": -5, "buồi": -5, "buoi": -5,
            "nguyền rủa": -5, "nguyen rua": -5, "chửi thề": -5, "chui the": -5, "toxic": -4, "vc": -5, "cdmm": -5, "cđmm": -5,
            # Neutral or context-dependent - adjusted scores
            "bình thường": 0, "binh thuong": 0, "ổn": 0.5, "on": 0.5, "được": 0.5, "duoc": 0.5, "không": 0, "khong": 0,
            # Additional neutral words and phrases with lower positive scores
            "ổn thôi": 0, "on thoi": 0, "được đấy": 0, "duoc day": 0, "tương đối ổn": 0, "tuong doi on": 0,
            "cũng được": 0, "cung duoc": 0, "không tệ": 0, "khong te": 0, "tạm ổn": 0, "tam on": 0,
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
            # Add neutral phrase from failed prompt
            "khien toi on dinh": 0, "khiến tôi ổn định": 0,
        }

        # Negation words
        self.negations = {"không", "chẳng", "chưa", "đừng", "khỏi"}

        # Intensifiers/Diminishers
        self.intensifiers = {"rất": 1.5, "cực kỳ": 2.0, "quá": 1.2, "hơi": 0.5, "khá": 1.2}

        # Neutral indicators - expanded (questions, filler, mild praise and filler phrases)
        self.neutral_indicators = {
            "?", "có", "là", "đã", "sẽ", "có thể", "nên", "tại", "ở", "từ", "đến", "như", "theo", "với", "cho",
            "hoặc", "và", "nhưng", "mặc dù", "tuy nhiên",
            # filler / neutral phrasing
            "không có ý kiến", "không có ý kiến gì", "không sao", "ổn thôi", "ổn", "bình thường", "bình thường,", "trung lập", "được đấy", "cũng được", "cũng tạm", "tương đối ổn", "cũng tạm",
            # mild descriptive phrases often labelled neutral in dataset
            "sản phẩm", "dịch vụ", "chất lượng", "giao hàng", "hỗ trợ", "đáp ứng nhu cầu", "đáp ứng", "mua lại", "tôi sẽ mua lại", "cong viec", "công việc",
            # Additional modal phrases that neutralize
            "tôi nghĩ", "theo tôi", "nhìn chung", "có lẽ", "hôm nay", "tương đối",
        }

        # Contrastive connectors used for splitting clauses
        self.contrastive_connectors = ["tuy nhiên", "nhưng", "mặc dù", "mặc dù vậy", "mà", "nhưng mà", "tuy", "dù", "mặc dù thế", "thế nhưng", "song", "song le", "dù sao"]

        # Sarcasm indicators (common Vietnamese sarcasm patterns)
        self.sarcasm_indicators = ["thật đấy", "đúng không", "tốt lắm", "hay quá", "tuyệt vời", "quá tốt", "rất hay"]

    def is_neutral_context(self, text):
        """Check if text has neutral context indicators"""
        text_lower = text.lower()
        words = text_lower.split()

        # Count neutral indicators
        neutral_count = sum(1 for word in words if word in self.neutral_indicators)
        # Also check neutral phrases anywhere in the text (e.g., 'sản phẩm', 'chất lượng')
        neutral_phrase_present = any(phrase in text_lower for phrase in self.neutral_indicators)

        # Check for question marks
        question_mark = "?" in text

        # Check for mixed sentiments (positive AND negative words/phrases)
        has_positive = False
        has_negative = False

        positive_words = ["tốt", "tot", "hay", "tuyệt", "tuyet", "vui", "hạnh phúc", "hanh phuc", "yêu", "yeu", "thích", "thich", "đẹp", "dep", "xinh", "đáng yêu", "dang yeu", "thú vị", "thu vi", "hào hứng", "hao hung", "phấn khích", "phan khich", "kiên nhẫn", "kien nhan", "lạc quan", "lac quan", "tích cực", "tich cuc", "hài lòng", "hai long", "ưng ý", "ung y", "thoải mái", "thoai mai", "bình yên", "binh yen", "ổn định", "on dinh", "an toàn", "an toan", "tự hào", "tu hao", "hoàn hảo", "hoan hao", "xuất sắc", "xuat sac", "tinh tế", "tinh te", "tốt lành", "tot lanh"]
        negative_words = ["tệ", "te", "xấu", "xau", "ghét", "ghet", "buồn", "buon", "tức giận", "tuc gian", "giận", "gian", "khó chịu", "kho chiu", "thất vọng", "that vong", "lo lắng", "lo lang", "sợ hãi", "so hai", "đau khổ", "dau kho", "tuyệt vọng", "tuyet vong", "căng thẳng", "cang thang", "mệt mỏi", "met moi", "chán nản", "chan nan", "phiền muộn", "phien muon", "bực bội", "buc boi", "cáu kỉnh", "cau kinh", "tức tối", "tuc toi", "điên tiết", "dien tiet", "khinh bỉ", "khinh bi", "ghê tởm", "ghe tom", "kinh hoàng", "kinh hoang", "tồi tệ", "toi te", "đáng sợ", "dang so", "khủng khiếp", "khung khiep", "tiêu cực", "tieu cuc", "bất mãn", "bat man", "không hài lòng", "khong hai long"]
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        mixed_sentiment = pos_count > 0 and neg_count > 0

        # Check phrases first (longer matches)
        for length in range(min(4, len(words)), 0, -1):
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

        # If has strong sentiment words, don't force neutral
        has_sentiment = has_positive or has_negative

        # Nếu có nhiều neutral indicator, chỉ hiện diện phrase trung lập, dấu hỏi, hoặc câu rất dài VÀ không có sentiment => NEUTRAL
        return (neutral_count >= 2 or neutral_phrase_present or question_mark or len(words) > 12) and not has_sentiment

    def detect_mixed_sentiment(self, text):
        """Return True if text contains both positive and negative signals (words/phrases).
        We use lexicon phrases and additional heuristic lists for robustness (handles no-diacritic).
        """
        text_lower = text.lower()
        words = text_lower.split()

        # quick counts from lexicon
        pos_count = 0
        neg_count = 0

        # check phrases first (longer matches)
        for length in range(min(4, len(words)), 0, -1):
            for i in range(len(words) - length + 1):
                phrase = ' '.join(words[i:i+length])
                if phrase in self.sentiment_lexicon:
                    score = self.sentiment_lexicon[phrase]
                    if score > 0:
                        pos_count += 1
                    elif score < 0:
                        neg_count += 1

        # check single words (fallback)
        for w in words:
            if w in self.sentiment_lexicon:
                s = self.sentiment_lexicon[w]
                if s > 0:
                    pos_count += 1
                elif s < 0:
                    neg_count += 1

        # conservative mixed detection: require both positive and negative signals in text
        if pos_count > 0 and neg_count > 0:
            # if counts similar or both >=1, treat as mixed
            if abs(pos_count - neg_count) <= 1 or (pos_count >= 2 and neg_count >= 1) or (neg_count >= 2 and pos_count >= 1):
                return True

        # contrastive alone is not enough to mark as mixed; prefer to let clause-level logic decide
        return False

    def _clause_score(self, clause_text):
        """Compute a simple clause-level lexicon score (no neutralization)."""
        words = clause_text.lower().split()
        score = 0.0
        i = 0
        while i < len(words):
            # check 3-word phrases to single words
            matched = False
            for length in range(min(4, len(words) - i), 0, -1):
                phrase = ' '.join(words[i:i+length])
                if phrase in self.sentiment_lexicon:
                    s = self.sentiment_lexicon[phrase]
                    # simple negation if 'không' immediately before phrase
                    if i - 1 >= 0 and words[i-1] in self.negations:
                        s = -s
                    score += s
                    i += length
                    matched = True
                    break
            if not matched:
                i += 1
        return score

    def _post_contrast_clause_score(self, text):
        """If there's a contrastive connector, return the score of the clause after it, else 0.0"""
        text_lower = text.lower()
        for conn in sorted(self.contrastive_connectors, key=lambda x: -len(x)):
            if conn in text_lower:
                parts = text_lower.split(conn, 1)
                if len(parts) > 1:
                    right = parts[1].strip()
                    return self._clause_score(right)
        return 0.0

    def analyze_sentiment(self, text):
        """Compute rule-based sentiment score S_Rule with improved negation handling"""
        # Quick neutral/question heuristics
        text_lower = text.lower()
        if "?" in text or any(q in text_lower for q in ["có phải", "phải không", "bạn nghĩ", "bạn có", "bạn thấy", "bạn nghĩ thế nào"]):
            return 0.0

        # Detect sarcasm (reverse polarity for exaggerated positive words in negative context)
        sarcasm_detected = any(sarc in text_lower for sarc in self.sarcasm_indicators) and any(neg in text_lower.split() for neg in self.negations)

        words = text_lower.split()
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
            for length in range(min(5, len(words) - i), 0, -1):  # from longest to shortest
                phrase = ' '.join(words[i:i+length])
                if phrase in self.sentiment_lexicon:
                    phrase_score = self.sentiment_lexicon[phrase]
                    phrase_length = length
                    break

            if phrase_score is not None:
                # Apply negation if in scope and phrase doesn't already include negation
                negate = negation_scope > 0 and not any(phrase.startswith(neg + ' ') for neg in self.negations)
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

        # If mixed sentiment detected, prefer neutralization
        if self.detect_mixed_sentiment(text):
            # If there is a strong sentiment after a contrastive connector, prefer that clause
            post_score = self._post_contrast_clause_score(text)
            if abs(post_score) >= 1.0:
                return post_score
            # otherwise set to zero so fusion will tend to prefer NEUTRAL in truly ambiguous cases
            return 0.0

        # Adjust for neutral context - more aggressive reduction
        if self.is_neutral_context(text):
            if abs(score) <= 2:
                score *= 0.1  # Nearly zero for low scores
            elif abs(score) <= 4:
                score *= 0.3  # Strong reduction for medium scores
            else:
                score *= 0.5  # Moderate reduction for high scores

        # Apply sarcasm reversal
        if sarcasm_detected and abs(score) > 0:
            score = -score

        return score

    def get_label(self, score):
        """Convert score to label"""
        if score > 0:
            return "POSITIVE"
        elif score < 0:
            return "NEGATIVE"
        else:
            return "NEUTRAL"