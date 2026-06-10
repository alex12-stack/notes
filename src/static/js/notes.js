const notesList = document.getElementById("notes-list");
const noteForm = document.getElementById("note-form");
const searchInput = document.getElementById("search-input");
const reloadButton = document.getElementById("reload-notes");
const folderSelect = document.getElementById("folder-select");

let allNotes = [];
let foldersById = new Map();

async function loadFoldersForSelect() {
    if (!folderSelect) return;

    try {
        const folders = await apiFetch("/folders?page=1&per_page=100");
        foldersById = new Map((folders || []).map(folder => [Number(folder.id), folder]));

        folderSelect.innerHTML = '<option value="">Без папки</option>';
        for (const folder of folders || []) {
            const option = document.createElement("option");
            option.value = folder.id;
            option.textContent = folder.name || folder.title || `Папка ${folder.id}`;
            folderSelect.appendChild(option);
        }
    } catch (_) {
        folderSelect.innerHTML = '<option value="">Папки не загружены</option>';
    }
}

async function loadNotes() {
    notesList.innerHTML = '<p class="muted">Загрузка...</p>';

    try {
        allNotes = await apiFetch("/notes?page=1&per_page=100") || [];
        renderNotes();
    } catch (error) {
        notesList.innerHTML = `<p class="error-text">${escapeHtml(error.message)}</p>`;
    }
}

function getFilteredNotes() {
    const query = (searchInput?.value || "").trim().toLowerCase();
    if (!query) return allNotes;

    return allNotes.filter(note => {
        const title = String(note.title || "").toLowerCase();
        const content = String(note.content || "").toLowerCase();
        return title.includes(query) || content.includes(query);
    });
}

function renderNotes() {
    const notes = getFilteredNotes();

    if (!notes.length) {
        notesList.innerHTML = '<p class="muted">Заметок пока нет.</p>';
        return;
    }

    notesList.innerHTML = notes.map(note => {
        const folderName = note.folder_id && foldersById.has(Number(note.folder_id))
            ? foldersById.get(Number(note.folder_id)).name
            : "Без папки";

        return `
            <article class="card" data-note-id="${note.id}">
                <div class="card-head">
                    <input class="edit-title" value="${escapeHtml(note.title)}">
                    <span class="badge">${escapeHtml(folderName)}</span>
                </div>

                <textarea class="edit-content" rows="5">${escapeHtml(note.content)}</textarea>

                <label class="checkbox-row small-gap">
                    <input class="edit-public" type="checkbox" ${note.is_public ? "checked" : ""}>
                    Публичная
                </label>

                <div class="card-actions">
                    <button class="button secondary" data-action="save">Сохранить</button>
                    <button class="button danger" data-action="delete">Удалить</button>
                </div>
            </article>
        `;
    }).join("");
}

async function createNote(event) {
    event.preventDefault();

    const payload = formToObject(noteForm);
    payload.folder_id = payload.folder_id ? Number(payload.folder_id) : null;
    payload.is_public = Boolean(noteForm.elements.is_public.checked);

    try {
        await apiFetch("/notes", {
            method: "POST",
            body: JSON.stringify(payload),
        });
        noteForm.reset();
        showToast("Заметка добавлена");
        await loadNotes();
    } catch (error) {
        showToast(error.message, true);
    }
}

async function handleNoteAction(event) {
    const button = event.target.closest("button[data-action]");
    if (!button) return;

    const card = button.closest(".card");
    const noteId = card.dataset.noteId;
    const action = button.dataset.action;

    try {
        if (action === "delete") {
            await apiFetch(`/notes/${noteId}`, { method: "DELETE" });
            showToast("Заметка удалена");
            await loadNotes();
        }

        if (action === "save") {
            const payload = {
                title: card.querySelector(".edit-title").value,
                content: card.querySelector(".edit-content").value,
                is_public: card.querySelector(".edit-public").checked,
            };

            await apiFetch(`/notes/${noteId}`, {
                method: "PATCH",
                body: JSON.stringify(payload),
            });
            showToast("Заметка сохранена");
            await loadNotes();
        }
    } catch (error) {
        showToast(error.message, true);
    }
}

noteForm?.addEventListener("submit", createNote);
notesList?.addEventListener("click", handleNoteAction);
searchInput?.addEventListener("input", renderNotes);
reloadButton?.addEventListener("click", loadNotes);

document.addEventListener("DOMContentLoaded", async () => {
    await loadFoldersForSelect();
    await loadNotes();
});
