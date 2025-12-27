import streamlit as st
import time
from io import BytesIO
from datetime import datetime
import os
import tempfile

from openai import OpenAI
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from summarizer import generate_report


# =========================
#   PAGE CONFIG
# =========================
st.set_page_config(
    page_title="MedNote AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================
#   OPENAI CLIENT
# =========================
try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
except:
    api_key = os.getenv("OPENAI_API_KEY", "")

client = OpenAI(api_key=api_key) if api_key else None


# =========================
#   CUSTOM CSS
# =========================
st.markdown("""
<style>
    .stApp {
        background: #0a0a0a;
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.1) 0px, transparent 50%);
    }
    
    .stButton>button {
        background: rgba(30, 30, 40, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: rgba(50, 50, 60, 0.9);
        transform: translateY(-2px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stButton>button[kind="primary"] {
        background: #ef4444 !important;
        border: none !important;
        box-shadow: 0 4px 20px 0 rgba(239, 68, 68, 0.5) !important;
    }
    
    .stButton>button[kind="primary"]:hover {
        background: #dc2626 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(59, 130, 246, 0.3);
        color: white;
    }
    
    .stTextArea>div>div>textarea {
        background: rgba(20, 20, 30, 0.8);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6 { color: white !important; }
    
    .stAlert {
        background: rgba(30, 30, 40, 0.8);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stMetricValue"] { color: white; font-size: 28px; }
    [data-testid="stMetricLabel"] { color: rgba(255, 255, 255, 0.7); }
    
    .element-container div[data-testid="stMarkdownContainer"] { color: white; }
    
    .stSelectbox>div>div, .stTextInput>div>div>input {
        background: rgba(30, 30, 40, 0.8);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .disclaimer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(20, 20, 30, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 8px;
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 11px;
        z-index: 999;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =========================
#   SESSION STATE
# =========================
if "report" not in st.session_state:
    st.session_state.report = None
if "full_transcript" not in st.session_state:
    st.session_state.full_transcript = ""
if "report_language" not in st.session_state:
    st.session_state.report_language = "english"
if "doctor_name" not in st.session_state:
    st.session_state.doctor_name = "Dr. Nayef"


# =========================
#   HELPER FUNCTIONS
# =========================
def safe_str(value, default="—"):
    if value is None or (isinstance(value, str) and not value.strip()):
        return default
    return str(value)


def transcribe_audio(audio_file) -> str:
    """Transcribe audio using OpenAI Whisper"""
    if not client:
        return "OpenAI API key not configured"
    
    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        # Transcribe with Whisper
        with open(tmp_path, "rb") as audio:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                language="ar"  # Auto-detect works too, but specifying helps
            )
        
        # Clean up
        os.unlink(tmp_path)
        
        return transcript.text
    
    except Exception as e:
        return f"Transcription error: {str(e)}"


# PDF Generation (same as before, compressed version)
def generate_professional_pdf(rep: dict, doctor_name: str) -> BytesIO:
    """Generate ONE-PAGE compressed medical report PDF"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 30
    
    def draw_compact_text(text, font="Helvetica", size=8, x_offset=70, max_lines=3):
        nonlocal y
        c.setFont(font, size)
        max_width = width - 140
        words = str(text).split()
        line = ""
        lines_drawn = 0
        
        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, font, size) < max_width:
                line = test_line
            else:
                if line and lines_drawn < max_lines:
                    c.drawString(x_offset, y, line.strip()[:95])
                    y -= 10
                    lines_drawn += 1
                line = word + " "
        if line and lines_drawn < max_lines:
            c.drawString(x_offset, y, line.strip()[:95])
            y -= 10
    
    # Compact header
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#3B82F6"))
    c.drawString(50, y, "MedNote AI")
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.grey)
    c.drawString(160, y, "Smart Medical Documentation")
    y -= 15
    
    # Patient info
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.black)
    c.drawString(50, y, f"Dr: {doctor_name}")
    c.setFont("Helvetica", 8)
    c.drawString(200, y, f"Patient: {safe_str(rep.get('patient_name', 'Not documented'))[:20]}")
    
    demo = rep.get('demographics', {})
    demo_parts = []
    if demo.get('age'): demo_parts.append(f"Age:{demo['age']}")
    if demo.get('gender'): demo_parts.append(f"Sex:{demo['gender']}")
    if demo.get('weight'): demo_parts.append(f"Wt:{demo['weight']}")
    if demo.get('height'): demo_parts.append(f"Ht:{demo['height']}")
    
    if demo_parts:
        c.drawString(400, y, " | ".join(demo_parts)[:50])
    
    y -= 10
    c.setFont("Helvetica", 7)
    c.drawString(50, y, datetime.now().strftime('%b %d, %Y'))
    y -= 12
    c.setStrokeColor(colors.grey)
    c.line(50, y, width - 50, y)
    y -= 12
    
    # Overview
    overview = rep.get('conversation_overview', {})
    if overview and overview.get('conversation_summary'):
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "SUMMARY:")
        y -= 10
        draw_compact_text(overview['conversation_summary'], size=7, max_lines=2)
        y -= 5
    
    # Chief Complaint
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "CHIEF COMPLAINT:")
    y -= 10
    draw_compact_text(rep.get('chief_complaint', 'Not documented'), size=7, max_lines=2)
    y -= 5
    
    # HPI
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "HISTORY:")
    y -= 10
    draw_compact_text(rep.get('history_of_present_illness', 'Not documented'), size=7, max_lines=3)
    y -= 5
    
    # Vital Signs
    vitals = rep.get('vital_signs', {})
    if vitals and any(vitals.values()):
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "VITALS:")
        y -= 10
        c.setFont("Helvetica", 7)
        vital_str = " | ".join([
            f"BP:{vitals['blood_pressure']}" if vitals.get('blood_pressure') else "",
            f"HR:{vitals['heart_rate']}" if vitals.get('heart_rate') else "",
            f"Temp:{vitals['temperature']}" if vitals.get('temperature') else "",
        ]).strip(' |')
        c.drawString(70, y, vital_str[:100])
        y -= 12
    
    # Assessment
    assessment = rep.get('clinical_assessment', {})
    if assessment and assessment.get('suspected_diagnosis'):
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "ASSESSMENT:")
        y -= 10
        c.setFont("Helvetica-Bold", 8)
        c.drawString(70, y, safe_str(assessment['suspected_diagnosis'])[:80])
        y -= 10
        if assessment.get('reasoning'):
            draw_compact_text(assessment['reasoning'], size=7, max_lines=2)
        y -= 5
    
    # Medications
    meds = rep.get('medication_plan', [])
    if meds:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "PRESCRIBED:")
        y -= 10
        for i, med in enumerate(meds[:4], 1):
            c.setFont("Helvetica-Bold", 8)
            c.drawString(70, y, f"{i}. {safe_str(med.get('name'))[:30]}")
            y -= 9
            c.setFont("Helvetica", 7)
            c.drawString(85, y, f"{safe_str(med.get('dose'))[:20]} - {safe_str(med.get('frequency'))[:20]}"[:50])
            y -= 9
        y -= 3
    
    # Follow-up
    followup = rep.get('follow_up')
    if followup:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "FOLLOW-UP:")
        y -= 10
        draw_compact_text(followup, size=7, max_lines=2)
    
    # Footer
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.grey)
    c.drawString(50, 25, "MedNote AI - For Testing Purposes Only - Not a substitute for professional medical judgment")
    
    c.save()
    buffer.seek(0)
    return buffer


# =========================
#   HEADER
# =========================
col_new, col_spacer = st.columns([1, 5])
with col_new:
    if st.button("🆕 New Consultation", use_container_width=True):
        st.session_state.full_transcript = ""
        st.session_state.report = None
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-top: -10px; margin-bottom: 5px;'>🩺 MedNote AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.6); margin-bottom: 40px;'>Smart Medical Documentation System</p>", unsafe_allow_html=True)


# =========================
#   MAIN LAYOUT
# =========================
left_col, center_col, right_col = st.columns([1, 2, 1.5])

# LEFT: Patient Profile
with left_col:
    st.markdown("<h3>👤 Patient Profile</h3>", unsafe_allow_html=True)
    
    if st.session_state.report:
        rep = st.session_state.report
        st.markdown(f"<h4>{safe_str(rep.get('patient_name', 'Patient'))}</h4>", unsafe_allow_html=True)
        
        demo = rep.get('demographics', {})
        if demo.get('age'): st.markdown(f"**Age:** {demo['age']}")
        if demo.get('gender'): st.markdown(f"**Gender:** {demo['gender']}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        allergies = rep.get('allergies', {})
        if allergies and allergies.get('drug_allergies'):
            st.markdown("**🚫 Allergies:**")
            for allergy in allergies['drug_allergies']:
                st.error(f"• {allergy}", icon="⚠️")
        
        current_meds = rep.get('current_medications', [])
        if current_meds:
            st.markdown("**💊 Current Medications:**")
            for med in current_meds[:3]:
                st.info(f"• {med.get('name', '—')}")
        
        vitals = rep.get('vital_signs', {})
        if vitals and any(vitals.values()):
            st.markdown("**📊 Vital Signs:**")
            if vitals.get('blood_pressure'): st.metric("BP", vitals['blood_pressure'])
            if vitals.get('heart_rate'): st.metric("HR", vitals['heart_rate'])
            if vitals.get('temperature'): st.metric("Temp", vitals['temperature'])
    else:
        st.info("Patient information will appear here after generating report")

# CENTER: Audio Recording/Upload
with center_col:
    st.markdown("<h3 style='text-align: center;'>🎙 Record Consultation</h3>", unsafe_allow_html=True)
    
    st.info("💡 **Works on ANY device!** 1️⃣ Click mic → 2️⃣ Speak → 3️⃣ Transcribe")
    
    # Audio input (browser recording) - WORKS ON ALL DEVICES!
    audio_input = st.audio_input("Click to record consultation", key="audio_recorder")
    
    if audio_input:
        st.audio(audio_input)
        
        if st.button("📝 Transcribe Audio", type="primary", use_container_width=True):
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(audio_input)
                if st.session_state.full_transcript:
                    st.session_state.full_transcript += "\n\n" + transcript
                else:
                    st.session_state.full_transcript = transcript
            st.success("Transcription complete!")
            st.rerun()
    
    # OR file upload
    st.markdown("---")
    st.markdown("**Or upload an audio file:**")
    uploaded_file = st.file_uploader(
        "Upload audio (WAV, MP3, M4A)",
        type=['wav', 'mp3', 'm4a', 'ogg'],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.audio(uploaded_file)
        
        if st.button("📝 Transcribe Uploaded File", use_container_width=True):
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(uploaded_file)
                if st.session_state.full_transcript:
                    st.session_state.full_transcript += "\n\n" + transcript
                else:
                    st.session_state.full_transcript = transcript
            st.success("Transcription complete!")
            st.rerun()
    
    # Show transcript
    st.markdown("**📝 Full Transcript:**")
    st.text_area(
        "Transcript",
        value=st.session_state.full_transcript,
        height=300,
        label_visibility="collapsed",
        placeholder="Audio will be transcribed here...",
    )

# RIGHT: Results
with right_col:
    st.markdown("<h3>📊 Results</h3>", unsafe_allow_html=True)
    
    st.markdown("**🌐 Select Report Language:**")
    st.session_state.report_language = st.selectbox(
        "Language",
        ["English", "Arabic"],
        label_visibility="collapsed"
    ).lower()
    
    if st.session_state.full_transcript:
        if st.button("🧠 Generate Report", use_container_width=True):
            with st.spinner("AI analyzing..."):
                st.session_state.report = generate_report(
                    st.session_state.full_transcript,
                    st.session_state.report_language
                )
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.report:
        rep = st.session_state.report
        
        # Overview
        overview = rep.get('conversation_overview', {})
        if overview:
            st.markdown("### 💬 Conversation Overview")
            
            if overview.get('what_patient_said'):
                st.info(f"**Patient's Complaint:** {overview['what_patient_said']}")
            
            if overview.get('what_doctor_observed'):
                st.info(f"**Doctor's Observation:** {overview['what_doctor_observed']}")
            
            st.markdown("---")
        
        # Diagnosis
        assessment = rep.get('clinical_assessment', {})
        if assessment and assessment.get('suspected_diagnosis'):
            st.success(f"**🎯 Diagnosis:** {assessment['suspected_diagnosis']}")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Doctor Report",
            "🧑‍⚕️ Patient Summary", 
            "💊 Medications",
            "⚠️ Safety & Advisory"
        ])
        
        with tab1:
            st.markdown("**Chief Complaint:**")
            st.write(safe_str(rep.get('chief_complaint')))
            
            st.markdown("**History of Present Illness:**")
            st.write(safe_str(rep.get('history_of_present_illness')))
            
            st.markdown("**Physical Examination:**")
            st.write(safe_str(rep.get('physical_examination')))
            
            if assessment.get('reasoning'):
                st.markdown("**Clinical Reasoning:**")
                st.info(assessment['reasoning'])
        
        with tab2:
            patient_report = rep.get('patient_report')
            if patient_report:
                st.write(patient_report)
            else:
                st.info("Patient-friendly summary will appear here")
        
        with tab3:
            meds = rep.get('medication_plan', [])
            if meds:
                for i, med in enumerate(meds, 1):
                    stock = med.get('stock_status', {})
                    in_stock = stock.get('in_stock', True)
                    
                    st.markdown(f"**{i}. {safe_str(med.get('name'))}**")
                    
                    if in_stock:
                        st.success("✅ In Stock")
                    else:
                        st.error("❌ Out of Stock")
                        st.info(f"**Alternative:** {safe_str(stock.get('alternative'))}")
                    
                    st.write(f"**Dose:** {safe_str(med.get('dose'))}")
                    st.write(f"**Frequency:** {safe_str(med.get('frequency'))}")
                    st.write(f"**Duration:** {safe_str(med.get('duration'))}")
                    st.write(f"**Instructions:** {safe_str(med.get('instructions'))}")
                    
                    if med.get('guideline_basis'):
                        st.caption(f"📚 {med['guideline_basis']}")
                    st.markdown("---")
            else:
                st.info("No medications prescribed")
        
        with tab4:
            safety = rep.get('safety_checks', [])
            if safety:
                st.markdown("**⚠️ Safety Checks:**")
                for check in safety:
                    st.warning(check)
            
            missing = rep.get('doctor_advisory_missing_questions', [])
            if missing:
                st.markdown("**❓ Suggested Questions:**")
                for i, q in enumerate(missing, 1):
                    st.write(f"{i}. {q}")
        
        # Export
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**👨‍⚕️ Doctor:** {st.session_state.doctor_name}")
        st.caption("(Automatically filled from your account)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📄 Download PDF Report", use_container_width=True, type="primary"):
            pdf_buffer = generate_professional_pdf(rep, st.session_state.doctor_name)
            st.download_button(
                "⬇️ Download PDF",
                pdf_buffer,
                f"MedNote_{safe_str(rep.get('patient_name', 'Patient')).replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("Results will appear here after generating report")

# Disclaimer
st.markdown("""
<div class='disclaimer'>
    ⚠️ This system is built for testing and research purposes only. 
    MedNote AI is not intended to replace professional medical consultations or clinical judgment. 
    Always consult qualified healthcare professionals for medical decisions.
</div>
""", unsafe_allow_html=True)
