/* -----------------SCRIPTS DE "REGISTER"------------------ */


const form = document.getElementById("form");
const c1 = document.getElementById("password");
const c2 = document.getElementById("c-password");
const msg = document.getElementById("msg");

form.addEventListener("submit", function(e){
  if (p1.value !== p2.value) {
    e.preventDefault();
    msg.textContent = "Las contraseñas no coinciden";
    msg.style.color = "red";
  }
});


/* -----------------SCRIPTS DE "REGISTER"------------------ */