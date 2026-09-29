const API_URL = "http://127.0.0.1:5000";

const loading = document.getElementById("loading");
const titlesGrid = document.getElementById("titles-grid");
const emptyState = document.getElementById("empty-state");
const itemCount = document.getElementById("item-count");
const message = document.getElementById("message");

const detailSection = document.getElementById("detail-section");
const detailTitle = document.getElementById("detail-title");
const detailContent = document.getElementById("detail-content");

const formSection = document.getElementById("form-section");
const titleForm = document.getElementById("title-form");
const formHeading = document.getElementById("form-heading");
const formEyebrow = document.getElementById("form-eyebrow");
const submitButton = document.getElementById("submit-button");
const formError = document.getElementById("form-error");

let editingId = null;

async function loadTitles() {
    loading.classList.remove("hidden");
    titlesGrid.innerHTML = "";
    emptyState.classList.add("hidden");

    try {
        const response = await fetch(`${API_URL}/titles`);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }

        const titles = await response.json();

        loading.classList.add("hidden");

        itemCount.textContent =
            `${titles.length} title${titles.length === 1 ? "" : "s"}`;

        if (titles.length === 0) {
            emptyState.classList.remove("hidden");
            return;
        }

        titles.forEach(title => {
            const card = document.createElement("article");
            card.className = "title-card";

            card.innerHTML = `
                <div class="card-header">
                    <span class="type-badge">${escapeHtml(title.type)}</span>
                    <span class="rating">
                        ⭐ ${title.rating ?? "N/A"}
                    </span>
                </div>

                <h3>${escapeHtml(title.title)}</h3>

                <p>
                    ${title.year} • ${escapeHtml(title.genre)}
                </p>

                <p class="creator">
                    ${title.creator ? `Creator: ${escapeHtml(title.creator)}` : ""}
                </p>

                <div class="card-actions">
                    <button class="button secondary"
                            onclick="viewTitle(${title.id})">
                        View
                    </button>

                    <button class="button secondary"
                            onclick="editTitle(${title.id})">
                        Edit
                    </button>

                    <button class="button danger"
                            onclick="deleteTitle(${title.id})">
                        Delete
                    </button>
                </div>
            `;

            titlesGrid.appendChild(card);
        });

    } catch (error) {
        loading.classList.add("hidden");

        itemCount.textContent = "Unable to load titles";

        showMessage(
            "Could not connect to the Flask API. Make sure Command Prompt #1 is running the server at http://127.0.0.1:5000",
            "error"
        );

        console.error(error);
    }
}


async function viewTitle(id) {
    try {
        const response = await fetch(`${API_URL}/titles/${id}`);

        if (!response.ok) {
            throw new Error("Title not found");
        }

        const title = await response.json();

        detailTitle.textContent = title.title;

        detailContent.innerHTML = `
            <div>
                <strong>Year</strong>
                <p>${title.year}</p>
            </div>

            <div>
                <strong>Type</strong>
                <p>${escapeHtml(title.type)}</p>
            </div>

            <div>
                <strong>Genre</strong>
                <p>${escapeHtml(title.genre)}</p>
            </div>

            <div>
                <strong>Rating</strong>
                <p>⭐ ${title.rating ?? "N/A"}</p>
            </div>

            <div>
                <strong>Creator</strong>
                <p>${title.creator ? escapeHtml(title.creator) : "N/A"}</p>
            </div>
        `;

        detailSection.classList.remove("hidden");
        detailSection.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        showMessage(error.message, "error");
    }
}


async function editTitle(id) {
    try {
        const response = await fetch(`${API_URL}/titles/${id}`);

        if (!response.ok) {
            throw new Error("Title not found");
        }

        const title = await response.json();

        editingId = id;

        formEyebrow.textContent = "Edit Title";
        formHeading.textContent = "Edit a Title";
        submitButton.textContent = "Save Changes";

        document.getElementById("title").value = title.title;
        document.getElementById("year").value = title.year;
        document.getElementById("type").value = title.type;
        document.getElementById("genre").value = title.genre;
        document.getElementById("rating").value = title.rating ?? "";
        document.getElementById("creator").value = title.creator ?? "";

        formError.classList.add("hidden");
        formSection.classList.remove("hidden");

        formSection.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        showMessage(error.message, "error");
    }
}


async function deleteTitle(id) {
    const confirmed = confirm(
        "Are you sure you want to delete this title?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/titles/${id}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Could not delete title");
        }

        showMessage("Title deleted successfully.", "success");

        await loadTitles();

    } catch (error) {
        showMessage(error.message, "error");
    }
}


function openAddForm() {
    editingId = null;

    titleForm.reset();

    formEyebrow.textContent = "New Title";
    formHeading.textContent = "Add a Title";
    submitButton.textContent = "Add Title";

    formError.classList.add("hidden");

    formSection.classList.remove("hidden");
    detailSection.classList.add("hidden");

    formSection.scrollIntoView({ behavior: "smooth" });
}


function closeForm() {
    formSection.classList.add("hidden");
    editingId = null;
}


function closeDetail() {
    detailSection.classList.add("hidden");
}


titleForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    formError.classList.add("hidden");

    const data = {
        title: document.getElementById("title").value.trim(),
        year: document.getElementById("year").value,
        type: document.getElementById("type").value,
        genre: document.getElementById("genre").value.trim(),
        rating: document.getElementById("rating").value || null,
        creator: document.getElementById("creator").value.trim() || null
    };

    if (!data.title || !data.year || !data.type || !data.genre) {
        formError.textContent =
            "Please fill in all required fields.";

        formError.classList.remove("hidden");
        return;
    }

    try {
        const url = editingId
            ? `${API_URL}/titles/${editingId}`
            : `${API_URL}/titles`;

        const method = editingId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Request failed");
        }

        closeForm();

        showMessage(
            editingId
                ? "Title updated successfully."
                : "Title added successfully.",
            "success"
        );

        await loadTitles();

    } catch (error) {
        formError.textContent = error.message;
        formError.classList.remove("hidden");
    }
});


function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type}`;

    setTimeout(() => {
        message.classList.add("hidden");
    }, 4000);
}


function escapeHtml(value) {
    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


document
    .getElementById("add-button")
    .addEventListener("click", openAddForm);

document
    .getElementById("cancel-form")
    .addEventListener("click", closeForm);

document
    .getElementById("cancel-form-button")
    .addEventListener("click", closeForm);

document
    .getElementById("close-detail")
    .addEventListener("click", closeDetail);


// Start the application
loadTitles();
