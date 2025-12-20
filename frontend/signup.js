const API_URL = 'http://localhost:8000/api/auth/register/';

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
    for(let i = 1; i <= step; i++) {
        document.getElementById('step' + i + '-indicator').classList.add('active');
    }
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
    
    const formData = new FormData();
    formData.append('user_id', document.getElementById('user_id').value);
    formData.append('password', document.getElementById('password').value);
    formData.append('user_type', document.getElementById('user_type').value);
    formData.append('f_name', document.getElementById('f_name').value);
    formData.append('m_name', document.getElementById('m_name').value);
    formData.append('l_name', document.getElementById('l_name').value);
    formData.append('dob', document.getElementById('dob').value);
    formData.append('sex', document.getElementById('sex').value);
    formData.append('about', document.getElementById('about').value);
    formData.append('province', document.getElementById('province').value);
    formData.append('district', document.getElementById('district').value);
    formData.append('ward', document.getElementById('ward').value);
    formData.append('tole', document.getElementById('tole').value);
    formData.append('phone', document.getElementById('phone').value);
    formData.append('phone2', document.getElementById('phone2').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('whatsapp', document.getElementById('whatsapp').value);
    formData.append('facebook', document.getElementById('facebook').value);
    
    const profilePicture = document.getElementById('profile_picture').files[0];
    if (profilePicture) {
        formData.append('profile_picture', profilePicture);
    }
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('User registered successfully! Please login.');
            window.location.href = 'login.html';
        } else {
            alert('Error: ' + (data.error || JSON.stringify(data)));
        }
    } catch (error) {
        alert('Error connecting to server: ' + error.message);
    }
});
