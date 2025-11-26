
function get(id) {
    return document.getElementById(id);
}

function hide(id) {
    const el = get(id);
    if (el) el.classList.add("hidden");
}

function show(id) {
    const el = get(id);
    if (el) el.classList.remove("hidden");
}

function ocultarTodo() {
    hide("listaPeliculas");
    hide("listaEntradas");
    hide("formCrearPelicula");
    hide("formEditarPelicula");
    hide("usuariosSection");
}


const toggle = get("menuToggle");
const options = get("menuOptions");
const arrow = get("arrow");

if (toggle && options && arrow) {
    toggle.addEventListener("click", () => {
        options.classList.toggle("hidden");
        arrow.classList.toggle("rotate-180");
    });
}



const btnPublicar = get("btnPublicar");

if (btnPublicar) {
    btnPublicar.addEventListener("click", () => {
        ocultarTodo();
        show("formCrearPelicula");
    });
}


// ============================
// BOTÓN: GESTIÓN PELÍCULAS
// ============================
const btnPeliculas = get("btnPeliculas");

if (btnPeliculas) {
    btnPeliculas.addEventListener("click", async () => {
        ocultarTodo();
        show("listaPeliculas");

        const resp = await fetch("/admin/peliculas/lista");
        const peliculas = await resp.json();

        const tabla = get("tablaPeliculas");
        tabla.innerHTML = "";

        peliculas.forEach(p => {
            tabla.innerHTML += `
                <tr class="border-b border-gray-700 hover:bg-gray-800">
                    <td class="px-4 py-2">${p.id_pelicula}</td>
                    <td class="px-4 py-2">${p.titulo}</td>
                    <td class="px-4 py-2">${p.duracion}'</td>
                    <td class="px-4 py-2">${p.genero}</td>
                    <td class="px-4 py-2">${p.estado}</td>
                    <td class="px-4 py-2">
                        <img src="/static/${p.imagen_url}" class="w-16 h-20 object-cover rounded">
                    </td>
                    <td class="px-4 py-2 text-center space-x-2">
                        <button class="btnEditar bg-blue-600 px-3 py-1 rounded-lg text-white"
                                data-id="${p.id_pelicula}">
                            Editar
                        </button>
                        <button class="btnEliminar bg-red-600 px-3 py-1 rounded-lg text-white"
                                data-id="${p.id_pelicula}">
                            Eliminar
                        </button>
                    </td>
                </tr>
            `;
        });

        attachEditButtons();
        attachDeleteButtons();
    });
}


// ============================
// BOTÓN: GESTIÓN ENTRADAS
// ============================
const btnEntradas = get("btnEntradas");

if (btnEntradas) {
    btnEntradas.addEventListener("click", async () => {
        ocultarTodo();
        show("listaEntradas");

        const resp = await fetch("/admin/entradas/lista");
        const entradas = await resp.json();

        const tabla = get("tablaEntradas");
        tabla.innerHTML = "";

        entradas.forEach(e => {
            tabla.innerHTML += `
                <tr class="border-b border-gray-700 hover:bg-gray-800">
                    <td class="px-4 py-2">${e.id_entrada}</td>
                    <td class="px-4 py-2">${e.id_user}</td>
                    <td class="px-4 py-2">${e.id_funcion}</td>
                    <td class="px-4 py-2">${e.id_butaca}</td>
                    <td class="px-4 py-2">${e.precio_final}</td>
                    <td class="px-4 py-2">${e.estado}</td>
                    <td class="px-4 py-2">${e.fecha}</td>
                    <td class="px-4 py-2 text-center">
                        <button class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-lg">
                            Eliminar
                        </button>
                    </td>
                </tr>
            `;
        });
    });
}


// ============================
// CREAR PELÍCULA
// ============================
const form = get("peliculaForm");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        const resp = await fetch("/admin/peliculas/nueva", {
            method: "POST",
            body: formData
        });

        const data = await resp.json();
        alert(data.message || data.error);

        if (resp.ok) {
            form.reset();
            get("funcionesContainer").innerHTML = "";
        }
    });
}

const funcionesContainer = document.getElementById("funcionesContainer");
const addFuncionBtn = document.getElementById("addFuncionBtn");

addFuncionBtn.addEventListener("click", () => {
    const div = document.createElement("div");
    div.classList = "bg-gray-700 p-4 rounded-lg grid grid-cols-3 gap-4";

    div.innerHTML = `
        <input type="number" name="funcion_sala[]" placeholder="ID Sala"
               class="bg-gray-600 px-2 py-2 rounded">

        <input type="datetime-local" name="funcion_fecha[]" 
               class="bg-gray-600 px-2 py-2 rounded">

        <input type="number" name="funcion_precio[]" placeholder="Precio base"
               class="bg-gray-600 px-2 py-2 rounded">
    `;

    funcionesContainer.appendChild(div);
});


// ============================
// EDICIÓN Y BORRADO
// ============================
function attachDeleteButtons() {
    document.querySelectorAll(".btnEliminar").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;

            if (!confirm("¿Eliminar?")) return;

            await fetch(`/admin/peliculas/${id}`, {
                method: "DELETE"
            });

            btnPeliculas.click();
        });
    });
}

function attachEditButtons() {
    document.querySelectorAll(".btnEditar").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;

            const resp = await fetch(`/admin/peliculas/${id}`);
            const p = await resp.json();

            mostrarFormularioEditar(p);
        });
    });
}


// ============================
// FORMULARIO DE EDICIÓN
// ============================
function mostrarFormularioEditar(p) {
    ocultarTodo();

    const cont = get("formEditarPelicula");

    cont.innerHTML = `
        <div class="bg-gray-800 p-6 rounded-xl shadow-xl text-gray-100">
        <h2 class="text-2xl font-bold mb-4">Editar película</h2>

        <form id="formEdit" class="space-y-4" enctype="multipart/form-data">

            <input type="text" name="titulo" value="${p.titulo}"
                class="w-full bg-gray-700 px-4 py-2 rounded-lg">

            <input type="number" name="duracion" value="${p.duracion}"
                class="w-full bg-gray-700 px-4 py-2 rounded-lg">

            <input type="text" name="genero" value="${p.genero}"
                class="w-full bg-gray-700 px-4 py-2 rounded-lg">
            

            <textarea name="sinopsis"
                class="w-full bg-gray-700 px-4 py-2 rounded-lg">${p.sinopsis || ""}</textarea>

            <input type="text" name="director" value="${p.director || ""}"
                class="w-full bg-gray-700 px-4 py-2 rounded-lg">

            <label class="block font-semibold">Estado</label>
            <select name="estado" class="w-full bg-gray-700 px-4 py-2 rounded-lg">
                <option value="en_cartelera" ${p.estado === 'en_cartelera' ? 'selected' : ''}>En cartelera</option>
                <option value="proximamente" ${p.estado === 'proximamente' ? 'selected' : ''}>Próximamente</option>
                <option value="finalizada" ${p.estado === 'finalizada' ? 'selected' : ''}>Finalizada</option>
            </select>

            <label class="block font-semibold mt-4">Imagen actual</label>
            <img src="/static/${p.imagen_url}" 
                 class="w-32 h-44 object-cover rounded-lg shadow mb-2">

            <input type="hidden" name="imagen_actual" value="${p.imagen_url}">

            <label class="block font-semibold mt-4">Nueva imagen (opcional)</label>
            <input type="file" name="imagen" class="w-full bg-gray-700 px-4 py-2 rounded-lg">


            <button type="submit"
                class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold">
                Guardar cambios
            </button>
        </form>
    </div>
    `;

    cont.classList.remove("hidden");

    const formEdit = get("formEdit");

    formEdit.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = new FormData(formEdit);

        await fetch(`/admin/peliculas/${p.id_pelicula}`, {
            method: "PUT",
            body: data
        });

        btnPeliculas.click();
    });
}

function desactivarUsuario(id) {
    fetch(`http://localhost:9090/usuarios/desactivar/${id}`, {
      method: "PATCH"
    })
      .then(res => res.json())
      .then(data => {
        alert("Usuario desactivado");
        location.reload();
      })
      .catch(err => console.error("Error:", err));

  }
  function borrarUsuario(id) {
    fetch(`http://localhost:9090/usuarios/borrar/${id}`, {
      method: "DELETE"
    })
      .then(res => res.json())
      .then(data => {
        alert("Usuario eliminado");
        location.reload();
      })
      .catch(err => console.error("Error:", err));

  }
  function activarUSuario(id) {
    fetch(`http://localhost:9090/usuarios/activar/${id}`, {
      method: "PATCH"
    })
      .then(res => res.json())
      .then(data => {
        alert("Usuario activado");
        location.reload();
      })
      .catch(err => console.error("Error:", err));

  }