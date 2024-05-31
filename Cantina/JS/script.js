document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.querySelector('.login-btn');
    const logoutBtn = document.querySelector('.logout-btn');
    const foodSelectionScreen = document.getElementById('food-selection');
    const loginScreen = document.getElementById('login-screen');
    const loginSubmitBtn = document.querySelector('.login-submit');
    const foodList = document.getElementById('food-list');

    const foods = [
        {
            name: "Comida 1",
            description: "Descrição da Comida 1",
            image: "/food1.jpg"
        },
        {
            name: "Comida 2",
            description: "Descrição da Comida 2",
            image: "/food2.jpg"
        },
        // Adicione mais itens de comida conforme necessário
    ];

    function renderFoodItems() {
        foodList.innerHTML = '';
        foods.forEach(food => {
            const foodItem = document.createElement('div');
            foodItem.classList.add('food-item');

            foodItem.innerHTML = `
                <img src="${food.image}" alt="${food.name}" class="food-img">
                <div class="food-info">
                    <h3>${food.name}</h3>
                    <p>${food.description}</p>
                    <button class="btn add-to-cart">Adicionar ao Carrinho</button>
                </div>
            `;

            foodList.appendChild(foodItem);
        });
    }

    function showLoginScreen() {
        foodSelectionScreen.style.display = 'none';
        loginScreen.style.display = 'flex';
    }

    function redirectToLoginPage() {
        window.location.href = './HTML/login.html'; // Redireciona para a página login.html
    }

    function showFoodSelectionScreen() {
        foodSelectionScreen.style.display = 'flex';
        loginScreen.style.display = 'none';
    }

    loginBtn.addEventListener('click', () => {
        // showLoginScreen();
        redirectToLoginPage(); // Redireciona para a página de login ao clicar no botão de login
    });

    logoutBtn.addEventListener('click', () => {
        logoutBtn.style.display = 'none';
        loginBtn.style.display = 'block';
        showLoginScreen();
    });

    loginSubmitBtn.addEventListener('click', () => {
        // Simulate successful login
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'block';
        showFoodSelectionScreen();
    });

    renderFoodItems();

    const cart = document.querySelector('.cart-items');

    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('add-to-cart')) {
            const foodItem = event.target.closest('.food-item');
            const foodName = foodItem.querySelector('h3').innerText;
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerText = foodName;
            cart.appendChild(cartItem);
        }
    });
});
