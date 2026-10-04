from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
import joblib
import os

from resume_utils import (
    clean_text,
    extract_skills,
    suggest_roles,
    skills,
    role_skills
)


# ---------------------------------
# Create Flask application
# ---------------------------------

app = Flask(__name__)
CORS(app)


# ---------------------------------
# Load trained ML artifacts
# ---------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

tfidf_path = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
model_path = os.path.join(BASE_DIR, "resume_model.pkl")

tfidf = joblib.load(tfidf_path)
model = joblib.load(model_path)


# ---------------------------------
# Health check
# ---------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Resume Screening API is running"
    })


# ---------------------------------
# Resume analysis
# ---------------------------------

@app.route("/analyze", methods=["POST"])
def analyze_resume():

    # Check whether a file was uploaded
    if "resume" not in request.files:
        return jsonify({
            "error": "No resume file uploaded"
        }), 400

    file = request.files["resume"]

    # Check filename
    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    # Check PDF
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are supported"
        }), 400

    try:

        # ---------------------------------
        # 1. Extract text from PDF
        # ---------------------------------

        reader = PdfReader(file)

        pdf_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text


        # ---------------------------------
        # 2. Check extracted text
        # ---------------------------------

        if not pdf_text.strip():
            return jsonify({
                "error": "Could not extract text from this PDF"
            }), 400


        # ---------------------------------
        # 3. Clean text
        # ---------------------------------

        cleaned_text = clean_text(pdf_text)


        # ---------------------------------
        # 4. TF-IDF transformation
        # ---------------------------------

        resume_tfidf = tfidf.transform([cleaned_text])


        # ---------------------------------
        # 5. ML prediction
        # ---------------------------------

        predicted_category = model.predict(resume_tfidf)[0]


        # ---------------------------------
        # 6. Extract skills
        # ---------------------------------

        detected_skills = extract_skills(
            pdf_text,
            skills
        )


        # ---------------------------------
        # 7. Suggest roles
        # ---------------------------------

        role_predictions = suggest_roles(
            detected_skills,
            role_skills
        )


        # ---------------------------------
        # 8. Prepare role results
        # ---------------------------------

        roles = []

        for role, data in role_predictions:

            roles.append({
                "role": role,
                "score": round(data["score"], 1),
                "matched_skills": data["matched_skills"]
            })


        # ---------------------------------
        # 9. Return JSON response
        # ---------------------------------

        return jsonify({
            "category": predicted_category,
            "skills": detected_skills,
            "roles": roles
        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ---------------------------------
# Start server
# ---------------------------------

if __name__ == "__main__":
    app.run(debug=True)