function showToast(message, isError = false) {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.textContent = message;
    toast.className = isError ? "toast toast-error" : "toast";
    toast.hidden = false;

    setTimeout(() => {
        toast.hidden = true;
    }, 3500);
}

function formatApiError(data) {
    const detail = data?.detail || data || "Ошибка запроса";

    if (Array.isArray(detail)) {
        return detail
            .map(item => {
                const field = Array.isArray(item.loc) ? item.loc.at(-1) : null;
                return field ? `${field}: ${item.msg}` : item.msg || String(item);
            })
            .join("; ");
    }

    return String(detail);
}

async function apiFetch(path, options = {}) {
    const headers = new Headers(options.headers || {});

    if (options.body && !(options.body instanceof FormData) && !headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
    }

    const response = await fetch(path, {
        ...options,
        headers,
        credentials: "same-origin",
    });

    const text = await response.text();
    let data = null;

    if (text) {
        try {
            data = JSON.parse(text);
        } catch {
            data = text;
        }
    }

    if (!response.ok) {
        const isAuthRequest = path.startsWith("/auth/login") || path.startsWith("/auth/register");

        if (response.status === 401 && !isAuthRequest) {
            window.location.href = "/app/login";
        }

        throw new Error(formatApiError(data));
    }

    return data;
}

function formToObject(form) {
    return Object.fromEntries(new FormData(form).entries());
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

const logoutButton = document.getElementById("logout-button");

logoutButton?.addEventListener("click", async () => {
    try {
        await apiFetch("/auth/logout", { method: "POST" });
    } finally {
        window.location.href = "/app/login";
    }
});
