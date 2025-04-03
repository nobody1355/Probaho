document.addEventListener('DOMContentLoaded', function () {
    const cartList = document.getElementById('selected-products-list');
    const cartTotalElement = document.getElementById('cart-total');
    const checkoutButton = document.getElementById('checkout-btn');
    const billModal = document.getElementById('bill-modal');
    const billItemsList = document.getElementById('bill-items-list');
    const billTotalElement = document.getElementById('bill-total');
    const paidAmountInput = document.getElementById('paid-amount');
    const changeField = document.getElementById('change');

    // Render cart from localStorage
    renderCartFromLocalStorage();

    // Helper function to update the total
    function updateCartTotal() {
        let total = 0;
        cartList.querySelectorAll('li').forEach(item => {
            total += parseFloat(item.getAttribute('data-product-price')) * 
                     parseInt(item.getAttribute('data-product-quantity'));
        });
        cartTotalElement.textContent = total.toFixed(2);
        return total;
    }

    // Handle paid amount and calculate change
    paidAmountInput.addEventListener('input', function () {
        const total = parseFloat(cartTotalElement.textContent) || 0;
        const paidAmount = parseFloat(paidAmountInput.value) || 0;

        // Calculate and update the change
        const change = Math.max(0, paidAmount - total);
        changeField.value = change.toFixed(2);
    });

    // Handle checkout button
    checkoutButton.addEventListener('click', function () {
        const total = parseFloat(cartTotalElement.textContent);
        const paidAmount = parseFloat(paidAmountInput.value);

        // Calculate change
        const change = paidAmount - total;

        // Show the bill modal and finalize the transaction
        billModal.style.display = 'block';
        billTotalElement.textContent = `Total: Tk ${total.toFixed(2)}`;
        billItemsList.innerHTML = '';

        // Populate bill items
        cartList.querySelectorAll('li').forEach(item => {
            const productName = item.getAttribute('data-product-name');
            const quantity = item.getAttribute('data-product-quantity');
            const price = item.getAttribute('data-product-price');

            const li = document.createElement('li');
            li.textContent = `${productName} - Qty: ${quantity} - Price: $${price}`;
            billItemsList.appendChild(li);
        });

        // Append Paid Amount and Change to the Receipt
        const paidAmountLi = document.createElement('li');
        paidAmountLi.textContent = `Paid Amount: Tk ${paidAmount.toFixed(2)}`;
        billItemsList.appendChild(paidAmountLi);

        const changeLi = document.createElement('li');
        changeLi.textContent = `Change: Tk ${change.toFixed(2)}`;
        billItemsList.appendChild(changeLi);
    });



    // Add to cart functionality
    document.querySelectorAll('.add-to-cart-btn').forEach((button) => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            const price = parseFloat(this.getAttribute('data-price'));
            const quantityInput = document.getElementById(`quantity_${productId}`);
            const quantity = parseInt(quantityInput.value) || 0;
    
            if (quantity < 1) {
                alert('Please enter a valid quantity.');
                return;
            }
    
            let existingItem = cartList.querySelector(`li[data-product-id="${productId}"]`);
    
            if (existingItem) {
                // Replace the existing item's quantity with the new one
                existingItem.setAttribute('data-product-quantity', quantity);
                existingItem.querySelector('.item-details').textContent = `${productName} - ${quantity} x Tk ${price}`;
                updateCartInLocalStorage(productId, quantity); // Update localStorage
            } else {
                // Add new item to the cart
                const cartItem = document.createElement('li');
                cartItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');
                cartItem.setAttribute('data-product-id', productId);
                cartItem.setAttribute('data-product-quantity', quantity);
                cartItem.setAttribute('data-product-price', price);
    
                cartItem.innerHTML = `
                    <span class="item-details">${productName} - ${quantity} x Tk ${price}</span>
                    <button class="btn btn-danger btn-sm remove-btn">Remove</button>
                `;
    
                cartList.appendChild(cartItem);
    
                // Add remove functionality
                cartItem.querySelector('.remove-btn').addEventListener('click', function () {
                    cartItem.remove();
                    updateCartTotal();
                    removeFromLocalStorage(productId); // Remove from localStorage
                });

                saveToLocalStorage(productId, productName, price, quantity); // Save new item to localStorage
            }
    
            updateCartTotal();
        });
    });

    // Checkout functionality
    checkoutButton.addEventListener('click', function () {
        if (cartList.children.length === 0) {
            alert('Your cart is empty. Please add items to proceed.');
            return;
        }

        billItemsList.innerHTML = '';
        cartList.querySelectorAll('li').forEach((item) => {
            const productName = item.querySelector('.item-details').textContent;
            const quantity = item.getAttribute('data-product-quantity');
            const price = item.getAttribute('data-product-price');
            const total = (quantity * price).toFixed(2);

            const billItem = document.createElement('li');
            billItem.classList.add('list-group-item', 'd-flex', 'justify-content-between');
            billItem.innerHTML = `
                <span>${productName}</span>
                <span>Tk ${total}</span>
            `;
            billItemsList.appendChild(billItem);
        });

        billTotalElement.textContent = cartTotalElement.textContent;
        billModal.style.display = 'block';
    });

    // Confirm functionality
    document.getElementById('print-bill-btn').addEventListener('click', function () {
        alert('Purchase confirmed successfully!');
        billModal.style.display = 'none';
        cartList.innerHTML = '';
        cartTotalElement.textContent = '0.00';
        clearLocalStorage(); // Optionally clear localStorage after checkout
    });

    // Close modal functionality
    document.getElementById('close-bill-btn').addEventListener('click', function () {
        billModal.style.display = 'none';
    });

    // Save new item to localStorage
    function saveToLocalStorage(productId, productName, price, quantity) {
        let cart = getCartFromLocalStorage();
        cart.push({ productId, productName, price, quantity });
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Get cart data from localStorage
    function getCartFromLocalStorage() {
        let cart = localStorage.getItem('cart');
        return cart ? JSON.parse(cart) : [];
    }

    // Update item in localStorage
    function updateCartInLocalStorage(productId, quantity) {
        let cart = getCartFromLocalStorage();
        let product = cart.find(item => item.productId === productId);
        if (product) {
            product.quantity = quantity;
            localStorage.setItem('cart', JSON.stringify(cart));
        }
    }

    // Remove item from localStorage
    function removeFromLocalStorage(productId) {
        let cart = getCartFromLocalStorage();
        cart = cart.filter(item => item.productId !== productId);
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Clear all items from localStorage
    function clearLocalStorage() {
        localStorage.removeItem('cart');
    }

    // Render cart items from localStorage
    function renderCartFromLocalStorage() {
        const cart = getCartFromLocalStorage();
        cart.forEach(item => {
            const cartItem = document.createElement('li');
            cartItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');
            cartItem.setAttribute('data-product-id', item.productId);
            cartItem.setAttribute('data-product-quantity', item.quantity);
            cartItem.setAttribute('data-product-price', item.price);

            cartItem.innerHTML = `
                <span class="item-details">${item.productName} - ${item.quantity} x Tk ${item.price}</span>
                <button class="btn btn-danger btn-sm remove-btn">Remove</button>
            `;

            cartList.appendChild(cartItem);

            // Add remove functionality
            cartItem.querySelector('.remove-btn').addEventListener('click', function () {
                cartItem.remove();
                updateCartTotal();
                removeFromLocalStorage(item.productId); // Remove from localStorage
            });
        });

        updateCartTotal();
    }
});
