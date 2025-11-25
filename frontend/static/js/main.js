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