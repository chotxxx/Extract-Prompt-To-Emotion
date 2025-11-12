import streamlit as st
import pandas as pd
import json
import csv
from io import StringIO, BytesIO
from datetime import datetime
from preprocessing import VietnamesePreprocessor
from phobert_module import PhoBERTModule
from rule_based import RuleBasedSentiment
from fusion import ConditionalFusion
from db_connector import DBConnector

# Input validation functions
def validate_input(text):
    """
    Validate input text for Vietnamese sentiment analysis.
    Returns (is_valid, error_message)
    """
    import re
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
        return False, "⚠️ Không phát hiện nội dung tiếng Việt. Vui lòng nhập văn bản bằng tiếng Việt."

    return True, "✅ Văn bản hợp lệ!"

# Export functions
def export_to_csv(df):
    """Export dataframe to CSV"""
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    return csv_buffer.getvalue()

def export_to_json(df):
    """Export dataframe to JSON"""
    # Convert timestamp to string for JSON serialization
    df_copy = df.copy()
    df_copy['Timestamp'] = df_copy['Timestamp'].astype(str)
    return json.dumps(df_copy.to_dict('records'), ensure_ascii=False, indent=2)

def export_to_html(df):
    """Export dataframe to HTML (for PDF-like display)"""
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Lịch sử Phân loại Cảm xúc</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #1f77b4; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Lịch sử Phân loại Cảm xúc</h1>
        <p>Xuất ngày: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        {df.to_html(index=False, classes='table table-striped')}
    </body>
    </html>
    """
    return html

def export_to_ics(df):
    """Export dataframe to ICS format (simplified calendar format)"""
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Sentiment Analysis//History//EN\n"
    
    for _, row in df.iterrows():
        ics_content += "BEGIN:VEVENT\n"
        ics_content += f"SUMMARY:Phân loại - {row['Label']}\n"
        ics_content += f"DESCRIPTION:{row['Input'][:100]}...\n"
        # Convert timestamp to ICS format
        if isinstance(row['Timestamp'], str):
            dt = datetime.fromisoformat(row['Timestamp'].replace('Z', '+00:00'))
        else:
            dt = row['Timestamp']
        ics_content += f"DTSTART:{dt.strftime('%Y%m%dT%H%M%S')}\n"
        ics_content += f"DTEND:{(dt.replace(second=dt.second+1)).strftime('%Y%m%dT%H%M%S')}\n"
        ics_content += "END:VEVENT\n"
    
    ics_content += "END:VCALENDAR\n"
    return ics_content

def import_from_csv(uploaded_file):
    """Import data from CSV file"""
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        return df, None
    except Exception as e:
        return None, str(e)

def import_from_json(uploaded_file):
    """Import data from JSON file"""
    try:
        data = json.load(uploaded_file)
        df = pd.DataFrame(data)
        return df, None
    except Exception as e:
        return None, str(e)

# Cache resources
@st.cache_resource
def load_models():
    preprocessor = VietnamesePreprocessor()
    phobert = PhoBERTModule()
    rule_based = RuleBasedSentiment()
    fusion = ConditionalFusion()
    return preprocessor, phobert, rule_based, fusion

preprocessor, phobert, rule_based, fusion = load_models()
db = DBConnector()

st.title("Phân loại cảm xúc tiếng Việt")

tab1, tab2 = st.tabs(["Phân loại Cảm xúc", "Lịch sử Phân loại"])

with tab1:
    st.header("Phân loại Cảm xúc")
    text_input = st.text_area("Nhập câu tiếng Việt:", height=100)
    
    # Confidence threshold slider
    confidence_threshold = st.slider(
        "Ngưỡng độ tin cậy cho kết quả mơ hồ:",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Nếu độ tin cậy dưới ngưỡng này, hệ thống sẽ cảnh báo kết quả có thể mơ hồ."
    )

    if st.button("Phân loại"):
        if text_input.strip():
            # Validate input first
            is_valid, error_msg = validate_input(text_input)
            if not is_valid:
                st.error(error_msg)
            else:
                with st.spinner("Đang xử lý..."):
                    # Preprocess
                    processed_text = preprocessor.preprocess(text_input)

                    # PhoBERT
                    l_phobert, c_phobert = phobert.analyze_sentiment(processed_text)

                    # Rule-based
                    s_rule = rule_based.analyze_sentiment(processed_text)

                    # Fusion
                    final_label, final_conf = fusion.fuse(l_phobert, c_phobert, s_rule)

                    # Display results
                    if final_conf < confidence_threshold:
                        st.warning(f"⚠️ Cảm xúc: {final_label} (Có thể mơ hồ - Độ tin cậy thấp)")
                        st.info("💡 Gợi ý: Kết quả này có độ tin cậy thấp. Hãy xem xét ngữ cảnh hoặc nhập thêm chi tiết.")
                    else:
                        st.success(f"✅ Cảm xúc: {final_label}")
                    
                    st.info(f"Độ tin cậy tổng hợp: {final_conf:.2f}")
                    
                    # Additional details
                    with st.expander("Chi tiết phân tích"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("PhoBERT", f"{l_phobert}", f"{c_phobert:.2f}")
                        with col2:
                            st.metric("Rule-based", f"{rule_based.get_label(s_rule)}", f"{s_rule:.2f}")
                        with col3:
                            st.metric("Fusion", final_label, f"{final_conf:.2f}")
        else:
            st.error("❌ Vui lòng nhập văn bản!")

with tab2:
    st.header("Lịch sử Phân loại")
    history = db.fetch_history()
    if history:
        import pandas as pd
        df = pd.DataFrame(history, columns=["ID", "Input", "Processed", "Label", "Confidence", "Timestamp"])
        
        # Delete all button
        if st.button("Xóa Tất Cả Lịch Sử"):
            try:
                db.delete_all()
                st.success("Đã xóa tất cả lịch sử! Vui lòng làm mới trang.")
            except Exception as e:
                st.error(f"Lỗi khi xóa: {e}")
        
        # Multiselect for individual deletions
        selected_ids = st.multiselect("Chọn ID để xóa:", df["ID"].tolist())
        if st.button("Xóa Các ID Đã Chọn") and selected_ids:
            try:
                for id in selected_ids:
                    db.delete_by_id(id)
                st.success(f"Đã xóa {len(selected_ids)} bản ghi! Vui lòng làm mới trang.")
            except Exception as e:
                st.error(f"Lỗi khi xóa: {e}")
        
        st.dataframe(df)
        
        # Export section
        st.subheader("Xuất dữ liệu")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            csv_data = export_to_csv(df)
            st.download_button(
                label="📄 Xuất CSV",
                data=csv_data,
                file_name=f"sentiment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="csv_export"
            )
        
        with col2:
            json_data = export_to_json(df)
            st.download_button(
                label="📋 Xuất JSON",
                data=json_data,
                file_name=f"sentiment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="json_export"
            )
        
        with col3:
            html_data = export_to_html(df)
            st.download_button(
                label="📕 Xuất HTML",
                data=html_data,
                file_name=f"sentiment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                key="html_export"
            )
        
        with col4:
            ics_data = export_to_ics(df)
            st.download_button(
                label="📅 Xuất ICS",
                data=ics_data,
                file_name=f"sentiment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics",
                mime="text/calendar",
                key="ics_export"
            )
        
        # Import section
        st.subheader("Nhập dữ liệu")
        uploaded_file = st.file_uploader("Chọn file CSV hoặc JSON để nhập", type=['csv', 'json'])
        
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                import_df, error = import_from_csv(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                import_df, error = import_from_json(uploaded_file)
            else:
                st.error("Chỉ hỗ trợ file CSV và JSON!")
                import_df = None
            
            if import_df is not None:
                st.success(f"Đã đọc thành công {len(import_df)} bản ghi từ file.")
                st.dataframe(import_df.head())
                
                if st.button("Thêm vào cơ sở dữ liệu"):
                    try:
                        imported_count = 0
                        for _, row in import_df.iterrows():
                            # Assuming columns: Input, Processed, Label, Confidence
                            if 'Input' in row and 'Label' in row:
                                processed = row.get('Processed', row['Input'])
                                confidence = row.get('Confidence', 0.5)
                                
                                # Insert into database (timestamp will be auto-generated)
                                db.insert_history(row['Input'], processed, row['Label'], confidence)
                                imported_count += 1
                        
                        st.success(f"Đã thêm thành công {imported_count} bản ghi vào cơ sở dữ liệu!")
                        st.info("Vui lòng làm mới trang để xem dữ liệu mới.")
                    except Exception as e:
                        st.error(f"Lỗi khi thêm dữ liệu: {e}")
            elif error:
                st.error(f"Lỗi khi đọc file: {error}")
        
    else:
        st.write("Chưa có lịch sử.")