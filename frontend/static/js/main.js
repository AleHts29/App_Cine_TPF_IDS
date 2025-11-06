/* -----------------SCRIPTS DE "REGISTER"------------------ */


const form = document.getElementById("form");
const c1 = document.getElementById("password");
const c2 = document.getElementById("c-password");
const msg = document.getElementById("msg");

form.addEventListener("submit", function(e){
  if (c1.value !== c2.value) {
    e.preventDefault();
    msg.textContent = "Las contraseñas no coinciden";
    msg.style.color = "red";
  }
});

const slides = document.querySelectorAll(".slide");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

let index = 0;
let isAnimating = false;
let interval;

function setupSlides() {
  slides.forEach((slide, i) => {
    slide.classList.add(
      "absolute",
      "w-full",
      "h-full",
      "top-0",
      "left-0",
      "transition-all",
      "duration-700",
      "ease-in-out",
      "transform"
    );
    slide.style.zIndex = i === 0 ? "10" : "0";
    slide.style.opacity = i === 0 ? "1" : "0";
    slide.style.transform = "translateX(0)";
  });
}

function showSlide(newIndex, direction = 1) {
  if (isAnimating || newIndex === index) return;
  isAnimating = true;

  const current = slides[index];
  const next = slides[newIndex];

  next.style.transition = "none";
  next.style.opacity = "0";
  next.style.transform = `translateX(${direction === 1 ? "100%" : "-100%"})`;
  next.style.zIndex = "20";

  void next.offsetWidth;

  current.style.transition = "transform 0.7s ease-in-out, opacity 0.7s ease-in-out";
  next.style.transition = "transform 0.7s ease-in-out, opacity 0.7s ease-in-out";

  current.style.transform = `translateX(${direction === 1 ? "-100%" : "100%"})`;
  current.style.opacity = "0";
  next.style.transform = "translateX(0)";
  next.style.opacity = "1";

  setTimeout(() => {
    current.style.zIndex = "0";
    next.style.zIndex = "10";
    index = newIndex;
    isAnimating = false;
  }, 700);
}

function nextSlide() {
  const newIndex = (index + 1) % slides.length;
  showSlide(newIndex, 1);
}

function prevSlideFunc() {
  const newIndex = (index - 1 + slides.length) % slides.length;
  showSlide(newIndex, -1);
}

function startInterval() {
  interval = setInterval(nextSlide, 7000);
}

function resetInterval() {
  clearInterval(interval);
  startInterval();
}

nextBtn.addEventListener("click", () => {
  nextSlide();
  resetInterval();
});

prevBtn.addEventListener("click", () => {
  prevSlideFunc();
  resetInterval();
});

// Inicialización
setupSlides();
startInterval();

/* -----------------SCRIPTS DE "REGISTER"------------------ */