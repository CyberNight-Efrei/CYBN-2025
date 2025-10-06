let token = localStorage.getItem("token");

if (token) {
  window.location.href = '/';
}

const usernameField = document.querySelector('#login');
const passwordField = document.querySelector('#password');
const loginBtn = document.querySelector('.login-btn-container button');

async function makeLogin() {
  const username = usernameField.value;
  const password = passwordField.value;

  const response = await fetch('/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ login: username, password })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem("token", data.token);
    window.location.href = '/';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

loginBtn.addEventListener('click', makeLogin);
usernameField.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    makeLogin();
  }
});
passwordField.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    makeLogin();
  }
});
