
async function login(event) {
    event.preventDefault();

        const loginData = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
    };

    const response = await fetch('http://localhost:8000/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: loginData.email, password: loginData.password }),
    });
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('isLoggedIn', true);
        localStorage.setItem('userId', data.userId); // Armazena o ID do usuário
        window.location.href = 'main.html';
    } else {
        alert('Credenciais inválidas');
    }
}

async function register(event) {
    event.preventDefault();

    const selectedInterests = [];
    const checkboxes = document.querySelectorAll('input[name="areasOfInterest"]:checked');
    checkboxes.forEach((checkbox) => {
        selectedInterests.push(checkbox.value);
    });

    const registerData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        userName: document.getElementById('userName').value,
        businessType: document.getElementById('businessType').value,
        businessDescription: document.getElementById('businessDescription').value,
        objectives: document.getElementById('objectives').value,
        areasOfInterest: selectedInterests
    };

    const response = await fetch('http://localhost:8000/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user: registerData }),
    });

    if (response.ok) {
        alert('Registrado com sucesso. Por favor, faça o login.');
        window.location.href = 'login.html';
    } else {
        alert('Erro ao fazer o registro.');
    }
}


async function getRecomendations() {
    // Supondo que o ID do usuário esteja armazenado no localStorage
    const userId = localStorage.getItem('userId');
    
    if (!userId) {
        alert('Você não está logado');
        return;
    }

    const response = await fetch(`http://localhost:8000/recomendations?userId=${userId}`);
    if (response.ok) {
        const data = await response.json();
        const recomendationsList = document.getElementById('recomendationsList');
        recomendationsList.innerHTML = ''; // Limpa a lista antes de adicionar novos itens
        data.recomendations.forEach(recomendation => {
            const item = document.createElement('li');
            item.className = 'list-group-item';
            item.textContent = `${recomendation.name}: ${recomendation.description} - ${recomendation.link}`;
            recomendationsList.appendChild(item);
        });
    } else {
        alert('Falha ao buscar recomendações');
    }
}


if (window.location.pathname.endsWith('main.html')) {
    getRecomendations();
}
