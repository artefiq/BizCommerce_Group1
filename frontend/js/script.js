(function($) {

  "use strict";

  var initPreloader = function() {
    $(document).ready(function($) {
    var Body = $('body');
        Body.addClass('preloader-site');
    });
    $(window).load(function() {
        $('.preloader-wrapper').fadeOut();
        $('body').removeClass('preloader-site');
    });
  }

  // init Chocolat light box
	var initChocolat = function() {
		Chocolat(document.querySelectorAll('.image-link'), {
		  imageSize: 'contain',
		  loop: true,
		})
	}

  var initSwiper = function() {

    var swiper = new Swiper(".main-swiper", {
      speed: 500,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    var bestselling_swiper = new Swiper(".bestselling-swiper", {
      slidesPerView: 4,
      spaceBetween: 30,
      speed: 500,
      breakpoints: {
        0: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 3,
        },
        991: {
          slidesPerView: 4,
        },
      }
    });

    var testimonial_swiper = new Swiper(".testimonial-swiper", {
      slidesPerView: 1,
      speed: 500,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    var products_swiper = new Swiper(".products-carousel", {
      slidesPerView: 4,
      spaceBetween: 30,
      speed: 500,
      breakpoints: {
        0: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 3,
        },
        991: {
          slidesPerView: 4,
        },

      }
    });

  }

  var initProductQty = function(){

    $('.product-qty').each(function(){

      var $el_product = $(this);
      var quantity = 0;

      $el_product.find('.quantity-right-plus').click(function(e){
          e.preventDefault();
          var quantity = parseInt($el_product.find('#quantity').val());
          $el_product.find('#quantity').val(quantity + 1);
      });

      $el_product.find('.quantity-left-minus').click(function(e){
          e.preventDefault();
          var quantity = parseInt($el_product.find('#quantity').val());
          if(quantity>0){
            $el_product.find('#quantity').val(quantity - 1);
          }
      });

    });

  }

  // init jarallax parallax
  var initJarallax = function() {
    jarallax(document.querySelectorAll(".jarallax"));

    jarallax(document.querySelectorAll(".jarallax-keep-img"), {
      keepImg: true,
    });
  }

  // document ready
  $(document).ready(function() {
    
    initPreloader();
    initSwiper();
    initProductQty();
    initJarallax();
    initChocolat();

        // product single page
        var thumb_slider = new Swiper(".product-thumbnail-slider", {
          spaceBetween: 8,
          slidesPerView: 3,
          freeMode: true,
          watchSlidesProgress: true,
        });
    
        var large_slider = new Swiper(".product-large-slider", {
          spaceBetween: 10,
          slidesPerView: 1,
          effect: 'fade',
          thumbs: {
            swiper: thumb_slider,
          },
        });

    window.addEventListener("load", (event) => {
      //isotope
      $('.isotope-container').isotope({
        // options
        itemSelector: '.item',
        layoutMode: 'masonry'
      });


      var $grid = $('.entry-container').isotope({
        itemSelector: '.entry-item',
        layoutMode: 'masonry'
      });


      // Initialize Isotope
      var $container = $('.isotope-container').isotope({
        // options
        itemSelector: '.item',
        layoutMode: 'masonry'
      });

      $(document).ready(function () {
        //active button
        $('.filter-button').click(function () {
          $('.filter-button').removeClass('active');
          $(this).addClass('active');
        });
      });

      // Filter items on button click
      $('.filter-button').click(function () {
        var filterValue = $(this).attr('data-filter');
        if (filterValue === '*') {
          // Show all items
          $container.isotope({ filter: '*' });
        } else {
          // Show filtered items
          $container.isotope({ filter: filterValue });
        }
      });

    });

  }); // End of a document

  // Fetch Produk List
function fetchProductList() {
  fetch('http://localhost:8000/produk/', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    const productList = document.getElementById('product-list');
    productList.innerHTML = ''; // Bersihkan konten sebelumnya

    data.forEach(item => {
      const productItem = document.createElement('div');
      productItem.classList.add('swiper-slide');
      productItem.innerHTML = `
        <div class="card position-relative">
          <a href="single-product.html?id=${item.id}"><img src="${item.gambar}" class="img-fluid rounded-4" alt="${item.nama}"></a>
          <div class="card-body p-0">
            <a href="single-product.html?id=${item.id}">
              <h3 class="card-title pt-4 m-0">${item.nama}</h3>
            </a>
            <div class="card-text">
              <span class="rating secondary-font">
                <iconify-icon icon="clarity:star-solid" class="text-primary"></iconify-icon>
                <iconify-icon icon="clarity:star-solid" class="text-primary"></iconify-icon>
                <iconify-icon icon="clarity:star-solid" class="text-primary"></iconify-icon>
                <iconify-icon icon="clarity:star-solid" class="text-primary"></iconify-icon>
                <iconify-icon icon="clarity:star-solid" class="text-primary"></iconify-icon>
                5.0
              </span>
              <h3 class="secondary-font text-primary">$${item.harga}</h3>
              <div class="d-flex flex-wrap mt-3">
                <a href="#" class="btn-cart me-3 px-4 pt-3 pb-3">
                  <h5 class="text-uppercase m-0">Add to Cart</h5>
                </a>
                <a href="#" class="btn-wishlist px-4 pt-3">
                  <iconify-icon icon="fluent:heart-28-filled" class="fs-5"></iconify-icon>
                </a>
              </div>
            </div>
          </div>
        </div>
      `;
      productList.appendChild(productItem);
    });
  })
  .catch(error => {
    console.error('There has been a problem with fetching the product list:', error);
  });
}

// Panggil fungsi saat halaman dimuat
document.addEventListener('DOMContentLoaded', fetchProductList);

})(jQuery);

// Quantity controls for cart items
function increaseQuantity(id) {
  const input = document.getElementById(id);
  input.value = parseInt(input.value) + 1;
  updateCartTotal(); // Add this if you want to automatically update the total
}

function decreaseQuantity(id) {
  const input = document.getElementById(id);
  if (input.value > 1) {
      input.value = parseInt(input.value) - 1;
      updateCartTotal(); // Add this if you want to automatically update the total
  }
}

// Optional: Function to update the cart total
function updateCartTotal() {
  const quantities = [
      { id: 'qty1', price: 12 },
      { id: 'qty2', price: 8 },
      { id: 'qty3', price: 5 }
  ];

  let total = 0;
  quantities.forEach(item => {
      const quantity = parseInt(document.getElementById(item.id).value);
      total += quantity * item.price;
  });

  // Update the total display
  document.querySelector('.list-group-item strong').textContent = `$${total}`;
}

// Optional: Add input event listeners to handle manual quantity changes
document.addEventListener('DOMContentLoaded', function() {
  const quantityInputs = document.querySelectorAll('input[type="number"]');
  quantityInputs.forEach(input => {
      input.addEventListener('change', function() {
          if (this.value < 1) this.value = 1;
          updateCartTotal();
      });
  });
});