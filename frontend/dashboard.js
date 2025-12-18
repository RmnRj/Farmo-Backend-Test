const user = JSON.parse(localStorage.getItem('user'));

if (!user) {
    window.location.href = 'login.html';
}

document.getElementById('userName').textContent = user.user_id;
document.getElementById('userId').textContent = user.user_id;
document.getElementById('userPhone').textContent = user.phone;

document.getElementById('logoutBtn').addEventListener('click', function() {
    localStorage.clear();
    window.location.href = 'login.html';
});
