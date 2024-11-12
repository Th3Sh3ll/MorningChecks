document.querySelector('.login-form').addEventListener('submit', function(e) {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!email || !password) {
        alert('Please fill out both fields.');
        e.preventDefault();
    }
});
