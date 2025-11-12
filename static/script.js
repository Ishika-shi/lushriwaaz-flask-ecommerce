// ---------- Modal Quick View ----------
const modal = document.getElementById('product-modal');
const closeBtn = document.querySelector('.close');
const modalImg = document.getElementById('modal-img');
const modalTitle = document.getElementById('modal-title');
const modalDesc = document.getElementById('modal-desc');
const modalPrice = document.getElementById('modal-price');
const modalAddBtn = document.getElementById('modal-add');

document.addEventListener('click', function (e) {
  // Product image click opens modal
  if (e.target.closest('.product-card img')) {
    const card = e.target.closest('.product-card');
    modalImg.src = card.querySelector('img').src;
    modalTitle.textContent = card.querySelector('h3').textContent;
    modalDesc.textContent = card.querySelector('p').textContent;
    modalPrice.textContent = card.querySelector('.price').textContent;
    modalAddBtn.dataset.id = card.querySelector('.add-to-cart').dataset.id;
    modal.classList.remove('hidden');
  }

  // Add-to-cart button click
  if (e.target.classList.contains('add-to-cart') || e.target.id === 'modal-add') {
    const id = e.target.dataset.id;
    fetch('/add_to_cart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: id, quantity: 1 })
    })
      .then(res => {
        if (res.status === 401) {
          alert('Please login first.');
          window.location.href = '/login';
          return;
        }
        return res.json();
      })
      .then(data => {
        if (data && data.status === 'ok') alert('✅ Added to cart');
      })
      .catch(err => console.error(err));
  }

  // Close modal
  if (e.target === closeBtn || e.target === modal) modal.classList.add('hidden');
});
