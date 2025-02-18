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
                    alert("Registration completed!");
                    window.location.href = "/";
                } else {
                    alert("Error: " + data.message);
                }
            } catch (error) {
                console.error("Bad request: ", error);
                alert("Internal server error, please try again later.");
            }
        });
    } else {
        console.warn("missing register-from.");
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
                    alert("Authorization completed!");
                    window.location.href = "/";
                } else {
                    alert("Error: " + data.message);
                }
            } catch (error) {
                console.error("Bad request: ", error);
                alert("Internal server error, please try again later.");
            }
        });
    } else {
        console.warn("missing auth-form.");
    }
});
