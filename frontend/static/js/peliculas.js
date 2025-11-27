async function mostrarPelicula(
  titulo,
  duracion,
  sinopsis,
  director,
  genero,
  id_pelicula,
  imagen
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
    return f.toLocaleTimeString("es-ES", {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  const agrupadas = {};
  funciones.forEach((f) => {
    const clave = obtenerDiaClave(f.fecha_hora);
    if (!agrupadas[clave]) agrupadas[clave] = [];
    agrupadas[clave].push(f);
  });

  let fechasHtml = "";
  for (let clave in agrupadas) {
    fechasHtml += `
      <button class="fecha-btn px-4 py-2 bg-gray-700 rounded hover:bg-red-700"
              data-fecha="${clave}">
        ${formatearFecha(agrupadas[clave][0].fecha_hora)}
      </button>`;
  }

  Swal.fire({
    width: "50%",
    background: "#111",
    color: "#fff",
    showConfirmButton: false,
    html: `
      <div class="flex flex-col md:flex-row text-left">

        <div class="">
          <div class="relative">
          <img src="${imagen}" class="img-card w-60 h-96 object-cover rounded-t-2xl shadow-lg">
          <p class="absolute top-2 right-2 bg-black/60 text-white text-sm px-2 py-1 rounded-md">⏱ ${duracion}'</p>
          </div>
          <div class="flex gap-2">
            <span class="px-3 py-1 bg-gray-700 rounded-full text-sm mt-2 inline-block hover:bg-[#700000] transition">
              genero: ${genero}
            </span>
            <span class="px-3 py-1 bg-gray-700 rounded-full text-sm mt-2 inline-block hover:bg-[#700000] transition">
              director: ${director}
            </span>
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

  document.addEventListener("click", function listener(e) {
    if (e.target.classList.contains("fecha-btn")) {
      document.querySelectorAll(".fecha-btn").forEach((btn) => {
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
        <div class="flex flex-wrap gap-3">`;

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

    if (e.target.classList.contains("hora-btn")) {
      document.querySelectorAll(".hora-btn").forEach((btn) => {
        btn.classList.remove("bg-red-600", "text-white");
        btn.classList.add("bg-gray-700", "text-gray-300");
      });

      e.target.classList.remove("bg-gray-700", "text-gray-300");
      e.target.classList.add("bg-red-600", "text-white");

      document.querySelector("#contenedor-comprar").innerHTML = "";

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
        if (window.usernameActual) {
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

// Listeners
document.querySelectorAll(".pelicula-cartelera").forEach((card) => {
  card.addEventListener("click", () => {
    mostrarPelicula(
      card.dataset.titulo,
      card.dataset.duracion,
      card.dataset.sinopsis,
      card.dataset.director,
      card.dataset.genero,
      card.dataset.id,
      card.dataset.img
    );
  });
});

document.getElementById("filtroGenero").addEventListener("change", function () {
  const generoSeleccionado = this.value.toLowerCase();
  const peliculas = document.querySelectorAll(".card-pelicula");

  peliculas.forEach((card) => {
    const generoCard = card.dataset.genero.toLowerCase();

    if (generoSeleccionado === "todos" || generoCard === generoSeleccionado) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
});