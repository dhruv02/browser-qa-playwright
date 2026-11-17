'use strict';

const products = [
  { id: 'p1', name: 'Wireless Mouse', category: 'Electronics', price: 24.99 },
  { id: 'p2', name: 'USB-C Cable', category: 'Electronics', price: 12.50 },
  { id: 'p3', name: 'Notebook', category: 'Stationery', price: 7.25 },
  { id: 'p4', name: 'Desk Lamp', category: 'Home', price: 39.00 },
];
const storageKey = 'demo-store-cart-v1';
const elements = {
  search: document.getElementById('search'),
  products: document.getElementById('products'),
  catalogCount: document.getElementById('catalog-count'),
  cartItems: document.getElementById('cart-items'),
  cartCount: document.getElementById('cart-count'),
  cartTotal: document.getElementById('cart-total'),
  clearCart: document.getElementById('clear-cart'),
  checkout: document.getElementById('checkout'),
  feedback: document.getElementById('feedback'),
};

function loadCart() {
  try {
    const raw = JSON.parse(localStorage.getItem(storageKey) || '{}');
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return {};
    const clean = {};
    for (const product of products) {
      const count = raw[product.id];
      if (Number.isInteger(count) && count > 0 && count <= 99) clean[product.id] = count;
    }
    return clean;
  } catch (_) { return {}; }
}
let cart = loadCart();
function money(cents) { return '$' + (cents / 100).toFixed(2); }
function notify(text, type) {
  elements.feedback.replaceChildren();
  const message = document.createElement('p');
  message.textContent = text;
  message.className = type;
  elements.feedback.append(message);
}
function saveCart() { localStorage.setItem(storageKey, JSON.stringify(cart)); }
function renderProducts() {
  const search = elements.search.value.trim().toLowerCase();
  const filtered = products.filter(p => `${p.name} ${p.category}`.toLowerCase().includes(search));
  elements.catalogCount.textContent = `${filtered.length} products found`;
  elements.products.replaceChildren();
  for (const p of filtered) {
    const article = document.createElement('article');
    article.className = 'product';
    article.dataset.productId = p.id;
    const title = document.createElement('h3'); title.textContent = p.name;
    const category = document.createElement('p'); category.textContent = p.category;
    const price = document.createElement('strong'); price.textContent = money(Math.round(p.price * 100));
    const wrap = document.createElement('p'); wrap.append(price);
    const button = document.createElement('button');
    button.textContent = `Add ${p.name} to cart`;
    button.addEventListener('click', () => {
      cart[p.id] = Math.min((cart[p.id] || 0) + 1, 99);
      saveCart(); renderCart(); notify(`${p.name} added to cart.`, 'success');
    });
    article.append(title, category, wrap, button);
    elements.products.append(article);
  }
}
function renderCart() {
  elements.cartItems.replaceChildren();
  let count = 0, totalCents = 0;
  for (const p of products) {
    const quantity = cart[p.id] || 0;
    if (!quantity) continue;
    count += quantity;
    totalCents += Math.round(p.price * 100) * quantity;
    const row = document.createElement('div'); row.className = 'cart-row';
    const label = document.createElement('span'); label.textContent = `${p.name} × ${quantity}`;
    const actions = document.createElement('div'); actions.className = 'actions';
    const minus = document.createElement('button'); minus.type = 'button'; minus.className = 'ghost';
    minus.textContent = '−'; minus.setAttribute('aria-label', `Decrease ${p.name}`);
    minus.addEventListener('click', () => { if (cart[p.id] <= 1) delete cart[p.id]; else cart[p.id] -= 1; saveCart(); renderCart(); });
    const plus = document.createElement('button'); plus.type = 'button'; plus.className = 'ghost';
    plus.textContent = '+'; plus.setAttribute('aria-label', `Increase ${p.name}`);
    plus.addEventListener('click', () => { cart[p.id] = Math.min(cart[p.id] + 1, 99); saveCart(); renderCart(); });
    actions.append(minus, plus); row.append(label, actions); elements.cartItems.append(row);
  }
  if (!count) {
    const empty = document.createElement('p'); empty.className = 'muted'; empty.textContent = 'Your cart is empty.';
    elements.cartItems.append(empty);
  }
  elements.cartCount.textContent = String(count);
  elements.cartTotal.textContent = money(totalCents);
  elements.clearCart.disabled = count === 0;
}
elements.search.addEventListener('input', renderProducts);
elements.clearCart.addEventListener('click', () => {
  cart = {}; saveCart(); renderCart(); notify('Cart cleared.', 'success');
});
elements.checkout.addEventListener('submit', event => {
  event.preventDefault();
  const name = document.getElementById('customer-name').value.trim();
  const email = document.getElementById('customer-email').value.trim();
  if (Object.values(cart).reduce((a, b) => a + b, 0) === 0) { notify('Add at least one item before checkout.', 'error'); return; }
  if (name.length < 2) { notify('Enter your full name (at least 2 characters).', 'error'); return; }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { notify('Enter a valid email address.', 'error'); return; }
  const count = Object.values(cart).reduce((a, b) => a + b, 0);
  notify(`Demo order placed for ${name}: ${count} item(s).`, 'success');
  cart = {}; saveCart(); renderCart(); elements.checkout.reset();
});
renderProducts(); renderCart();
