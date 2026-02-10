document.addEventListener("DOMContentLoaded", () => {

  const modal = document.getElementById("studentModal");
  const openBtn = document.getElementById("openModal");

  if (!modal || !openBtn) {
    console.error("Modal or button not found");
    return;
  }

  openBtn.addEventListener("click", () => {
    modal.classList.add("show");
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("show");
    }
  });
});

