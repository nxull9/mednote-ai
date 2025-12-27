import json
import os
import streamlit as st
from openai import OpenAI


# Initialize OpenAI client
try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
except:
    api_key = os.getenv("OPENAI_API_KEY", "")

client = OpenAI(api_key=api_key) if api_key else None


# Medication stock database
MEDICATION_STOCK = {
    "metformin": True,
    "glipizide": True,
    "empagliflozin": False,
    "dapagliflozin": True,
    "liraglutide": False,
    "lisinopril": True,
    "losartan": True,
    "hydrochlorothiazide": False,
    "amlodipine": True,
    "carvedilol": True,
    "amoxicillin": False,
    "azithromycin": True,
    "ciprofloxacin": True,
    "cephalexin": False,
    "paracetamol": True,
    "acetaminophen": True,
    "ibuprofen": True,
    "omeprazole": True,
    "atorvastatin": True,
    "levothyroxine": True,
    "albuterol": True,
    "aspirin": True,
}


def check_medication_stock(medication_name: str) -> dict:
    """Check medication stock and suggest alternatives"""
    med_lower = medication_name.lower().strip()
    
    for stock_med, available in MEDICATION_STOCK.items():
        if stock_med in med_lower or med_lower in stock_med:
            if available:
                return {"in_stock": True, "alternative": None}
            else:
                alternatives = {
                    "amoxicillin": "azithromycin (macrolide antibiotic, broader coverage)",
                    "cephalexin": "azithromycin (if no allergy to macrolides)",
                    "empagliflozin": "dapagliflozin (same class SGLT2 inhibitor)",
                    "dapagliflozin": "empagliflozin (same class SGLT2 inhibitor)",
                    "liraglutide": "metformin + dietary modification",
                    "hydrochlorothiazide": "amlodipine (calcium channel blocker alternative)",
                }
                alt = alternatives.get(stock_med, "consult pharmacist for equivalent medication")
                return {"in_stock": False, "alternative": alt}
    
    return {"in_stock": True, "alternative": None}


def generate_report(transcript: str, report_language: str = "english") -> dict:
    """
    Convert consultation transcript into comprehensive medical report.
    AGGRESSIVE extraction - capture EVERYTHING from the conversation.
    """
    if not client:
        return _empty_report("OpenAI API key not configured")
    
    if not transcript or not transcript.strip():
        return _empty_report("Transcript was empty")
    
    # Language instruction
    if report_language.lower() == "arabic":
        lang_instruction = "Generate ALL report sections in Arabic (العربية)."
    else:
        lang_instruction = "Generate ALL report sections in English."
    
    system_msg = f"""You are an expert medical AI assistant. Your job is to extract EVERY piece of medical information from the consultation transcript.

{lang_instruction}

CRITICAL INSTRUCTIONS:
1. READ THE ENTIRE CONVERSATION CAREFULLY
2. EXTRACT EVERY DETAIL - symptoms, measurements, medications, history
3. DO NOT leave any section as "Not documented" unless truly not mentioned
4. BE AGGRESSIVE in extraction - if something is implied, include it
5. Capture EXACT values (BP readings, weight, height, ages, etc.)
6. Note EVERY symptom mentioned, even briefly
7. List ALL medications discussed (current and prescribed)
8. Include patient's own words about symptoms

MEDICAL KNOWLEDGE BASE:
- Diabetes Type 2: Polydipsia, polyuria, fatigue, blurred vision → Metformin first-line
- Hypertension: Headaches, dizziness → ACEi/ARB/CCB/Thiazide
- Fatigue: Can be from dehydration, poor sleep, caffeine, anemia, thyroid, heart issues
- Heat sensations: Can indicate anxiety, thyroid, hormones, or referred cardiac symptoms

Output ONLY valid JSON with these exact keys:

{{
  "conversation_overview": {{
    "what_patient_said": "Brief summary of patient's main complaints in their own words",
    "what_doctor_observed": "Doctor's observations and clinical findings",
    "conversation_summary": "2-3 sentence overview of the entire consultation"
  }},
  
  "patient_name": "Extract from conversation, otherwise 'Not documented'",
  
  "demographics": {{
    "age": "Extract if mentioned",
    "gender": "Extract if mentioned",
    "weight": "Extract with unit if mentioned (e.g., 79 kg)",
    "height": "Extract with unit if mentioned (e.g., 182 cm)",
    "contact": "Extract if mentioned"
  }},
  
  "chief_complaint": "Main reason for visit - be specific",
  
  "history_of_present_illness": "DETAILED description including: onset, duration, severity, associated symptoms, aggravating/relieving factors, impact on daily life",
  
  "past_medical_history": {{
    "diabetes": "true/false or details",
    "hypertension": "true/false or details",
    "asthma": "true/false or details",
    "heart_failure": "true/false or details",
    "hypothyroidism": "true/false or details",
    "hyperlipidemia": "true/false or details",
    "kidney_disease": "true/false or details",
    "liver_disease": "true/false or details",
    "copd": "true/false or details",
    "cancer": "true/false or details",
    "other": "Any other conditions mentioned"
  }},
  
  "past_surgical_history": "List any surgeries or 'None mentioned'",
  
  "current_medications": [
    {{
      "name": "Medication name",
      "dose": "Dose if mentioned",
      "frequency": "How often if mentioned",
      "duration": "How long taking if mentioned"
    }}
  ],
  
  "allergies": {{
    "drug_allergies": ["List all mentioned allergies"],
    "reactions": ["Type of reaction for each"]
  }},
  
  "vital_signs": {{
    "blood_pressure": "Extract EXACT reading if mentioned (e.g., 140/90)",
    "heart_rate": "Extract if mentioned",
    "respiratory_rate": "Extract if mentioned",
    "temperature": "Extract if mentioned",
    "oxygen_saturation": "Extract if mentioned"
  }},
  
  "physical_examination": "Document ALL examination findings mentioned. If none performed, say 'No physical examination documented in this conversation'",
  
  "lab_results": {{
    "mentioned": true/false,
    "details": "List any lab results discussed"
  }},
  
  "social_history": {{
    "smoking": "Extract if discussed",
    "alcohol": "Extract if discussed",
    "physical_activity": "Extract if discussed",
    "diet": "Extract if discussed (caffeine intake, eating habits, etc.)",
    "occupation": "Extract if mentioned",
    "sleep": "Extract sleep patterns if discussed"
  }},
  
  "family_history": {{
    "diabetes": "true/false or details",
    "hypertension": "true/false or details",
    "heart_disease": "true/false or details",
    "cancer": "true/false or details",
    "other": "Any other family conditions"
  }},
  
  "clinical_assessment": {{
    "suspected_diagnosis": "Primary diagnosis based on symptoms and clinical guidelines",
    "differential_diagnosis": ["List other possibilities"],
    "reasoning": "DETAILED explanation: What symptoms led to this diagnosis? What patterns match? Reference clinical guidelines."
  }},
  
  "recommended_workup": [
    "List specific tests/imaging needed (e.g., 'CBC to rule out anemia', 'TSH to check thyroid')"
  ],
  
  "medication_plan": [
    {{
      "name": "Medication name",
      "dose": "Specific dose and form",
      "frequency": "How often",
      "duration": "How long",
      "instructions": "Special instructions",
      "guideline_basis": "Why this medication per guidelines"
    }}
  ],
  
  "safety_checks": [
    "List important safety considerations (e.g., 'Monitor BP weekly', 'Check for side effects')"
  ],
  
  "contraindications_checked": [
    "List what was checked (e.g., 'No pregnancy', 'No kidney disease', 'No drug allergies')"
  ],
  
  "alternative_if_contraindicated": [
    "Alternative medications if first-line unavailable or contraindicated"
  ],
  
  "follow_up": "Specific follow-up plan with timeline",
  
  "doctor_advisory_missing_questions": [
    "Critical questions doctor should ask to complete assessment"
  ],
  
  "patient_report": "Patient-friendly summary in SIMPLE language explaining: what's wrong, why it happened, what to do, what medications to take, when to come back, warning signs to watch for"
}}

EXAMPLES OF GOOD EXTRACTION:

BAD: "Patient has fatigue"
GOOD: "Patient reports severe fatigue for 2 days, especially after work. Describes feeling exhausted by afternoon, with difficulty concentrating. Also experiencing heat sensations in neck and shoulders, and poor sleep quality."

BAD: "Vital signs: Not documented"
GOOD: "Blood pressure: 140/90 mmHg (patient reports), Weight: 79 kg, Height: 182 cm"

BAD: "Current medications: None"  
GOOD: "Current medications: Lisinopril 10mg daily for hypertension (started 2 years ago)"

REMEMBER: Extract EVERYTHING. Be thorough. Don't miss details.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"CONSULTATION TRANSCRIPT (extract ALL information):\n\n{transcript}"},
            ],
            temperature=0.2,  # Lower temperature for more consistent extraction
        )
        
        raw = response.choices[0].message.content
        
        # Parse JSON
        try:
            data = json.loads(raw)
        except:
            try:
                start = raw.index("{")
                end = raw.rindex("}") + 1
                data = json.loads(raw[start:end])
            except:
                return _empty_report(f"Failed to parse AI response")
        
        # Check medication stock
        medication_plan = data.get("medication_plan", []) or []
        for med in medication_plan:
            stock_info = check_medication_stock(med.get("name", ""))
            med["stock_status"] = stock_info
        
        # Ensure all keys exist
        return {
            "conversation_overview": data.get("conversation_overview", {}) or {},
            "patient_name": data.get("patient_name", "Not documented") or "Not documented",
            "demographics": data.get("demographics", {}) or {},
            "chief_complaint": data.get("chief_complaint", "") or "",
            "history_of_present_illness": data.get("history_of_present_illness", "") or "",
            "past_medical_history": data.get("past_medical_history", {}) or {},
            "past_surgical_history": data.get("past_surgical_history", "") or "",
            "current_medications": data.get("current_medications", []) or [],
            "allergies": data.get("allergies", {}) or {},
            "vital_signs": data.get("vital_signs", {}) or {},
            "physical_examination": data.get("physical_examination", "") or "",
            "lab_results": data.get("lab_results", {}) or {},
            "social_history": data.get("social_history", {}) or {},
            "family_history": data.get("family_history", {}) or {},
            "clinical_assessment": data.get("clinical_assessment", {}) or {},
            "recommended_workup": data.get("recommended_workup", []) or [],
            "medication_plan": medication_plan,
            "safety_checks": data.get("safety_checks", []) or [],
            "contraindications_checked": data.get("contraindications_checked", []) or [],
            "alternative_if_contraindicated": data.get("alternative_if_contraindicated", []) or [],
            "follow_up": data.get("follow_up", "") or "",
            "doctor_advisory_missing_questions": data.get("doctor_advisory_missing_questions", []) or [],
            "patient_report": data.get("patient_report", "") or "",
            "patient_profile_updates": data.get("patient_profile_updates", {}) or {},
        }
        
    except Exception as e:
        return _empty_report(f"Error generating report: {str(e)}")


def _empty_report(error_msg: str) -> dict:
    """Return empty report structure"""
    return {
        "conversation_overview": {},
        "patient_name": "Not documented",
        "demographics": {},
        "chief_complaint": error_msg,
        "history_of_present_illness": "",
        "past_medical_history": {},
        "past_surgical_history": "",
        "current_medications": [],
        "allergies": {},
        "vital_signs": {},
        "physical_examination": "",
        "lab_results": {},
        "social_history": {},
        "family_history": {},
        "clinical_assessment": {},
        "recommended_workup": [],
        "medication_plan": [],
        "safety_checks": [],
        "contraindications_checked": [],
        "alternative_if_contraindicated": [],
        "follow_up": "",
        "doctor_advisory_missing_questions": [],
        "patient_report": "",
        "patient_profile_updates": {},
    }
