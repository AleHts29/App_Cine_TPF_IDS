const username = JSON.parse(document.body.dataset.username || "null");
const activo = Number(document.body.dataset.activo || 0);

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

        let result;
        try {
          result = await response.json();
        } catch {
          result = { error: "Username/Email ya registrado(s)" };
        }

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


new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 15,
    loop: true,
    autoplay: {
      delay: 2000,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      0: { slidesPerView: 1 },
      640: { slidesPerView: 2 },
      1024: { slidesPerView: 3 },
      1280: { slidesPerView: 3 },
    },
  });



async function mostrarPelicula(
  titulo,
  duracion,
  sinopsis,
  director,
  genero,
  id_pelicula,
  imagen,
  activo,
  username
) {
  const resp = await fetch(`/api/funciones?pelicula=${id_pelicula}`);
  const funciones = await resp.json();

  if (!Array.isArray(funciones) || funciones.length === 0) {
    Swal.fire("Sin funciones disponibles", "", "warning");
    return;
  }

  function formatearFecha(fechaCompleta) {
    const f = new Date(fechaCompleta);
    return f.getDate() + " " + f.toLocaleString("es-ES", { month: "short" });
  }

  function obtenerDiaClave(fechaCompleta) {
    return new Date(fechaCompleta).toISOString().split("T")[0];
  }

  function formatearHora(fechaCompleta) {
    const f = new Date(fechaCompleta);
    return f.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" });
  }

  // AGRUPAR POR FECHA
  const agrupadas = {};
  funciones.forEach((f) => {
    const clave = obtenerDiaClave(f.fecha_hora);
    if (!agrupadas[clave]) agrupadas[clave] = [];
    agrupadas[clave].push(f);
  });

  // BOTONES DE FECHAS
  let fechasHtml = "";
  for (let clave in agrupadas) {
    fechasHtml += `
      <button class="fecha-btn px-4 py-2 bg-gray-700 rounded hover:bg-red-700"
              data-fecha="${clave}">
        ${formatearFecha(agrupadas[clave][0].fecha_hora)}
      </button>`;
  }

  // MOSTRAR POPUP
  Swal.fire({
    width: "80%",
    background: "#111",
    color: "#fff",
    showConfirmButton: false,
    html: `
      <div class="flex flex-col md:flex-row text-left">

        <div class="md:w-1/3">
          <img src="${imagen}" class="img-card w-60 h-96 object-cover rounded-t-2xl shadow-lg">
          <div class="flex gap-2">
            <span class="px-3 py-1 bg-gray-700 rounded-full text-sm mt-2 inline-block hover:bg-[#700000] transition">genero: ${genero}</span>
            <span class="px-3 py-1 bg-gray-700 rounded-full text-sm mt-2 inline-block hover:bg-[#700000] transition">director: ${director}</span>
          </div>
        </div>

        <div class="md:w-2/3 md:pl-6">
          <h1 class="text-3xl font-bold text-red-600">${titulo}</h1>
          <p class="text-gray-300 mb-4 leading-relaxed">${sinopsis}</p>

          <h2 class="text-xl font-semibold mb-2">Elegí una fecha:</h2>

          <div id="contenedor-fechas" class="flex flex-wrap gap-3 mb-6">
            ${fechasHtml}
          </div>

          <div id="contenedor-horarios"></div>
          <div id="contenedor-comprar" class="mt-6"></div>
        </div>

      </div>
    `,
  });

  // DELEGACIÓN DE EVENTOS DENTRO DEL SWEETALERT
  document.addEventListener("click", function listener(e) {
    // CLICK EN FECHA
    if (e.target.classList.contains("fecha-btn")) {
      document.querySelectorAll(".fecha-btn").forEach(btn => {
        btn.classList.remove("bg-red-600", "text-white");
        btn.classList.add("bg-gray-700", "text-gray-300");
      });
      e.target.classList.remove("bg-gray-700", "text-gray-300");
      e.target.classList.add("bg-red-600", "text-white");
      document.querySelector("#contenedor-comprar").innerHTML = "";

      const clave = e.target.dataset.fecha;
      const lista = agrupadas[clave];

      let horariosHtml = `
        <h3 class="text-xl font-semibold mb-2">Horarios disponibles:</h3>
        <div class="flex flex-wrap gap-3">
      `;

      lista.forEach((f) => {
        horariosHtml += `
          <button class="hora-btn px-4 py-2 bg-gray-700 rounded hover:bg-red-700"
                  data-id="${f.id_funcion}">
            ${formatearHora(f.fecha_hora)} · Sala ${f.id_sala}
          </button>`;
      });

      horariosHtml += "</div>";

      document.querySelector("#contenedor-horarios").innerHTML = horariosHtml;
    }

    // CLICK EN HORARIO
    if (e.target.classList.contains("hora-btn")) {
      document.querySelectorAll(".hora-btn").forEach(btn => {
        btn.classList.remove("bg-red-600", "text-white");
        btn.classList.add("bg-gray-700", "text-gray-300");
      });
      e.target.classList.remove("bg-gray-700", "text-gray-300");
      e.target.classList.add("bg-red-600", "text-white");

      const idFuncionSeleccionada = e.target.dataset.id;

      document.querySelector("#contenedor-comprar").innerHTML = `
        <div class="flex flex-col gap-2">
          <button id="btnComprar"
            class="mt-4 px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl">
            COMPRAR ENTRADAS
          </button>
          <p id="msgError" class="text-red-500 text-sm font-semibold hidden"></p>
        </div>
      `;

      document.querySelector("#btnComprar").onclick = () => {
        if (username) {
          window.location.href = `/butacas?pelicula=${id_pelicula}&funcion=${idFuncionSeleccionada}`;
        } else {
          const msg = document.querySelector("#msgError");
          msg.innerHTML = `Necesitas tener una cuenta para comprar entradas,
            podés iniciar sesión <a href="/login" class="underline text-red-400">aquí</a>.`;
          msg.classList.remove("hidden");
        }
      };
    }
  });
}

// CLICK EN CADA TARJETA
document.querySelectorAll(".pelicula-cartelera").forEach((card) => {
  card.addEventListener("click", () => {
    mostrarPelicula(
      card.dataset.titulo,
      card.dataset.duracion,
      card.dataset.sinopsis,
      card.dataset.director,
      card.dataset.genero,
      card.dataset.id,
      card.dataset.img,
      activo,
      username
    );
  });
});

// FILTRO POR GENERO
document.getElementById("filtroGenero").addEventListener("change", function () {
  const generoSeleccionado = this.value.toLowerCase();
  const peliculas = document.querySelectorAll(".card-pelicula");

  peliculas.forEach(card => {
    const generoCard = card.dataset.genero.toLowerCase();
    if (generoSeleccionado === "todos" || generoCard === generoSeleccionado) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
});

/* -----BOTON MOSTRAR MAS EN CARTELERA ----*/

function inicializarMostrarMas() {
    const btn = document.getElementById("btnMostrarMas");
    if (!btn) return; // por si estás en otra página

    const extras = document.querySelectorAll(".extra-pelicula");

    btn.addEventListener("click", () => {
        extras.forEach(card => card.classList.remove("hidden"));
        btn.classList.add("hidden");
    });
}

document.addEventListener("DOMContentLoaded", inicializarMostrarMas);

/* -----BOTON MOSTRAR MAS EN CARTELERA ----*/