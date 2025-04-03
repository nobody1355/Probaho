// static/javascript/index.js

// Set dynamic background images based on `data-bg` attribute
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('[data-bg]');
    sections.forEach(section => {
        const bg = section.getAttribute('data-bg');
        if (bg) {
            section.style.backgroundImage = `url(${bg})`;
        }
    });
});

// Change the body's background when scrolling to sections
document.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const scrollPosition = window.scrollY + window.innerHeight / 2;

    sections.forEach(section => {
        const offsetTop = section.offsetTop;
        const offsetHeight = section.offsetHeight;

        if (scrollPosition > offsetTop && scrollPosition < offsetTop + offsetHeight) {
            document.body.style.backgroundImage = `url('${section.getAttribute('data-bg')}')`;
        }
    });
});
