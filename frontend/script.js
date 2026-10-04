const resumeInput = document.getElementById("resumeInput");
const analyzeBtn = document.getElementById("analyzeBtn");

const statusText = document.getElementById("status");
const categoryText = document.getElementById("category");
const skillsContainer = document.getElementById("skills");
const rolesContainer = document.getElementById("roles");


analyzeBtn.addEventListener("click", async () => {

    const file = resumeInput.files[0];

    // Check whether a file was selected
    if (!file) {
        statusText.textContent = "Please select a PDF resume.";
        return;
    }

    // Check file type
    if (!file.name.toLowerCase().endsWith(".pdf")) {
        statusText.textContent = "Only PDF files are supported.";
        return;
    }

    statusText.textContent = "Analyzing resume...";

    analyzeBtn.disabled = true;

    const formData = new FormData();

    formData.append("resume", file);

    try {

        const response = await fetch(
            "https://ai-resume-analyzer-10r8.onrender.com",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        displayResults(data);

        statusText.textContent = "Resume analyzed successfully.";

    } catch (error) {

        console.error(error);

        statusText.textContent =
            "Error: " + error.message;

    } finally {

        analyzeBtn.disabled = false;
    }
});


function displayResults(data) {

    // -----------------------------
    // Predicted Category
    // -----------------------------

    categoryText.textContent = data.category;


    // -----------------------------
    // Detected Skills
    // -----------------------------

    skillsContainer.innerHTML = "";

    if (data.skills.length === 0) {

        skillsContainer.textContent =
            "No predefined skills detected.";

    } else {

        data.skills.forEach(skill => {

            const skillElement =
                document.createElement("span");

            skillElement.className = "skill";

            skillElement.textContent = skill;

            skillsContainer.appendChild(skillElement);

        });
    }


    // -----------------------------
    // Suggested Roles
    // -----------------------------

    rolesContainer.innerHTML = "";

    if (data.roles.length === 0) {

        rolesContainer.textContent =
            "No role suggestions available.";

        return;
    }


    // Show top 5 roles
    const topRoles = data.roles.slice(0, 5);


    topRoles.forEach(roleData => {

        const roleElement =
            document.createElement("div");

        roleElement.className = "role";


        const header =
            document.createElement("div");

        header.className = "role-header";


        const roleName =
            document.createElement("span");

        roleName.className = "role-name";

        roleName.textContent =
            roleData.role;


        const roleScore =
            document.createElement("span");

        roleScore.className = "role-score";

        roleScore.textContent =
            roleData.score + "%";


        header.appendChild(roleName);
        header.appendChild(roleScore);


        const matchedSkills =
            document.createElement("div");

        matchedSkills.className =
            "matched-skills";

        matchedSkills.textContent =
            "Matched skills: " +
            (
                roleData.matched_skills.length > 0
                    ? roleData.matched_skills.join(", ")
                    : "None"
            );


        roleElement.appendChild(header);
        roleElement.appendChild(matchedSkills);

        rolesContainer.appendChild(roleElement);

    });
}