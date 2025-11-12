/* -----------------SCRIPTS DE "REGISTER"------------------ */

(function () {

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
        const response = await fetch("http://localhost:9090/usuarios/", {
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
              const res = await fetch(`http://localhost:9090/usuarios/status/${userId}`);
              const data = await res.json();
              if (data.is_active) {
                clearInterval(interval);
                window.location.href = "/"; 
              }
            } catch (err) {
              console.error("Error en el polling:", err);
            }
          }, 3000); 

        }
        
      })

})();


/* -----------------SCRIPTS DE "REGISTER"------------------ */