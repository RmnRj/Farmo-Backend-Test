const API_URL = 'http://localhost:8000/api/auth/signup/';

document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordField = document.getElementById('password');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
    this.textContent = type === 'password' ? 'Show' : 'Hide';
});

function nextStep(step) {
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    
    document.getElementById('step' + step).classList.add('active');
    document.getElementById('step' + step + '-indicator').classList.add('active');
}

function prevStep(step) {
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    
    document.getElementById('step' + step).classList.add('active');
    for(let i = 1; i <= step; i++) {
        document.getElementById('step' + i + '-indicator').classList.add('active');
    }
}

document.getElementById('signupForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        user_id: document.getElementById('user_id').value,
        f_name: document.getElementById('f_name').value,
        m_name: document.getElementById('m_name').value,
        l_name: document.getElementById('l_name').value,
        user_type: document.getElementById('user_type').value,
        password: document.getElementById('password').value,
        province: document.getElementById('province').value,
        district: document.getElementById('district').value,
        ward: document.getElementById('ward').value,
        tole: document.getElementById('tole').value,
        phone: document.getElementById('phone').value,
        phone02: document.getElementById('phone02').value,
        email: document.getElementById('email').value,
        whatsapp: document.getElementById('whatsapp').value,
        facebook: document.getElementById('facebook').value
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
