const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const navLink = document.querySelector(".nav-link");


hamburger.addEventListener('click', mobileMenu);

// navLink.forEach(n => n.addEventListener("click", closeMenu));

function mobileMenu() {

    navMenu.classList.toggle("active");
};

