const sign_in_btn = document.querySelector("#add-trans-btn");
const sign_up_btn = document.querySelector("#view-trans-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
