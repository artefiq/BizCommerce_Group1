// open cart modal
const cart = document.querySelector('#cart');
const cartModalOverlay = document.querySelector('.cart-modal-overlay');

cart.addEventListener('click', () => {
  if (cartModalOverlay.style.transform === 'translateX(-200%)') {
    cartModalOverlay.style.transform = 'translateX(0)';
  } else {
    cartModalOverlay.style.transform = 'translateX(-200%)';
  }
});
// end of open cart modal

// close cart modal
const closeBtn = document.querySelector('#close-btn');

closeBtn.addEventListener('click', () => {
  cartModalOverlay.style.transform = 'translateX(-200%)';
});

cartModalOverlay.addEventListener('click', (e) => {
  if (e.target.classList.contains('cart-modal-overlay')) {
    cartModalOverlay.style.transform = 'translateX(-200%)';
  }
});
// end of close cart modal

// add products to cart
const addToCart = document.getElementsByClassName('add-to-cart');
const productRows = document.getElementsByClassName('product-row');

for (let i = 0; i < addToCart.length; i++) {
  const button = addToCart[i];
  button.addEventListener('click', addToCartClicked);
}

function addToCartClicked(event) {
  const button = event.target;
  const cartItem = button.parentElement;
  const price = cartItem.getElementsByClassName('product-price')[0].innerText;
  const imageSrc = cartItem.getElementsByClassName('product-image')[0].src;
  const description = cartItem.getElementsByClassName('product-description')[0].innerText;

  addItemToCart(price, imageSrc, description);
  updateCartPrice();
}

function addItemToCart(price, imageSrc, description) {
  const productRow = document.createElement('div');
  productRow.classList.add('product-row');
  const productRowsContainer = document.getElementsByClassName('product-rows')[0];
  const cartImages = document.getElementsByClassName('cart-image');

  for (let i = 0; i < cartImages.length; i++) {
    if (cartImages[i].src === imageSrc) {
      alert('This item has already been added to the cart');
      return;
    }
  }

  const cartRowItems = `
    <div class="product-row">
      <img class="cart-image" src="${imageSrc}" alt="">
      <span class="cart-description">${description}</span>
      <span class="cart-price">${price}</span>
      <input class="product-quantity" type="number" value="1">
      <button class="remove-btn">Remove</button>
    </div>
  `;

  productRow.innerHTML = cartRowItems;
  productRowsContainer.append(productRow);

  productRow.getElementsByClassName('remove-btn')[0].addEventListener('click', removeItem);
  productRow.getElementsByClassName('product-quantity')[0].addEventListener('change', changeQuantity);
  updateCartPrice();
}
// end of add products to cart

// Remove products from cart
const removeBtn = document.getElementsByClassName('remove-btn');
for (let i = 0; i < removeBtn.length; i++) {
  const button = removeBtn[i];
  button.addEventListener('click', removeItem);
}

function removeItem(event) {
  const btnClicked = event.target;
  btnClicked.parentElement.parentElement.remove();
  updateCartPrice();
}

// update quantity input
const quantityInputs = document.getElementsByClassName('product-quantity');

for (let i = 0; i < quantityInputs.length; i++) {
  const input = quantityInputs[i];
  input.addEventListener('change', changeQuantity);
}

function changeQuantity(event) {
  const input = event.target;
  if (isNaN(input.value) || input.value <= 0) {
    input.value = 1;
  }
  updateCartPrice();
}
// end of update quantity input

// update total price
function updateCartPrice() {
  let total = 0;
  for (let i = 0; i < productRows.length; i++) {
    const cartRow = productRows[i];
    const priceElement = cartRow.getElementsByClassName('cart-price')[0];
    const quantityElement = cartRow.getElementsByClassName('product-quantity')[0];
    const price = parseFloat(priceElement.innerText.replace('$', ''));
    const quantity = quantityElement.value;

    total += price * quantity;
  }

  document.getElementsByClassName('total-price')[0].innerText = '$' + total.toFixed(2);
  document.getElementsByClassName('cart-quantity')[0].textContent = productRows.length;
}
// end of update total price

// purchase items
const purchaseBtn = document.querySelector('.purchase-btn');

purchaseBtn.addEventListener('click', purchaseBtnClicked);

function purchaseBtnClicked() {
  alert('Thank you for your purchase');
  cartModalOverlay.style.transform = 'translateX(-200%)';
  const cartItems = document.getElementsByClassName('product-rows')[0];

  while (cartItems.hasChildNodes()) {
    cartItems.removeChild(cartItems.firstChild);
  }

  updateCartPrice();
}
// end of purchase items
