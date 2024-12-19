// Функция прокрутки категорий
function scrollCategory(direction) {
  const categoryList = document.querySelector('.category-list');
  const categoryItems = document.querySelectorAll('.category-item');
  const itemWidth = categoryItems[0].offsetWidth + 20; // ширина одного элемента с отступом
  let scrollAmount = categoryList.scrollLeft;

  if (direction === 'next') {
    scrollAmount += itemWidth * 3; // Прокручиваем на 3 элемента
  } else {
    scrollAmount -= itemWidth * 3;
  }

  categoryList.scrollTo({
    left: scrollAmount,
    behavior: 'smooth'
  });
}

// Функция прокрутки категорий
function scrollProduct(direction) {
  const categoryList = document.querySelector('.category-list');
  const categoryItems = document.querySelectorAll('.product-item');
  const itemWidth = ProductItems[0].offsetWidth + 20; // ширина одного элемента с отступом
  let scrollAmount = ProductList.scrollLeft;

  if (direction === 'next') {
    scrollAmount += itemWidth * 3; // Прокручиваем на 3 элемента
  } else {
    scrollAmount -= itemWidth * 3;
  }

  categoryList.scrollTo({
    left: scrollAmount,
    behavior: 'smooth'
  });
}

// Функция прокрутки скидок
function scrollDiscount(direction) {
  const discountList = document.querySelector('.discount-list');
  const discountItems = document.querySelectorAll('.discount-item');
  const itemWidth = discountItems[0].offsetWidth + 20; // ширина одного элемента с отступом
  let scrollAmount = discountList.scrollLeft;

  if (direction === 'next') {
    scrollAmount += itemWidth * 3; // Прокручиваем на 3 элемента
  } else {
    scrollAmount -= itemWidth * 3;
  }

  discountList.scrollTo({
    left: scrollAmount,
    behavior: 'smooth'
  });
}

// Получаем элемент карты сайта
const siteMap = document.getElementById('site-map');

// Функция для обработки прокрутки
window.addEventListener('scroll', function() {
  // Проверяем, находимся ли в верхней части страницы
  if (window.scrollY === 0) {
    // Если прокручено до верха, показываем карту сайта
    siteMap.classList.add('show');
  } else {
    // Если не вверху, скрываем карту сайта
    siteMap.classList.remove('show');
  }
});

// Получаем элементы плашки поиска и логотипа
const searchBar = document.querySelector('.search-bar');
const logoPlaceholder = document.getElementById('logo-placeholder');

// Функция для скрытия логотипа при прокрутке страницы
window.addEventListener('scroll', function() {
  if (window.scrollY > 0) {
    // Если страница прокручена вниз, скрываем логотип
    searchBar.classList.add('hide-logo');
    searchBar.classList.add('show-sm');
  } else {
    // Если страница снова наверху, показываем логотип
    searchBar.classList.remove('hide-logo');
    searchBar.classList.remove('show-sm');
  }
});

// Кнопки прокрутки для популярных товаров
const scrollLeftBtn = document.querySelector('.scroll-left');
const scrollRightBtn = document.querySelector('.scroll-right');
const productCarousel = document.querySelector('.product-carousel');

scrollLeftBtn.addEventListener('click', () => {
  productCarousel.scrollBy({ left: -200, behavior: 'smooth' });
});

scrollRightBtn.addEventListener('click', () => {
  productCarousel.scrollBy({ left: 200, behavior: 'smooth' });
});
