  const form = document.getElementById("contactForm");
    const modal = document.getElementById("modal");
    const openBtn = document.getElementById("openModal");
    const closeBtn = document.getElementById("closeModal");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    openBtn.addEventListener("click", function (e) {
        e.preventDefault();
        modal.classList.remove("hidden");
    });

    closeBtn.addEventListener("click", function () {
        modal.classList.add("hidden");
    });

    modal.addEventListener("click", function (e) {
        if (e.target === modal) modal.classList.add("hidden");
    });
