const API_URL = "http://localhost:5000/jobs";

let allJobs = [];
let showingSavedOnly = false;
let currentCategory = null;

/* =========================
   ACTIVE BUTTON HANDLING
========================= */

function setActiveButton(id) {
    document.querySelectorAll(".filter-toggles button")
        .forEach(btn => btn.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

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
    return daysAgo(dateString) <= 1;
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
    currentCategory = category;

    if (category === "faang") {
        url += "?category=faang";
    }

    try {
        const res = await fetch(url);
        allJobs = await res.json();
        applyAllFilters();
    } catch (err) {
        container.innerHTML = "<p>Error loading jobs.</p>";
        console.error(err);
    }
}

/* =========================
   APPLY ALL FILTERS
========================= */

function applyAllFilters() {
    let filtered = [...allJobs];

    const search = document.getElementById("search-input").value.toLowerCase();
    const location = document.getElementById("location-filter")?.value || "";
    const role = document.getElementById("role-filter")?.value || "";
    const time = document.getElementById("time-filter")?.value || "";
    const unappliedOnly = document.getElementById("unapplied-only")?.checked;

    if (showingSavedOnly) {
        const saved = getSavedJobs();
        filtered = filtered.filter(j => saved.includes(j.link));
    }

    if (unappliedOnly) {
        const applied = getAppliedJobs();
        filtered = filtered.filter(j => !applied.includes(j.link));
    }

    if (search) {
        filtered = filtered.filter(j =>
            j.title.toLowerCase().includes(search) ||
            j.company.toLowerCase().includes(search)
        );
    }

    if (location) {
        filtered = filtered.filter(j =>
            j.location.toLowerCase().includes(location)
        );
    }

    if (role) {
        filtered = filtered.filter(j =>
            j.title.toLowerCase().includes(role)
        );
    }

    if (time) {
        filtered = filtered.filter(j =>
            daysAgo(j.date_posted) <= parseInt(time)
        );
    }

    renderJobs(filtered);
}

/* =========================
   RENDER JOBS
========================= */

function renderJobs(jobs) {
    const container = document.getElementById("jobs-container");
    const count = document.getElementById("job-count");

    container.innerHTML = "";
    count.innerText = `Showing ${jobs.length} internships`;

    if (jobs.length === 0) {
        container.innerHTML = "<p>No jobs found.</p>";
        return;
    }

    jobs.forEach(job => {
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

            <div class="posted">
                Posted ${daysAgo(job.date_posted)} days ago
            </div>

            <div class="job-actions">
                <a class="apply-link" href="${job.link}" target="_blank">
                    View Posting →
                </a>
                <button class="applied-btn ${applied ? "applied" : ""}">
                    ${applied ? "✓ Applied" : "Mark Applied"}
                </button>
            </div>
        `;

        card.querySelector(".save-btn").addEventListener("click", () => {
            toggleSaveJob(job.link);
            applyAllFilters();
        });

        card.querySelector(".applied-btn").addEventListener("click", () => {
            toggleAppliedJob(job.link);
            applyAllFilters();
        });

        container.appendChild(card);
    });
}

/* =========================
   FILTER EVENTS
========================= */

document.getElementById("all-btn").addEventListener("click", () => {
    showingSavedOnly = false;
    setActiveButton("all-btn");
    loadJobs();
});

document.getElementById("faang-btn").addEventListener("click", () => {
    showingSavedOnly = false;
    setActiveButton("faang-btn");
    loadJobs("faang");
});

document.getElementById("saved-toggle").addEventListener("click", () => {
    showingSavedOnly = !showingSavedOnly;
    setActiveButton("saved-toggle");
    applyAllFilters();
});

document.querySelectorAll(
    "#search-input, #location-filter, #role-filter, #time-filter, #unapplied-only"
).forEach(el => {
    el.addEventListener("input", applyAllFilters);
    el.addEventListener("change", applyAllFilters);
});

document.querySelectorAll(".filter-controls select").forEach(select => {
  select.addEventListener("change", () => {
    if (select.value) {
      select.classList.add("active");
    } else {
      select.classList.remove("active");
    }
  });
});


/* =========================
   HEADER SCROLL EFFECT
========================= */

window.addEventListener("scroll", () => {
    const header = document.querySelector(".site-header");
    header.classList.toggle("scrolled", window.scrollY > 50);
});

/* =========================
   INIT
========================= */

updateSavedCount();
loadJobs();
