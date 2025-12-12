async function loadJobs() {
    const container = document.getElementById("jobs-container");

    try {
        const res = await fetch("http://localhost:5000/jobs");
        const jobs = await res.json();

        container.innerHTML = ""; // clear loading text

        if (jobs.length === 0) {
            container.innerHTML = "<p>No jobs found.</p>";
            return;
        }

        jobs.forEach(job => {
            const div = document.createElement("div");
            div.style.border = "1px solid #ccc";
            div.style.padding = "12px";
            div.style.margin = "12px 0";
            div.style.borderRadius = "6px";

            div.innerHTML = `
                <h3>${job.title}</h3>
                <p><strong>Company:</strong> ${job.company}</p>
                <p><strong>Location:</strong> ${job.location}</p>
                <p><strong>Source:</strong> ${job.source}</p>
                <a href="${job.link}" target="_blank">View Posting</a>
            `;

            container.appendChild(div);
        });

    } catch (err) {
        container.innerHTML = "<p>Error loading jobs.</p>";
        console.error("Error:", err);
    }
}

loadJobs();
