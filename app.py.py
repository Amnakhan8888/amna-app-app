# -*- coding: utf-8 -*-
import streamlit as st
from PIL import Image
import pytesseract
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import re
from datetime import datetime, timedelta

# ---------- Introduction ----------
st.title("📱 Digital Stress Scale Web App")
st.write("""
**Developer:** Amna Khan – Clinical Psychologist, Researcher, and Data Analyst

Welcome! This bilingual (Urdu + English) app will help you assess your digital stress level.
Please complete the payment to unlock the full assessment.
""")

st.markdown("""
### Introduction

This tool is based on the **Multidimensional Digital Stressor Scale (MDSS)**.
It is designed **only** for individuals aged **18 to 30 years**.
It diagnoses the **level of digital stress** you may be experiencing due to usage of devices such as mobile phones, laptops, and social media.

⚠️ **Important Notes:**
- This tool specifically measures **digital stress**, not other types of stress.
- It does **not** assess professional or work-related stress caused by using devices for your job or study.
- Please answer all questions honestly based on your experience in the **past 7 days**.
- While it is a diagnostic tool for digital stress, it should be used for **awareness and guidance**, not as a substitute for professional medical or psychological evaluation.
""")

# ---------- Part 1: Sample Questions ----------
st.subheader("Sample Questions")
sample_items = [
    ("Most of my friends approve of me being constantly available online",
     "میرے زیادہ تر دوست میرے مسلسل آن لائن رہنے سے متفق ہیں"),
    ("I feel a social obligation to be constantly available online",
     "مسلسل آن لائن رہنا مجھے ایک سماجی ذمہ داری محسوس ہوتا ہے")
]
scale_labels = ["0 - Strongly Disagree", "1 - Disagree", "2 - Neutral", "3 - Agree", "4 - Strongly Agree"]

for idx, item in enumerate(sample_items, 1):
    st.markdown(f"**Q{idx}. {item[0]}**  \n_{item[1]}_")
    st.radio("", scale_labels, key=f"sample_{idx}")

# ------------------------------
# Step 1: Initialize session_state
# ------------------------------
if 'payment_verified' not in st.session_state:
    st.session_state['payment_verified'] = False  # Default: not verified

if 'transaction_code' not in st.session_state:
    st.session_state['transaction_code'] = None  # Optional: store verification code
# ---------- Payment Verification ----------
# Step 2: Payment instruction
import streamlit as st
from PIL import Image
import pytesseract
import re
from datetime import datetime, timedelta

# Your payment details
EASYPaisa_NUMBER = "03290120728"   # replace with your real Easypaisa number
MY_NAME = "Amna Khan"
EXPECTED_AMOUNT_PKR = "560"
EXPECTED_AMOUNT_USD = "2"
ALLOWED_HOURS = 2  # slip must be within last 6 hours

st.title("💳 Payment Verification System")

slip = st.file_uploader("Upload your Easypaisa Payment Slip", type=["jpg", "png", "jpeg"])

if slip:
    image = Image.open(slip)

    # Extract text from slip
    extracted_text = pytesseract.image_to_string(image)

    st.write("📜 Extracted Slip Text:")
    st.code(extracted_text)

    # Check conditions
    number_ok = EASYPaisa_NUMBER in extracted_text
    name_ok = MY_NAME.lower() in extracted_text.lower()
    amount_ok = EXPECTED_AMOUNT_PKR in extracted_text or EXPECTED_AMOUNT_USD in extracted_text

    # Check date + time (example format: 19/08/2025 14:35 or 19-08-2025 14:35)
    datetime_match = re.search(r"(\d{2}[-/]\d{2}[-/]\d{4}\s+\d{2}:\d{2})", extracted_text)
    datetime_ok = False
    if datetime_match:
        try:
            slip_datetime = datetime.strptime(datetime_match.group(1), "%d/%m/%Y %H:%M")
        except:
            slip_datetime = datetime.strptime(datetime_match.group(1), "%d-%m-%Y %H:%M")

        time_diff = datetime.now() - slip_datetime
        if time_diff <= timedelta(hours=ALLOWED_HOURS):
            datetime_ok = True

    # Final verification
    if number_ok and name_ok and amount_ok and datetime_ok:
        st.success("✅ Payment Verified Successfully!")
        st.write("Redirecting you to the Assessment Tool...")

        # Redirect / unlock assessment
        st.page_link("assessment_tool.py", label="👉 Start Assessment Now")
    else:
        st.error("❌ Payment verification failed. Slip is fake, old, or invalid.")





# ---------- Full Assessment ----------
if st.session_state['payment_verified']:
    st.subheader("📝 Full Digital Stress Assessment")
    
    digital_stress_items = [
        {"id": 1, "en_text": "Most of my friends approve of me being constantly available online", "ur_text": "میرے زیادہ تر دوست میرے مسلسل آن لائن رہنے سے متفق ہیں"},
        {"id": 2, "en_text": "I feel a social obligation to be constantly available online", "ur_text": "مسلسل آن لائن رہنا مجھے ایک سماجی ذمہ داری محسوس ہوتا ہے"},
        {"id": 3, "en_text": "I am nervous about how people will respond to my posts and photos", "ur_text": "میں پریشان ہوتا ہوں کہ لوگ میرے پوسٹ اور تصویر کا کس طرح سے جواب دیں گے؟"},
        {"id": 4, "en_text": "I feel anxious about how others will respond when I share a new photo on social media", "ur_text": "میری طرف سے سوشل میڈیا پر کوئی نئی تصویر شیئر کی جاتی ہے تو مجھے بیچینی ہوتی ہے کہ دوسرے کیسے جواب دیں گے؟"},
        # ... add the remaining questions here ...
    ]

    responses = []
    for item in digital_stress_items:
        st.markdown(f"**Q{item['id']}. {item['en_text']}**  \n_{item['ur_text']}_")
        score = st.radio("", scale_labels, key=f"q{item['id']}")
        responses.append(int(score.split(" - ")[0]))

    if st.button("Submit Full Assessment"):
        total_score = sum(responses)
        st.write(f"**Your total digital stress score is: {total_score}**")
        
        # Categorize stress level
        if total_score <= 21:
            st.info("Low digital stress")
        elif total_score <= 44:
            st.info("Moderate digital stress")
        elif total_score <= 66:
            st.warning("Elevated digital stress")
        else:
            st.error("High digital stress")
else:
    st.info("🔒 Full assessment is locked. Complete payment to unlock it.")
