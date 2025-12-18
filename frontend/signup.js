const API_URL = 'http://localhost:8000/api/auth/signup/';

document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordField = document.getElementById('password');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
    this.textContent = type === 'password' ? 'Show' : 'Hide';
});

document.getElementById('signupForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        user_id: document.getElementById('user_id').value,
        profile_id: document.getElementById('profile_id').value,
        f_name: document.getElementById('f_name').value,
        l_name: document.getElementById('l_name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        user_type: document.getElementById('user_type').value,
        password: document.getElementById('password').value
    };
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Account created successfully! Please login.');
            window.location.href = 'login.html';
        } else {
            alert(JSON.stringify(data));
        }
    } catch (error) {
        alert('Error connecting to server');
    }
});
