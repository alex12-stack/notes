const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

async function login(email, password) {
    return await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
    });
}

loginForm?.addEventListener("submit", async event => {
    event.preventDefault();

    const payload = formToObject(loginForm);

    try {
        await login(payload.email, payload.password);
        window.location.href = "/app/notes";
    } catch (error) {
        showToast(error.message, true);
    }
});

registerForm?.addEventListener("submit", async event => {
    event.preventDefault();

    const payload = formToObject(registerForm);

    try {
        await apiFetch("/auth/register", {
            method: "POST",
            body: JSON.stringify(payload),
        });

        await login(payload.email, payload.password);
        window.location.href = "/app/notes";
    } catch (error) {
        showToast(error.message, true);
    }
});
