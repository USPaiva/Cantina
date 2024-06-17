document.addEventListener('DOMContentLoaded', () => {
    const cartItemsContainer = document.querySelector('.cart-items');
    const totalValueElement = document.querySelector('.total-value');

    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    let totalValue = 0;

    cart.forEach(item => {
        totalValue += parseFloat(item.price) * item.quantity;
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = 
            `<img src="${item.photo}" alt="${item.name}" class="cart-item-image">
            <p>${item.name} - R$ ${item.price} (Quantidade: ${item.quantity})</p>`;
        cartItemsContainer.appendChild(cartItem);
    });

    totalValueElement.textContent = `Valor Total: R$ ${totalValue.toFixed(2)}`;

    const finalizeOrderForm = document.getElementById('finalize-order-form');

    finalizeOrderForm.addEventListener('submit', (event) => {
        event.preventDefault();

        // Obter os valores dos campos
        const pickupDate = document.getElementById('pickup-date').value;
        const pickupTime = document.getElementById('pickup-time').value;
        const paymentMethod = document.getElementById('payment-method').value;

        console.log('Pickup Date:', pickupDate);
        console.log('Pickup Time:', pickupTime);
        console.log('Payment Method:', paymentMethod);

        if (pickupDate && pickupTime && paymentMethod) {
            // Adicionar o carrinho ao formulário como um campo oculto
            const cartInput = document.createElement('input');
            cartInput.type = 'hidden';
            cartInput.name = 'cart';
            cartInput.value = JSON.stringify(cart);
            finalizeOrderForm.appendChild(cartInput);

            // Submeter o formulário
            finalizeOrderForm.submit();
        } else {
            alert('Por favor, preencha todos os campos obrigatórios.');
        }
    });
});