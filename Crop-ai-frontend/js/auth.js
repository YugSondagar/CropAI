// Backend API Base URL
const API_BASE_URL = 'http://127.0.0.1:8000';

class Auth {
    static init() {
        // Form submissions
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', Auth.handleLogin);
        }

        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', Auth.handleRegister);
        }
    }

    static async handleLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const loader = document.getElementById('loginLoader');
        const errorDiv = document.getElementById('errorMessage');
        const btnText = document.querySelector('#loginForm button span');

        btnText.style.display = 'none';
        loader.style.display = 'block';
        errorDiv.style.display = 'none';

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Success
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                // Error
                throw new Error(data.message || 'Login failed');
            }
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
        } finally {
            btnText.style.display = 'block';
            loader.style.display = 'none';
        }
    }

    static async handleRegister(e) {
        e.preventDefault();
        
        // Select elements
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const loader = document.getElementById('registerLoader');
        const errorDiv = document.getElementById('registerErrorMessage');
        const btnText = document.querySelector('#registerForm button span');

        // UI state: Start Loading
        if (btnText) btnText.style.display = 'none';
        if (loader) loader.style.display = 'block';
        if (errorDiv) errorDiv.style.display = 'none';

        try {
            console.log("Attempting to register at:", `${API_BASE_URL}/api/auth/register`);
            
            const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = 'login.html?registered=true';
            } else {
                throw new Error(data.message || 'Registration failed');
            }
        } catch (error) {
            console.error("Registration Error Details:", error); // This helps you debug!
            if (errorDiv) {
                errorDiv.textContent = "Error: " + error.message + ". Is your backend running on port 8000?";
                errorDiv.style.display = 'block';
            }
        } finally {
            // UI state: Stop Loading - THIS MUST RUN
            if (btnText) btnText.style.display = 'block';
            if (loader) loader.style.display = 'none';
        }
    }

    static logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }

    static isAuthenticated() {
        return !!localStorage.getItem('token');
    }

    static getToken() {
        return localStorage.getItem('token');
    }

    static getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
}

// Initialize Auth
document.addEventListener('DOMContentLoaded', Auth.init);
