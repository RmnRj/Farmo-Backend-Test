const API_URL = 'http://localhost:8000/api/auth/login/';
const VERIFY_URL = 'http://localhost:8000/api/auth/verify-token/';

async function checkRememberedLogin() {
    const authToken = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
    const userId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');
    
    if (authToken && userId) {
        try {
            const response = await fetch(VERIFY_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ auth_token: authToken, user_id: userId })
            });
            
            const data = await response.json();
            if (data.valid) {
                localStorage.setItem('user_name', data.name);
                localStorage.setItem('user_phone', data.phone);
                window.location.replace('dashboard.html');
                return;
            } else {
                localStorage.clear();
                sessionStorage.clear();
            }
        } catch (error) {
            localStorage.clear();
            sessionStorage.clear();
        }
    }
}

checkRememberedLogin();

document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordField = document.getElementById('password');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
    this.textContent = type === 'password' ? 'Show' : 'Hide';
});

document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const identifier = document.getElementById('identifier').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identifier, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (rememberMe) {
                localStorage.setItem('auth_token', data.auth_token);
                localStorage.setItem('user_id', data.user_id);
            } else {
                sessionStorage.setItem('auth_token', data.auth_token);
                sessionStorage.setItem('user_id', data.user_id);
            }
            localStorage.setItem('user_name', data.name);
            localStorage.setItem('user_phone', data.phone);
            window.location.replace('dashboard.html');
        } else {
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        alert('Error connecting to server');
    }
});
