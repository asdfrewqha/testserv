document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");
    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault(); 

            let name = document.getElementById("username").value;
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;

            let userData = { name, email, password };

            try {
                let response = await fetch("/api/auth/sign-up", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData)
                });

                let data = await response.json();

                if (response.ok) {
                    alert("✅ Регистрация успешна! Ваш токен: " + data.token);
                    window.location.href = "/";
                } else {
                    alert("❌ Ошибка: " + data.message);
                }
            } catch (error) {
                console.error("Ошибка запроса:", error);
                alert("❌ Ошибка сервера. Попробуйте позже.");
            }
        });
    } else {
        console.warn("⚠️ Форма регистрации (#register-form) не найдена!");
    }

    // Форма авторизации
    const authForm = document.getElementById("auth-form");
    if (authForm) {
        authForm.addEventListener("submit", async function (event) {
            event.preventDefault(); 

            let login = document.getElementById("login").value;
            let password = document.getElementById("password").value;

            let userData = { login, password };

            try {
                let response = await fetch("/api/auth/sign-in", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData)
                });

                let data = await response.json();

                if (response.ok) {
                    alert("✅ Авторизация успешна! Ваш токен: " + data.token);
                    window.location.href = "/";
                } else {
                    alert("❌ Ошибка: " + data.message);
                }
            } catch (error) {
                console.error("Ошибка запроса:", error);
                alert("❌ Ошибка сервера. Попробуйте позже.");
            }
        });
    } else {
        console.warn("⚠️ Форма авторизации (#auth-form) не найдена!");
    }
});
