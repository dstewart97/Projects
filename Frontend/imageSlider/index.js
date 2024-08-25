const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

nextBtn.addEventListener('click', () => {
    const menu = document.querySelector('menu');
    const cards = document.querySelectorAll('li');
    menu.appendChild(cards[0])
})

prevBtn.addEventListener('click', () => {
    const menu = document.querySelector('menu');
    const cards = document.querySelectorAll('li');
    menu.prepend(cards[cards.length - 1])
})