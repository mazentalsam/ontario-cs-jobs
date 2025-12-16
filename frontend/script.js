const API_URL = "http://localhost:5000/jobs";

let allJobs = [];
let currentCategory = null;
let showingSavedOnly = false;

/* =========================
   SAVED JOBS (localStorage)
========================= */

function getSavedJobs() {
    return JSON.parse(localStorage.getItem("savedJobs")) || [];
}

function isJobSaved(link) {
    return getSavedJobs().includes(link);
}

function toggleSaveJob(link) {
    let saved = getSavedJobs();

    if (saved.includes(link)) {
        saved = saved.filter(l => l !== link);
    } else {
        saved.push(link);
    }

    localStorage.setItem("savedJobs", JSON.stringify(saved));
    updateSavedCount();
}

function updateSavedCount() {
    const el = document.getElementById("saved-count");
    if (el) el.innerText = getSavedJobs().length;
}

/* =========================
   APPLIED JOBS (localStorage)
========================= */

function getAppliedJobs() {
    return JSON.parse(localStorage.getItem("appliedJobs")) || [];
}

function isJobApplied(link) {
    return getAppliedJobs().includes(link);
}

function toggleAppliedJob(link) {
    let applied = getAppliedJobs();

    if (applied.includes(link)) {
        applied = applied.filter(l => l !== link);
    } else {
        applied.push(link);
    }

    localStorage.setItem("appliedJobs", JSON.stringify(applied));
}

/* =========================
   HELPERS
========================= */

function daysAgo(dateString) {
    const posted = new Date(dateString);
    const now = new Date();
    return Math.floor((now - posted) / (1000 * 60 * 60 * 24));
}

function isNewJob(dateString) {
    return daysAgo(dateString) <= 3;
}

/* =========================
   LOAD JOBS
========================= */

async function loadJobs(category = null) {
    const container = document.getElementById("jobs-container");

    container.innerHTML = `
        <div class="skeleton"></div>
        <div class="skeleton"></div>
        <div class="skeleton"></div>
    `;

    let url = API_URL;
    if (category === "faang") {
        url += "?category=faang";
    }

    try {
        const res = await fetch(url);
        allJobs = await res.json();
        renderJobs(allJobs);
    } catch (err) {
        container.innerHTML = "<p>Error loading jobs.</p>";
        console.error(err);
    }
}

/* =========================
   RENDER JOBS
========================= */

function renderJobs(jobs) {
    const container = document.getElementById("jobs-container");
    const count = document.getElementById("job-count");

    container.innerHTML = "";

    let jobsToRender = jobs;

    if (showingSavedOnly) {
        const saved = getSavedJobs();
        jobsToRender = jobs.filter(j => saved.includes(j.link));
    }

    count.innerText = `Showing ${jobsToRender.length} internships`;

    if (jobsToRender.length === 0) {
        container.innerHTML = showingSavedOnly
            ? "<p>No saved jobs yet.</p>"
            : "<p>No jobs found.</p>";
        return;
    }

    jobsToRender.forEach(job => {
        const saved = isJobSaved(job.link);
        const applied = isJobApplied(job.link);
        const isNew = isNewJob(job.date_posted);

        const card = document.createElement("div");
        card.className = "job-card";

        card.innerHTML = `
            <div class="job-header">
                <h3>
                    ${job.title}
                    ${isNew ? `<span class="badge new">NEW</span>` : ""}
                </h3>

                <button class="save-btn ${saved ? "saved" : ""}">
                    ${saved ? "★" : "☆"}
                </button>
            </div>

            <div class="job-meta">
                <strong>${job.company}</strong> · ${job.location}
            </div>

            <div class="job-meta">
                Source: ${job.source}
            </div>

            <div class="posted">
                Posted ${daysAgo(job.date_posted)} days ago
            </div>

            <div class="job-actions">
                <a
                    class="apply-link"
                    href="${job.link}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    View Posting →
                </a>

                <button class="applied-btn ${applied ? "applied" : ""}">
                    ${applied ? "✓ Applied" : "Mark Applied"}
                </button>
            </div>
        `;

        // Save toggle
        card.querySelector(".save-btn").addEventListener("click", () => {
            toggleSaveJob(job.link);
            renderJobs(jobs);
        });

        // Applied toggle
        card.querySelector(".applied-btn").addEventListener("click", () => {
            toggleAppliedJob(job.link);
            renderJobs(jobs);
        });

        container.appendChild(card);
    });
}

/* =========================
   SEARCH
========================= */

document.getElementById("search-input").addEventListener("input", e => {
    const q = e.target.value.toLowerCase();

    const filtered = allJobs.filter(job =>
        job.title.toLowerCase().includes(q) ||
        job.company.toLowerCase().includes(q)
    );

    renderJobs(filtered);
});

/* =========================
   FILTER BUTTONS
========================= */

document.getElementById("all-btn").addEventListener("click", () => {
    showingSavedOnly = false;
    loadJobs();
});

document.getElementById("faang-btn").addEventListener("click", () => {
    showingSavedOnly = false;
    loadJobs("faang");
});

document.getElementById("saved-toggle").addEventListener("click", () => {
    showingSavedOnly = !showingSavedOnly;
    renderJobs(allJobs);
});

/* =========================
   INIT
========================= */

updateSavedCount();
loadJobs();
