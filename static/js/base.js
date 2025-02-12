let lastScrollY = window.scrollY;
document.getElementsById('header');
window.addEventListener('scroll', () =>
{if (window.scrollY > lastScrollY)
{Headers.classList.add('hidden');}
else{
    Headers.classList.remove('hidden');
}
lastScrollY = window.scrollY;
})