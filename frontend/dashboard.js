const authToken = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
const userId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');
const userName = localStorage.getItem('user_name');
const userPhone = localStorage.getItem('user_phone');

if (!authToken || !userId) {
    window.location.replace('login.html');
}

history.pushState(null, null, location.href);
window.onpopstate = function() {
    history.go(1);
};

document.getElementById('userName').textContent = userName || userId;
document.getElementById('userId').textContent = userId;
document.getElementById('userPhone').textContent = userPhone;

document.getElementById('logoutBtn').addEventListener('click', function() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.replace('login.html');
});
