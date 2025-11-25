/* -----------------SCRIPTS DE "REGISTER"------------------ */

(async function () {

  const form = document.getElementById("form");
  const c1 = document.getElementById("password");
  const c2 = document.getElementById("c-password");
  const msg = document.getElementById("msg");

    form.addEventListener("submit", async function(e){ 
    e.preventDefault();
    if (c1.value !== c2.value) {
      msg.textContent = "Las contraseñas no coinciden";
      msg.style.color = "red";
      return;
    }

      const data = {
    email: document.getElementById("email").value,
    username: document.getElementById("name").value,
    full_name: document.getElementById("r-name").value,
    password: c1.value
      };
    
      try {
        const response = await fetch("/usuarios", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
          msg.textContent = "Se envió un correo de verificación. Revisá tu mail.";
          msg.style.color = "green";
          form.reset();
          startPolling(result.id);
        } 
        else {
          msg.textContent = result.error || "Error al registrar usuario";
          msg.style.color = "red";
        }
      } 
      catch (err) {
        console.error(err);
        msg.textContent = "Error del servidor";
        msg.style.color = "red";
      }

        function startPolling(userId) {
          const interval = setInterval(async () => {
            try {
              const res = await fetch(`/usuarios/status/${userId}`);
              const data = await res.json();
              if (data.is_active) {
                clearInterval(interval);
                window.location.href = "/login"; 
              }
            } catch (err) {
              console.error("Error en el polling:", err);
            }
          }, 3000); 

        }
        
      })

})();


/* -----------------SCRIPTS DE "REGISTER"------------------ */


/* -----------------SIDEBAR DE NAVBAR------------------ */


function sidebar_navbar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");

    if (sidebar.classList.contains("translate-x-full")) {
        sidebar.classList.remove("translate-x-full");
        overlay.classList.remove("hidden");
    } else {
        sidebar.classList.add("translate-x-full");
        overlay.classList.add("hidden");
    }
}


/* -----------------SIDEBAR DE NAVBAR------------------ */

/* -----------------NAVBAR FANTASMA------------------ */


function navbarFantasma() {

    const floatNav = document.getElementById("navbar-fantasma");
    const originalNav = document.getElementById("navbar-original");

    if (!floatNav || !originalNav) return;

    let lastScroll = 0;

    function handleScroll() {
        const fondo = originalNav.getBoundingClientRect().bottom;
        const scrollY = window.scrollY;

        if (fondo < 0 && scrollY > lastScroll) {
            floatNav.classList.remove("hidden");
            floatNav.classList.remove("-translate-y-full");
            floatNav.classList.add("translate-y-0");
        }

        if (scrollY < lastScroll && fondo >= 0) {
            floatNav.classList.add("-translate-y-full");
            setTimeout(() => floatNav.classList.add("hidden"), 300);
        }

        lastScroll = scrollY;
    }

    window.addEventListener("scroll", handleScroll);
}
document.addEventListener("DOMContentLoaded", navbarFantasma);


/* -----------------NAVBAR FANTASMA ------------------ */


function initSlider() {

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

  setupSlides();
  startInterval();
}


function initButacas() {

  document.querySelectorAll(".butaca").forEach(b => {
    if (!b.classList.contains("bg-red-600")) {
      b.addEventListener("click", () => {
        if (b.classList.contains("bg-green-500")) {
          b.classList.remove("bg-green-500");
          b.classList.add("bg-yellow-400");
        } else if (b.classList.contains("bg-yellow-400")) {
          b.classList.remove("bg-yellow-400");
          b.classList.add("bg-green-500");
        }
      });
    }
  });

  document.getElementById("btn-confirmar").addEventListener("click", () => {
    const seleccionadas = document.querySelectorAll(".bg-yellow-400");
    alert(`Seleccionaste ${seleccionadas.length} butaca(s).`);
  });

}