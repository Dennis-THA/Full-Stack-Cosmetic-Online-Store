const triggerOpen = document.querySelectorAll('[trigger-button]');
const triggerClose = document.querySelectorAll('[close-button]');
const overlay = document.querySelector('[data-overlay]');
const csrfToken = '{{ csrf_token }}'; 
const MEDIA_URL = "{{ MEDIA_URL }}"; 

for (let i = 0; i < triggerOpen.length; i++) {
    let currentId = triggerOpen[i].dataset.target,
    targetEl = document.querySelector(`#${currentId}`)

    const openData = function() {
        targetEl.classList.remove('active');
        overlay.classList.remove('active');
    };
    triggerOpen[i].addEventListener('click', function() {
        targetEl.classList.add('active');
        overlay.classList.add('active');
    });

    targetEl.querySelector('[close-button]').addEventListener('click', openData);
    overlay.addEventListener('click', openData);
}

//mobile-menu submenu
const submenu = document.querySelectorAll('.child-trigger');
submenu.forEach((menu) => menu.addEventListener('click', function(e) {
    e.preventDefault();
    submenu.forEach((item) => item != this ? item.closest('.has-child').classList.remove('active') : null);
    if(this.closest('.has-child').classList != 'active') {
        this.closest('.has-child').classList.toggle('active');
    }
}))




//Sorter

const sorter = document.querySelector('.sort-list');
if(sorter) {
    const sortLi = sorter.querySelectorAll('li');
    sorter.querySelector('.opt-trigger').addEventListener('click', function() {
        sorter.querySelector('ul').classList.toggle('show')
    });
    sortLi.forEach((item) => item.addEventListener('click', function() {
        sortLi.forEach((li) => li != this ? li.classList.remove('active') : null);

        this.classList.add('active');
        sorter.querySelector('.opt-trigger span.value').textContent = this.textContent;
        sorter.querySelector('ul').classList.toggle('show')
    }))

}

//Tabbed

const trigger = document.querySelectorAll('.tabbed-trigger'),
    content = document.querySelectorAll('.tabbed > div');
trigger.forEach((btn) => {
    btn.addEventListener('click', function() {
        let dataTarget = this.dataset.id,
        body = document.querySelector(`#${dataTarget}`);

        // Remove active class from all triggers and content
        trigger.forEach((b) => b.parentNode.classList.remove('active'));
        content.forEach((s) => s.classList.remove('active'));

        // Add active class to the clicked trigger and the corresponding content
        this.parentNode.classList.add('active');
        body.classList.add('active');
    });
});







//SLIDER

const swiper = new Swiper('.sliderbox', {

    loop: true,
    effect: 'fade',
    autoHeight: true,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  
    // // Navigation arrows
    // navigation: {
    //   nextEl: '.swiper-button-next',
    //   prevEl: '.swiper-button-prev',
    // },
  
    // // And if we need scrollbar
    // scrollbar: {
    //   el: '.swiper-scrollbar',
    // },
  });

  //Arrival

  const arrivals = new Swiper('.arrivalbox', {

    spaceBetween: 30,
    slidesPerView: 'auto',
    centeredSlides: true,
  
    // If we need pagination
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        481: {
            slidesPerView: 2,
            slidesPerGroup: 1,
            centeredSlides: false,
        },
        640: {
            slidesPerView: 3,
            slidesPerGroup: 3,
            centeredSlides: false,
        },
        992: {
            slidesPerView:4,
            slidesPerGroup: 4,
            centeredSlides: false,
        }
    }
  });


// product image > product page

const thumbImage = new Swiper('.thumbnail-image', {

    // loop: true,
    direction: 'vertical',
    spaceBetween: 15,
    slidesPerView: 1,
    freeMode: true,
    watchSlidesProgress: true,
  
});

const mainImage = new Swiper('.main-image', {

    loop: true,
    autoHeight: true,

    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    thumbs: {
        swiper: thumbImage,
    },
  
});


// Cart

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('addToCartButton').addEventListener('click', function () {
        var itemId = this.getAttribute('data-item-id');
        fetch(`/add-to-cart/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ quantity: 1 })
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/cart/';
            } else {
                alert('Failed to add item to cart');
            }
        });
    });
});

function getProductDetailUrl(itemId) {
    return `/product/${itemId}/`;
}

// Function to handle search results display
function displaySearchResults(items) {
    const searchResultsContainer = document.getElementById('search-results');
    searchResultsContainer.innerHTML = ''; // Clear previous results

    items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.innerHTML = `
            <a href="${getProductDetailUrl(item.id)}">
                <img src="${item.image}" alt="${item.title}">
                <span>${item.title}</span>
            </a>
        `;
        searchResultsContainer.appendChild(itemElement);
    });
}

// Event listener for search input
document.getElementById('search-input').addEventListener('input', function() {
    const query = this.value;
    
    // Fetch search results from the server (assuming you have an endpoint for this)
    fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => displaySearchResults(data.items))
        .catch(error => console.error('Error fetching search results:', error));
});
