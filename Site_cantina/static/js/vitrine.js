document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];

    const updateCart = () => {
        const cartItemsContainer = document.querySelector('.cart-items');
        cartItemsContainer.innerHTML = '';
        console.log('Atualizando carrinho:');

        let totalValue = 0;

        cart.forEach((item, index) => {
            console.log(`Adicionando item ao carrinho: ${item.name} - ${item.price}`);
            totalValue += parseFloat(item.price) * item.quantity; // Multiplicar o preço pela quantidade
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `
                <img src="${item.photo}" alt="${item.name}" class="cart-item-image">
                <p>${item.name} - R$ ${item.price} (Quantidade: ${item.quantity})</p>
                <button class="btn remove-from-cart" data-index="${index}">Remover</button>
            `;
            cartItemsContainer.appendChild(cartItem);
        });

        // Adicionar event listeners para os botões de remoção
        document.querySelectorAll('.remove-from-cart').forEach(button => {
            button.addEventListener('click', function () {
                const itemIndex = this.getAttribute('data-index');
                cart.splice(itemIndex, 1);
                updateCart();
            });
        });

        // Atualizar o valor total do pedido
        const totalValueElement = document.querySelector('.total-value');
        totalValueElement.textContent = `Valor Total: R$ ${totalValue.toFixed(2)}`;

        // Salvar carrinho atualizado no localStorage
        localStorage.setItem('cart', JSON.stringify(cart));
    };

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-id');
            const productName = this.parentElement.parentElement.querySelector('td:nth-child(2)').textContent;
            const productDescription = this.parentElement.parentElement.querySelector('td:nth-child(3)').textContent;
            const productPrice = this.parentElement.parentElement.querySelector('td:nth-child(4)').textContent;
            const productPhoto = this.parentElement.parentElement.querySelector('td:nth-child(1) img').getAttribute('src');

            const existingProductIndex = cart.findIndex(item => item.id === productId);

            if (existingProductIndex >= 0) {
                // Se o produto já está no carrinho, incrementa a quantidade
                cart[existingProductIndex].quantity += 1;
            } else {
                // Caso contrário, adiciona o produto ao carrinho com quantidade 1
                const product = { id: productId, name: productName, description: productDescription, price: productPrice, photo: productPhoto, quantity: 1 };
                cart.push(product);
            }

            console.log('Carrinho Atual:', cart); // Log para depuração
            updateCart();
        });
    });

    // Adicionar event listener para o botão de finalizar pedido
    const finalizeButton = document.querySelector('.checkout');
    if (finalizeButton) {
        finalizeButton.addEventListener('click', () => {
            // Construir a URL com os parâmetros do carrinho
            let cartParams = cart.map(item => `product_id=${item.id}&name=${encodeURIComponent(item.name)}&price=${item.price}&quantity=${item.quantity}`).join('&');

            // Redirecionar para a página de finalizar pedido com os parâmetros do carrinho
            window.location.href = `/finalizar_pedido?${cartParams}`;
        });
    }

    // Inicializar o carrinho ao carregar a página
    updateCart();
});