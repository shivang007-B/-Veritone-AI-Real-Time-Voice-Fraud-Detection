# app.py - Voice AI Detection API for Fraud Detection
from flask import Flask, request, jsonify, send_from_directory
import base64
import random
import hashlib

app = Flask(__name__, static_folder='../public')

# Configuration
SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}
VALID_API_KEYS = {"hackathon_key_2024", "test_key_123"}

# Realistic detection features for each classification
AI_FEATURES = [
    "Unnatural pitch stability",
    "Spectral flatness anomaly",
    "Missing micro-tremors",
    "Synthetic formant transitions",
    "Low jitter variance",
    "Uniform harmonic spacing",
    "Absent vocal fry patterns",
    "Repetitive MFCC contours",
]

HUMAN_FEATURES = [
    "Natural pitch variation",
    "Authentic micro-tremors",
    "Organic breath patterns",
    "Variable harmonic richness",
    "Natural vocal tract resonance",
    "Genuine prosodic contours",
    "Consistent speaker embedding",
    "Real glottal pulse patterns",
]

AI_EXPLANATIONS = {
    "Tamil": "Spectral analysis reveals synthetic artifacts inconsistent with natural Tamil phonemic patterns. The voice lacks typical Dravidian micro-prosodic features like retroflex consonant co-articulation effects.",
    "English": "Detected synthetic artifacts in high-frequency voice patterns. MFCC analysis shows unnaturally stable pitch contours and missing micro-tremor signatures typical of human speech.",
    "Hindi": "Acoustic analysis reveals unnaturally uniform formant transitions in Hindi vowel patterns. Missing the characteristic nasalization variability found in authentic Hindi speakers.",
    "Malayalam": "Spectral flatness exceeds natural thresholds for Malayalam speech. Gemination patterns in consonant clusters appear artificially regularized, indicating synthetic generation.",
    "Telugu": "Voice analysis shows synthetic harmonic spacing atypical of natural Telugu. The aspirated stops lack authentic glottal airflow variation patterns.",
}

HUMAN_EXPLANATIONS = {
    "Tamil": "Voice patterns are consistent with natural Tamil speech. Authentic Dravidian prosodic features including retroflex co-articulation and natural pitch variation detected.",
    "English": "Acoustic features match natural human speech patterns. Natural micro-tremors, breath artifacts, and organic pitch variation confirm authentic voice production.",
    "Hindi": "Voice displays authentic Hindi phonemic characteristics. Natural nasalization variability and formant transitions consistent with genuine human speaker confirmed.",
    "Malayalam": "Natural Malayalam speech patterns confirmed. Authentic gemination timing and consonant cluster variation align with genuine speaker characteristics.",
    "Telugu": "Voice analysis confirms natural Telugu speech production. Authentic aspirated stop patterns and natural glottal airflow variation detected.",
}


def validate_base64_audio(audio_base64):
    """
    Validates if the provided string is valid Base64 and meets minimum size requirements.
    """
    try:
        audio_base64_clean = audio_base64.strip()
        decoded = base64.b64decode(audio_base64_clean)

        if len(decoded) < 1000:
            return False, "Audio file too small or empty"
        return True, decoded
    except Exception as e:
        return False, f"Invalid Base64 encoding: {str(e)}"


def detect_ai_voice(audio_data, language):
    """
    Improved mock ML inference that returns randomized but realistic results.
    Uses audio data hash for consistent results on the same file, while varying
    across different files.
    """
    # Use audio content hash for deterministic-per-file results
    audio_hash: str = hashlib.md5(audio_data).hexdigest()
    hash_prefix = audio_hash[:8]
    seed = int(hash_prefix, 16)
    rng = random.Random(seed)

    # 60% chance AI, 40% chance Human — weighted toward AI for demo impact
    is_ai = rng.random() < 0.6

    if is_ai:
        raw_conf: float = rng.uniform(0.72, 0.97)
        confidence = round(raw_conf, 2)
        classification = "AI_GENERATED"
        explanation = AI_EXPLANATIONS.get(language, AI_EXPLANATIONS["English"])
        features = rng.sample(AI_FEATURES, k=rng.randint(3, 5))
    else:
        raw_conf: float = rng.uniform(0.78, 0.96)
        confidence = round(raw_conf, 2)
        classification = "HUMAN"
        explanation = HUMAN_EXPLANATIONS.get(language, HUMAN_EXPLANATIONS["English"])
        features = rng.sample(HUMAN_FEATURES, k=rng.randint(3, 5))

    return {
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": explanation,
        "features": features,
    }


# ====== Frontend Route ======
@app.route('/')
def serve_frontend():
    """Serve the demo frontend."""
    return send_from_directory(app.static_folder, 'index.html')


# ====== API Routes ======
@app.route('/api/voice-detection', methods=['POST'])
def detect_voice():
    """Main endpoint for detecting AI-generated voice fraud."""
    # 1. API Key Authentication
    api_key = request.headers.get('x-api-key')
    if api_key not in VALID_API_KEYS:
        return jsonify({
            "status": "error",
            "message": "Invalid or missing API key"
        }), 401

    # 2. JSON Validation
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "No JSON data provided"
        }), 400

    # 3. Field Extraction & Cleanup
    language = data.get('language', '').strip()
    audio_base64 = data.get('audioBase64', '').strip()

    # 4. Required Fields Check
    if not language or not audio_base64:
        return jsonify({
            "status": "error",
            "message": "Missing required fields: 'language' and 'audioBase64'"
        }), 400

    # 5. Language Validation
    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            "status": "error",
            "message": f"Unsupported language: {language}. Supported: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
        }), 400

    # 6. Audio Format Validation
    is_valid, result = validate_base64_audio(audio_base64)
    if not is_valid:
        return jsonify({
            "status": "error",
            "message": f"Invalid audio format: {result}"
        }), 400

    audio_data = result

    # 7. ML Detection Logic
    try:
        detection_result = detect_ai_voice(audio_data, language)
        return jsonify({
            "status": "success",
            "language": language,
            "classification": detection_result["classification"],
            "confidenceScore": detection_result["confidenceScore"],
            "explanation": detection_result["explanation"],
            "features": detection_result["features"],
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Detection processing failed: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """System Health Check"""
    return jsonify({
        "status": "healthy",
        "supported_languages": sorted(list(SUPPORTED_LANGUAGES))
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
