# 🩺 MedNote AI

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**AI-Powered Medical Documentation System**

*Transform doctor patient conversations into medical reports in seconds*

[🚀 Live Demo](https://mednote-ai-duphat.streamlit.app) • [📖 Documentation](#documentation) • [🐛 Report Bug](https://github.com/nxull9/mednote-ai/issues) • [✨ Request Feature](https://github.com/nxull9/mednote-ai/issues)

</div>

---

## 📋 Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [Clinical Intelligence](#clinical-intelligence)
- [Cost Analysis](#cost-analysis)
- [Security & Privacy](#security--privacy)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## 🎯 About

MedNote AI is an intelligent medical documentation system that leverages advanced AI to convert doctor-patient consultations into structured, guideline compliant medical reports. The system addresses a critical challenge in healthcare: reducing the administrative burden of medical documentation while maintaining clinical accuracy and completeness.

In many clinics, a 15-minute consultation often becomes 30 minutes of documentation.

This is not a medical problem. It is an administrative one.

MedNote AI was built to restore that balance. Doctors speak naturally with patients, and the system converts the conversation into a structured medical report aligned with clinical guidelines, in both Arabic and English.

The underlying technologies are mature. Speech recognition and LLMs already exist. What is missing is a system that works reliably in real clinical settings, supports Arabic natively, and integrates smoothly into a doctor’s workflow.

That is the gap this project addresses.

A doctor uses MedNote AI once and saves around 15 minutes. Used across 20 consultations in a day, that returns nearly 5 hours of time back to patient care rather than paperwork.

---

## ✨ Key Features

### 🎙️ Intelligent Transcription
- **Real-time speech-to-text** using OpenAI Whisper
- **Mixed language support** (Arabic/English)
- **Medical terminology recognition**
- **Browser-based recording** (works on any device)

### 🧠 Clinical Decision Support
- **Evidence-based recommendations** from ADA, AHA, ESC, WHO guidelines
- **Drug interaction checking** and contraindication warnings
- **Medication stock validation** with automatic alternatives
- **Safety alerts** for allergies, pregnancy, renal/hepatic function

### 📄 Professional Documentation
- **Structured medical records** with 11 standardized sections
- **One-page PDF reports** optimized for clinical workflows
- **Patient-friendly summaries** in simple language
- **Bilingual reports** (English/Arabic)

### 🔍 Smart Features
- **Differential diagnosis suggestions** based on symptoms
- **Missing information alerts** for complete documentation
- **Guideline compliance checking** for treatment plans
- **Clinical reasoning explanations** for each diagnosis

---

## 🛠️ Technology Stack

### Core Technologies
- **Frontend:** [Streamlit](https://streamlit.io/) - Modern Python web framework
- **AI/ML:** [OpenAI GPT-4 Mini](https://openai.com/) - Language understanding & report generation
- **Speech Recognition:** [OpenAI Whisper](https://openai.com/research/whisper) - Multilingual transcription
- **PDF Generation:** [ReportLab](https://www.reportlab.com/) - Professional document creation

### Clinical Knowledge Base
- 7 disease-specific clinical guidelines
- 23 medications with stock tracking
- Drug interaction database
- Safety contraindication rules

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
OpenAI API key
Modern web browser (Chrome, Safari, Firefox, Edge)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nxull9/mednote-ai.git
cd mednote-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API credentials**
```bash
# Create secrets file
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit with your API key
nano .streamlit/secrets.toml
```

Add your OpenAI API key:
```toml
OPENAI_API_KEY = "sk-your-api-key-here"
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the app**
```
Open your browser to: http://localhost:8501
```

### Quick Deploy to Cloud

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📖 Usage Guide

### Basic Workflow

1. **Start New Consultation**
   - Click `🆕 New Consultation` button
   - Patient profile resets for new case

2. **Record Consultation**
   - Click microphone icon to start recording
   - Speak naturally (supports mixed Arabic/English)
   - Browser will request microphone permission (allow it)
   - Recording indicator shows active capture

3. **Transcribe Audio**
   - Click `📝 Transcribe Audio` when finished
   - Wait 5-10 seconds for AI processing
   - Transcript appears in text area

4. **Generate Medical Report**
   - Select report language (English/Arabic)
   - Click `🧠 Generate Report`
   - AI analyzes consultation against clinical guidelines
   - Wait 10-15 seconds for comprehensive analysis

5. **Review & Export**
   - Review AI-generated diagnosis and recommendations
   - Check medication stock status
   - Verify safety alerts
   - Click `📄 Download PDF Report` for one-page professional document

### Advanced Features

#### Alternative Audio Input
- **File Upload:** Support for WAV, MP3, M4A, OGG formats
- **Pre-recorded consultations:** Upload existing recordings
- **Batch processing:** Multiple files in sequence

#### Report Customization
- **Doctor name auto-fill** from authentication
- **Language switching** without re-generating
- **Section-by-section review** via tabs

---

## 🏥 Clinical Intelligence

### Supported Conditions

MedNote AI includes evidence-based clinical guidelines for:

| Condition | Guideline Source | Key Medications |
|-----------|------------------|-----------------|
| **Diabetes Mellitus Type 2** | ADA 2024 | Metformin, GLP-1 agonists |
| **Hypertension** | AHA/ACC 2023 | ACE-I, ARB, CCB, Diuretics |
| **Common Cold/URI** | CDC Guidelines | Symptomatic treatment |
| **Asthma** | GINA 2024 | ICS, LABA, SABA |
| **Heart Failure** | ESC 2023 | ACE-I, Beta-blockers, Diuretics |
| **Hypothyroidism** | ATA Guidelines | Levothyroxine |
| **Hyperlipidemia** | ACC/AHA 2023 | Statins, Ezetimibe |

### Safety Checks

The AI performs comprehensive safety validation:

- ✅ **Drug Drug Interactions:** Cross references all prescribed medications
- ✅ **Allergy Alerts:** Warns about contraindicated medications
- ✅ **Contraindications:** Checks for pregnancy, renal/hepatic impairment
- ✅ **Dosing Adjustments:** Recommends modifications based on patient factors
- ✅ **Missing Information:** Flags incomplete clinical data

### Medication Stock Management

Real time inventory integration:
- 23 common medications in database
- Automatic alternative suggestions when out of stock
- Therapeutic equivalence checking
- Cost-effective substitutions

Example:
```
❌ Amoxicillin - Out of Stock
✅ Suggested Alternative: Azithromycin
   • Rationale: Macrolide antibiotic, broader coverage
   • Dose adjustment: 500mg daily vs 500mg TID
```

---

## 💰 Cost Analysis

### OpenAI API Usage (per consultation)

| Service | Duration | Cost |
|---------|----------|------|
| Whisper Transcription | 10 min audio | $0.06 |
| GPT-4 Mini Analysis | ~2000 tokens | $0.01 |
| **Total per consultation** | | **~$0.07** |

### Monthly Estimates

| Consultations/Day | Monthly Cost | Annual Cost |
|-------------------|--------------|-------------|
| 10 | $21 | $252 |
| 50 | $105 | $1,260 |
| 100 | $210 | $2,520 |

*Costs based on OpenAI pricing as of December 2024*

---

## 🔒 Security & Privacy

### Data Protection

- **No Persistent Storage:** All data is session-based only
- **Secure Communication:** HTTPS encryption for all API calls
- **API Key Protection:** Environment variables and .gitignore
- **No Patient Identifiers:** System doesn't store PHI permanently

### Compliance Considerations

⚠️ **Important Notice:** MedNote AI is currently designed for **testing and research purposes only**. 

For production medical use, additional measures required:
- HIPAA compliance certification
- Data encryption at rest and in transit
- Audit logging
- User authentication and access control
- Business Associate Agreement (BAA) with OpenAI

### Best Practices

1. **Never commit API keys** to version control
2. **Use separate API keys** for dev/prod environments
3. **Implement user authentication** before production
4. **Regular security audits** of dependencies
5. **Monitor API usage** for anomalies

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report bugs** and issues
- 💡 **Suggest new features** and improvements
- 📖 **Improve documentation**
- 🧪 **Write tests** and improve code quality
- 🌍 **Add translations** for new languages
- 🏥 **Contribute clinical guidelines** and medical knowledge

### Development Setup

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

### Code Style

- Follow [PEP 8](https://pep8.org/) for Python code
- Add docstrings to all functions
- Write unit tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Contact

**Nayef Aljhani**

- GitHub: [@nxull9](https://github.com/nxull9)
- Project Link: [https://github.com/nxull9/mednote-ai](https://github.com/nxull9/mednote-ai)
- Live Demo: [https://mednote-ai-duphat.streamlit.app](https://mednote-ai-duphat.streamlit.app)

---

## 🙏 Acknowledgments

### Technologies & Services
- [OpenAI](https://openai.com/) - GPT-4 and Whisper APIs
- [Streamlit](https://streamlit.io/) - Application framework
- [ReportLab](https://www.reportlab.com/) - PDF generation

### Medical Guidelines
- American Diabetes Association (ADA)
- American Heart Association (AHA)
- European Society of Cardiology (ESC)
- World Health Organization (WHO)
- Global Initiative for Asthma (GINA)
- American Thyroid Association (ATA)



---

<div align="center">

**Made with ❤️ from Tabuk to all healthcare professionals**



[⬆ Back to Top](#-mednote-ai)

</div>
