const folderForm = document.getElementById("folder-form");
const foldersList = document.getElementById("folders-list");

let allFolders = [];

async function loadFolders() {
    foldersList.innerHTML = '<p class="muted">Загрузка...</p>';

    try {
        allFolders = await apiFetch("/folders?page=1&per_page=100") || [];
        renderFolders();
    } catch (error) {
        foldersList.innerHTML = `<p class="error-text">${escapeHtml(error.message)}</p>`;
    }
}

function renderFolders() {
    if (!allFolders.length) {
        foldersList.innerHTML = '<p class="muted">Папок пока нет.</p>';
        return;
    }

    foldersList.innerHTML = allFolders.map(folder => `
        <article class="card folder-card" data-folder-id="${folder.id}">
            <input class="edit-folder-name" value="${escapeHtml(folder.name)}">
            <div class="card-actions">
                <button class="button secondary" data-action="save">Сохранить</button>
                <button class="button danger" data-action="delete">Удалить</button>
            </div>
        </article>
    `).join("");
}

async function createFolder(event) {
    event.preventDefault();

    const submitButton = folderForm.querySelector('button[type="submit"]');

    if (submitButton.disabled) return;

    submitButton.disabled = true;

    const payload = formToObject(folderForm);
    const name = payload.name.trim();

    try {
        if (!name) {
            throw new Error("Название папки не может быть пустым");
        }

        await apiFetch("/folders", {
            method: "POST",
            body: JSON.stringify({ name }),
        });

        folderForm.reset();
        showToast("Папка добавлена");
        await loadFolders();
    } catch (error) {
        showToast(error.message, true);
    } finally {
        submitButton.disabled = false;
    }
}

async function handleFolderAction(event) {
    const button = event.target.closest("button[data-action]");
    if (!button || button.disabled) return;

    const card = button.closest(".card");
    const folderId = card.dataset.folderId;
    const action = button.dataset.action;

    const actionButtons = card.querySelectorAll("button[data-action]");

    actionButtons.forEach(item => {
        item.disabled = true;
    });

    try {
        if (action === "delete") {
            const result = await apiFetch(`/folders/${folderId}`, {
                method: "DELETE",
            });

            const movedNotesCount = Number(result?.moved_notes_count || 0);
            const message = movedNotesCount > 0
                ? `Папка удалена. Заметки без папки: ${movedNotesCount}`
                : "Папка удалена";

            showToast(message);
            await loadFolders();
            return;
        }

        if (action === "save") {
            const name = card
                .querySelector(".edit-folder-name")
                .value
                .trim();

            if (!name) {
                throw new Error("Название папки не может быть пустым");
            }

            await apiFetch(`/folders/${folderId}`, {
                method: "PATCH",
                body: JSON.stringify({ name }),
            });

            showToast("Папка сохранена");
            await loadFolders();
        }
    } catch (error) {
        showToast(error.message, true);

        actionButtons.forEach(item => {
            item.disabled = false;
        });
    }
}

folderForm?.addEventListener("submit", createFolder);
foldersList?.addEventListener("click", handleFolderAction);
document.addEventListener("DOMContentLoaded", loadFolders);
