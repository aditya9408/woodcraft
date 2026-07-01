// Mobile nav toggle
const toggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

if (toggle && navLinks) {
  toggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

// Auto-dismiss flash messages after 5 seconds
setTimeout(() => {
  document.querySelectorAll('.flash-message').forEach(el => el.remove());
}, 5000);
