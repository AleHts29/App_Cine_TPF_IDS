const toggle = document.getElementById("menuToggle");
const options = document.getElementById("menuOptions");
const arrow = document.getElementById("arrow");

toggle.addEventListener("click", () => {
    options.classList.toggle("hidden");
    arrow.classList.toggle("rotate-180");
});


// 🔹 Mostrar formulario de película
const btnPublicar = document.getElementById("btnPublicar");
const formCrear = document.getElementById("formCrearPelicula");
const usuariosSection = document.getElementById("usuarios");
// const tablaUsuarios = document.getElementById("tablaUsuarios");
// const buscadorUsuarios = document.getElementById("buscadorUsuarios");
const tablaUsuarios = document.getElementById("tablaDatos");
const buscadorUsuarios = document.querySelector("input[placeholder='Buscar por username']");

btnPublicar.addEventListener("click", () => {
    formCrear.classList.remove("hidden");

    // ocultar vistas
    document.getElementById("listaPeliculas").classList.add("hidden");
    document.getElementById("formEditarPelicula").classList.add("hidden");
    tablaUsuarios.classList.add("hidden");
    buscadorUsuarios.classList.add("hidden");
    usuariosSection.classList.add("hidden");
});


const form = document.getElementById("peliculaForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    // SE ENVÍA AL FRONTEND, NO AL BACKEND DIRECTO
    const resp = await fetch("/admin/peliculas/nueva", {
        method: "POST",
        body: formData
    });

    const data = await resp.json();
    alert(data.message);
});


// 🔹 Eliminar películas
function attachDeleteButtons() {
    document.querySelectorAll(".btnEliminar").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;

            if (!confirm("¿Seguro que deseas eliminar esta película?")) return;

            const resp = await fetch(`/admin/peliculas/${id}`, {
                method: "DELETE"
            });

            const data = await resp.json();
            alert(data.message);

            // refrescar lista
            document.getElementById("btnPeliculas").click();
        });
    });
}

// Mostrar formulario de edición
function attachEditButtons() {
    document.querySelectorAll(".btnEditar").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;

            // pedir datos al backend
            const resp = await fetch(`/admin/peliculas/${id}`);
            const peli = await resp.json();

            mostrarFormularioEditar(peli);
        });
    });
}


// 🔹 Listar películas
document.getElementById("btnPeliculas").addEventListener("click", async () => {
    // ocultar otras vistas
    document.getElementById("formCrearPelicula").classList.add("hidden");
    document.getElementById("formEditarPelicula").classList.add("hidden");
    tablaUsuarios.classList.add("hidden");
    buscadorUsuarios.classList.add("hidden");

    // Mostrar la sección de películas
    const lista = document.getElementById("listaPeliculas");
    lista.classList.remove("hidden");

    // Llamar al frontend → backend → DB
    const response = await fetch("/admin/peliculas/lista");
    const peliculas = await response.json();

    // Renderizar en la tabla
    const tabla = document.getElementById("tablaPeliculas");
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
          <img src="/static/${p.imagen_url || '/static/img/default.jpg'}" 
               class="w-16 h-20 object-cover rounded">
        </td>
        <td class="px-4 py-2 text-center space-x-2">
          <button class="btnEditar bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg" 
            data-id="${p.id_pelicula}">
            Editar
          </button>
          <button class="btnEliminar bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-lg" 
            data-id="${p.id_pelicula}">
            Eliminar
          </button>
        </td>
      </tr>
    `;
    });

    // Re-enganchamos los botones una vez renderizados
    attachEditButtons();
    attachDeleteButtons();
});


// Función para mostrar el formulario de edición
function mostrarFormularioEditar(p) {
    const cont = document.getElementById("formEditarPelicula");

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

    document.getElementById("listaPeliculas").classList.add("hidden");

    const formEdit = document.getElementById("formEdit");

    formEdit.addEventListener("submit", async (e) => {
        e.preventDefault();

        let data = new FormData(formEdit);

        const resp = await fetch(`/admin/peliculas/${p.id_pelicula}`, {
            method: "PUT",
            body: data
        });

        const result = await resp.json();
        alert(result.message);

        // refrescar lista
        document.getElementById("btnPeliculas").click();
    });
}