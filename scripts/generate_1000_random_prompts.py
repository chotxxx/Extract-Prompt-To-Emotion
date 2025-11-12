import random

# Positive phrases
positive_phrases = [
    "tôi rất vui", "sản phẩm tốt", "dịch vụ tuyệt vời", "phim hay lắm", "món ăn ngon", "công việc ổn định",
    "thời tiết đẹp", "bạn bè thân thiện", "giáo viên tận tâm", "sách hay", "âm nhạc du dương",
    "trò chơi thú vị", "du lịch tuyệt vời", "sức khỏe tốt", "gia đình hạnh phúc", "công nghệ tiên tiến",
    "thiết kế đẹp", "chất lượng cao", "giá cả hợp lý", "hỗ trợ khách hàng tốt", "giao hàng nhanh",
    "ứng dụng dễ sử dụng", "trải nghiệm tuyệt vời", "nhân viên thân thiện", "môi trường làm việc tốt",
    "cơ hội phát triển", "đào tạo chuyên nghiệp", "lương thưởng hấp dẫn", "phúc lợi tốt", "văn hóa doanh nghiệp tích cực",
    "sản phẩm sáng tạo", "dịch vụ chuyên nghiệp", "hài lòng với sản phẩm", "tích cực", "lạc quan",
    "hạnh phúc", "vui vẻ", "thoải mái", "bình yên", "ổn định", "an toàn", "tự hào", "hoàn hảo",
    "xuất sắc", "tinh tế", "tốt lành", "đáng yêu", "thú vị", "hào hứng", "phấn khích", "kiên nhẫn",
    "lạc quan", "tích cực", "hài lòng", "ưng ý", "thoải mái", "bình yên", "ổn định", "an toàn",
    "tự hào", "hoàn hảo", "xuất sắc", "tinh tế", "tốt lành"
]

# Negative phrases
negative_phrases = [
    "tôi rất buồn", "sản phẩm tệ", "dịch vụ kém", "phim dở", "món ăn khó ăn", "công việc khó khăn",
    "thời tiết xấu", "bạn bè xa cách", "giáo viên nghiêm khắc", "sách nhàm chán", "âm nhạc khó nghe",
    "trò chơi nhàm", "du lịch thất vọng", "sức khỏe kém", "gia đình bất hòa", "công nghệ lỗi thời",
    "thiết kế xấu", "chất lượng thấp", "giá cả cao", "hỗ trợ khách hàng kém", "giao hàng chậm",
    "ứng dụng khó sử dụng", "trải nghiệm tệ", "nhân viên thô lỗ", "môi trường làm việc xấu",
    "cơ hội phát triển ít", "đào tạo kém", "lương thưởng thấp", "phúc lợi kém", "văn hóa doanh nghiệp tiêu cực",
    "sản phẩm lỗi", "dịch vụ nghiệp dư", "không hài lòng", "tiêu cực", "bi quan",
    "buồn bã", "khó chịu", "căng thẳng", "lo lắng", "bất ổn", "nguy hiểm", "thất vọng", "tồi tệ",
    "đáng sợ", "khủng khiếp", "tiêu cực", "bất mãn", "không hài lòng", "mệt mỏi", "chán nản",
    "phiền muộn", "bực bội", "cáu kỉnh", "tức tối", "điên tiết", "khinh bỉ", "ghê tởm", "kinh hoàng",
    "tồi tệ", "đáng sợ", "khủng khiếp", "tiêu cực", "bất mãn"
]

# Neutral phrases
neutral_phrases = [
    "thời tiết bình thường", "công việc ổn", "sản phẩm bình thường", "dịch vụ ổn", "phim trung bình",
    "món ăn tạm", "bạn bè bình thường", "giáo viên bình thường", "sách bình thường", "âm nhạc bình thường",
    "trò chơi bình thường", "du lịch bình thường", "sức khỏe bình thường", "gia đình bình thường",
    "công nghệ bình thường", "thiết kế bình thường", "chất lượng bình thường", "giá cả bình thường",
    "hỗ trợ khách hàng bình thường", "giao hàng bình thường", "ứng dụng bình thường", "trải nghiệm bình thường",
    "nhân viên bình thường", "môi trường làm việc bình thường", "cơ hội phát triển bình thường",
    "đào tạo bình thường", "lương thưởng bình thường", "phúc lợi bình thường", "văn hóa doanh nghiệp bình thường",
    "sản phẩm bình thường", "dịch vụ bình thường", "bình thường", "ổn thôi", "cũng được", "tương đối ổn",
    "cũng tạm", "không tệ", "không tốt", "trung lập", "được đấy", "cũng được", "cũng tạm", "tương đối ổn",
    "cũng tạm", "không tệ", "không tốt", "trung lập", "được đấy", "cũng được", "cũng tạm", "tương đối ổn",
    "cũng tạm", "không tệ", "không tốt", "trung lập", "được đấy"
]

def generate_random_prompts(num_prompts=1000):
    prompts = []
    sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    weights = [0.35, 0.35, 0.30]  # Slightly more positive/negative for balance

    for _ in range(num_prompts):
        sentiment = random.choices(sentiments, weights=weights)[0]

        if sentiment == "POSITIVE":
            phrase = random.choice(positive_phrases)
        elif sentiment == "NEGATIVE":
            phrase = random.choice(negative_phrases)
        else:
            phrase = random.choice(neutral_phrases)

        # Add some variation with prefixes/suffixes
        prefixes = ["", "Hôm nay ", "Tôi nghĩ ", "Theo tôi ", "Có lẽ ", "Nhìn chung "]
        suffixes = ["", " quá", " lắm", " thôi", " đấy", " mà"]

        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)

        prompt = f"{prefix}{phrase}{suffix}".strip()

        prompts.append((prompt, sentiment))

    return prompts

def save_prompts_to_file(prompts, filename="test_1000_random_prompts.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for prompt, sentiment in prompts:
            f.write(f"{prompt}\t{sentiment}\n")
    print(f"Saved {len(prompts)} prompts to {filename}")

if __name__ == "__main__":
    prompts = generate_random_prompts(1000)
    save_prompts_to_file(prompts)