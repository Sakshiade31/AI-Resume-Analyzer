import re


# -----------------------------
# Text Cleaning
# -----------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Skills
# -----------------------------

skills = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "natural language processing",
    "nlp",
    "computer vision",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "git",
    "linux",
    "html",
    "css",
    "javascript",
    "react",
    "angular",
    "node.js",
    "spring boot",
    "mongodb",
    "postgresql",
    "mysql",
    "c++",
    "c#",
    "salesforce",
    "sap",
    "project management",

    # Engineering / Operations skills
    "lean manufacturing",
    "production planning",
    "supply chain management",
    "quality control",
    "inventory management",
    "minitab",
    "autocad",
    "solidworks"
]


# -----------------------------
# Extract Skills
# -----------------------------

def extract_skills(text, skills):
    text = text.lower()

    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# -----------------------------
# Role → Skills
# -----------------------------

role_skills = {

    "Software Engineer": [
        "python",
        "java",
        "sql",
        "javascript",
        "git",
        "spring boot",
        "c++",
        "c#"
    ],

    "Data Scientist": [
        "python",
        "machine learning",
        "data science",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data analysis",
        "pandas"
    ],

    "ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "docker",
        "aws"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "angular",
        "node.js"
    ],

    "Industrial Engineer": [
        "project management",
        "data analysis",
        "excel",
        "sap",
        "lean manufacturing",
        "production planning",
        "supply chain management",
        "quality control",
        "inventory management",
        "minitab",
        "autocad",
        "solidworks"
    ],

    "Mechanical Engineer": [
        "c++",
        "autocad",
        "solidworks",
        "minitab",
        "project management",
        "quality control"
    ],

    "Supply Chain Analyst": [
        "excel",
        "sap",
        "data analysis",
        "supply chain management",
        "inventory management",
        "project management"
    ]
}


# -----------------------------
# Role Matching
# -----------------------------

def suggest_roles(found_skills, role_skills):

    role_scores = {}

    for role, required_skills in role_skills.items():

        matches = set(found_skills).intersection(required_skills)

        score = len(matches) / len(required_skills) * 100

        role_scores[role] = {
            "score": score,
            "matched_skills": list(matches)
        }

    return sorted(
        role_scores.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )