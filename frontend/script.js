const API_URL = "http://localhost:5000/jobs";

let allJobs = [];

// Convert YYYY-MM-DD → human readable
function daysAgo(dateString) {
    const posted = new Date(dateString);
    const now = new Date();
    const diff = Math.floor((now - posted) / (1000 * 60 * 60 * 24));

    if (diff <= 0) return "Posted today";
    if (diff === 1) return "Posted 1 day ago";
    return `Posted ${diff} days ago`;
}

async function loadJobs() {
    const container = document.getElementById("jobs-container");

    try {
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error();

        allJobs = await res.json();
        renderJobs(allJobs);

    } catch (err) {
        container.innerHTML = `
            <p class="error">
                Error loading jobs. Please try again later.
            </p>
        `;
    }
}

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
        const card = document.createElement("div");
        card.className = "job-card";

        card.innerHTML = `
            <h3>${job.title}</h3>

            <div class="job-meta">
                <strong>${job.company}</strong> · ${job.location}
            </div>

            <div class="job-meta">
                Source: ${job.source}
            </div>

            <div class="posted">
                ${daysAgo(job.date_posted)}
            </div>

            <a
                class="apply-link"
                href="${job.link}"
                target="_blank"
                rel="noopener noreferrer"
            >
                View Posting →
            </a>
        `;

        container.appendChild(card);
    });
}

// Search filtering
document.getElementById("search-input").addEventListener("input", e => {
    const q = e.target.value.toLowerCase();

    const filtered = allJobs.filter(job =>
        job.title.toLowerCase().includes(q) ||
        job.company.toLowerCase().includes(q)
    );

    renderJobs(filtered);
});

// Initial load
loadJobs();
