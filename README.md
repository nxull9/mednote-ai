# 🩺 MedNote AI

**Smart Medical Documentation System with AI-Powered Clinical Intelligence**

Transform doctor-patient conversations into comprehensive medical reports in seconds. MedNote AI uses advanced speech recognition and clinical AI to generate professional documentation that follows medical guidelines.

---

## ✨ Features

### 🎙 Real-Time Transcription
- Live speech-to-text conversion
- Arabic, English, and mixed language support
- High accuracy medical terminology recognition

### 🧠 Clinical Intelligence
- Evidence-based diagnosis suggestions
- Guideline-compliant treatment recommendations
- Drug interaction and contraindication checking
- Medication stock availability alerts

### 📋 Professional Reports
- Structured medical records (11 sections)
- Patient-friendly summaries
- One-page PDF exports
- Complete clinical documentation

### 🌐 Multi-Language
- Generate reports in English or Arabic
- Automatic translation of medical terms
- Bilingual interface support

---

## 📸 Screenshots

### Main Interface
- **Left:** Patient profile with vitals and allergies
- **Center:** Real-time transcription with recording controls
- **Right:** AI-generated results and analysis

### Report Sections
- 📋 Doctor Report (complete clinical documentation)
- 🧑‍⚕️ Patient Summary (simple language)
- 💊 Medications (with stock status)
- ⚠️ Safety & Advisory (warnings and suggestions)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Microphone access

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mednote-ai.git
cd mednote-ai

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your OpenAI API key

# Run the application
streamlit run app.py
```

### Configuration

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-your-api-key-here"
```

---

## 📖 Usage

1. **Start New Consultation**
   - Click "🆕 New Consultation" button

2. **Record Conversation**
   - Click "🔴 Start Recording"
   - Speak naturally with patient
   - Click "⏹ Stop Recording" when done

3. **Select Report Language**
   - Choose English or Arabic from dropdown

4. **Generate Report**
   - Click "🧠 Generate Report"
   - AI analyzes conversation using clinical guidelines

5. **Review Results**
   - View diagnosis and recommendations
   - Expand sections for detailed information
   - Check medication stock status

6. **Export PDF**
   - Click "📄 Download PDF Report"
   - Get professional one-page medical report

---

## 🧬 Clinical Intelligence

### Medical Knowledge Base

MedNote AI includes clinical guidelines for:

1. **Diabetes Mellitus Type 2** - Metformin first-line therapy
2. **Hypertension** - ACEi/ARB/CCB recommendations
3. **Common Flu/URI** - Supportive care protocols
4. **Asthma** - ICS/LABA treatment plans
5. **Heart Failure** - Multi-drug therapy guidance
6. **Hypothyroidism** - Levothyroxine management
7. **Hyperlipidemia** - Statin recommendations

### Safety Features

- ✅ Drug interaction checking
- ✅ Contraindication warnings
- ✅ Allergy cross-reference
- ✅ Kidney/liver function considerations
- ✅ Pregnancy safety alerts

---

## 📄 Report Structure

### Medical Record Sections

1. Demographics
2. Chief Complaint
3. History of Present Illness
4. Past Medical History
5. Current Medications
6. Allergies
7. Vital Signs
8. Physical Examination
9. Assessment & Diagnosis
10. Medication Plan
11. Follow-Up Instructions

### One-Page PDF

Professional medical report with:
- Patient and doctor information
- Consultation summary
- Complete clinical findings
- Evidence-based treatment plan
- Recommended investigations
- Follow-up schedule

---

## 💊 Medication Features

### Stock Checking

Real-time validation against pharmacy inventory:
- ✅ In Stock - Proceed with prescription
- ❌ Out of Stock - Alternative suggested

### Smart Alternatives

AI suggests clinically appropriate alternatives:
```
❌ Amoxicillin (Out of Stock)
✅ Alternative: Azithromycin
   Rationale: Macrolide antibiotic, broader coverage
```

---

## 🔒 Privacy & Safety

### Disclaimer

⚠️ **Important:** This system is built for testing and research purposes only. MedNote AI is not intended to replace professional medical consultations or clinical judgment. Always consult qualified healthcare professionals for medical decisions.

### Data Handling

- No patient data stored permanently
- Session-based processing only
- API calls use secure HTTPS
- Compliance with medical data standards

---

## 🛠 Technical Details

### Architecture

```
Microphone → PyAudio (16kHz) → OpenAI Whisper API
                                      ↓
                              Transcript (AR/EN/Mixed)
                                      ↓
                          GPT-4 Mini + Clinical Guidelines
                                      ↓
                              Structured Report
                                      ↓
                         PDF Export + UI Display
```

### Tech Stack

- **Frontend:** Streamlit (Python web framework)
- **Transcription:** OpenAI Whisper API
- **AI Analysis:** GPT-4 Mini with clinical prompts
- **Audio:** PyAudio for recording
- **PDF Generation:** ReportLab
- **Word Export:** python-docx

### Cost

Per 10-minute consultation:
- Whisper transcription: ~$0.06
- GPT-4 Mini analysis: ~$0.01
- **Total: ~$0.07 per consultation**

---

## 📦 Dependencies

```
streamlit>=1.28.0
openai>=1.0.0
pyaudio>=0.2.13
python-docx>=0.8.11
reportlab>=3.6.0
```

Full list in `requirements.txt`

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👥 Authors

**Nayef Aljhani**
- GitHub: [nxull9](https://github.com/nxull9)

---

## 🙏 Acknowledgments

- OpenAI for Whisper and GPT-4 APIs
- Medical guidelines from ADA, AHA, ESC, WHO
- Streamlit for the amazing framework

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: your.email@example.com

---

## 🔮 Roadmap

### Upcoming Features

- [ ] Multi-user authentication
- [ ] Cloud deployment
- [ ] EHR integration
- [ ] More disease guidelines (20+ conditions)
- [ ] Real pharmacy API integration
- [ ] Lab result auto-import
- [ ] Appointment scheduling
- [ ] Analytics dashboard

---

**Made with ❤️ for healthcare professionals**
