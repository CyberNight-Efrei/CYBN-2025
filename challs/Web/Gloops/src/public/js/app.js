let token = localStorage.getItem("token");

if (!token) {
  window.location.href = "/login";
}

if (token) {
  // Parse JWT
  const payload = JSON.parse(atob(token.split('.')[1]));
  if (payload.exp < Date.now() / 1000) {
    // Token expired
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

async function getOrganizations() {
  const response = await fetch('/api/organizations', {
    headers: {
      'Authorization': 'Bearer ' + token
    }
  });
  if (response.ok) {
    return await response.json();
  } else {
    console.error('Failed to fetch organizations:', response.statusText);
  }
}

async function getOrganization(id) {
  const response = await fetch(`/api/organizations/${id}`, {
    headers: {
      'Authorization': 'Bearer ' + token
    }
  });
  if (response.ok) {
    return await response.json();
  } else {
    console.error('Failed to fetch organization:', response.statusText);
  }
}

async function getAdminOrganizations() {
  const response = await fetch('/api/admin/organizations', {
    headers: {
      'Authorization': 'Bearer ' + token
    }
  });
  if (response.ok) {
    return await response.json();
  } else {
    console.error('Failed to fetch admin organizations:', response.statusText);
  }
}

async function getAdminOrganization(id) {
  const response = await fetch(`/api/admin/organizations/${id}`, {
    headers: {
      'Authorization': 'Bearer ' + token
    }
  });
  if (response.ok) {
    return await response.json();
  } else {
    console.error('Failed to fetch admin organization:', response.statusText);
  }
}

if (document.location.pathname === '/') {
  const cardsContainer = document.querySelector('.cards-container');
  getOrganizations().then(organizations => {
    organizations.forEach(element => {
      const card = document.createElement('a');
      card.classList.add('card');
      card.href = `/organizations/${element.id}`;
      card.innerHTML = `
        <p class="card-title">${element.name}</p>
        <p class="card-description">${element.publicDescription}</p>
      `;
      cardsContainer.appendChild(card);
    });
  });
}
else if (document.location.pathname.startsWith('/organizations/')) {
  const orgId = document.location.pathname.split('/')[2];
  getOrganization(orgId).then(organization => {
    if (organization) {
      document.querySelector('.main').innerHTML += `
        <div class="org-info">
          <h1>${organization.name}</h1>
          <p>${organization.publicDescription}</p>
        </div>
      `;
    }
  });
}
else if (document.location.pathname === '/admin/') {
  const cardsContainer = document.querySelector('.cards-container');
  getAdminOrganizations().then(organizations => {
    organizations.forEach(element => {
      const card = document.createElement('a');
      card.classList.add('card');
      card.href = `/admin/organizations/${element.id}`;
      card.innerHTML = `
        <p class="card-title">${element.name}</p>
        <p class="card-description">${element.internalDescription}</p>
      `;
      cardsContainer.appendChild(card);
    });
  });
}
else if (document.location.pathname.startsWith('/admin/organizations/')) {
  const orgId = document.location.pathname.split('/')[3];
  getAdminOrganization(orgId).then(organization => {
    if (organization) {
      document.querySelector('.main').innerHTML += `
        <div class="org-info">
          <h1>${organization.name}</h1>
          <p>${organization.internalDescription}</p>
        </div>
      `;
    }
  });
}

getAdminOrganizations().then(organizations => {
  if (organizations.length === 0) {
    document.querySelector('a[href="/admin"]').style.display = 'none';
  }
}).catch(error => {
  document.querySelector('a[href="/admin"]').style.display = 'none';
});