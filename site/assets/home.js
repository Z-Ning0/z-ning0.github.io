const experiment = document.querySelector(".walk");
const controls = experiment.querySelector(".walk-controls");
const buttons = controls.querySelectorAll("button");

for (const button of buttons) {
  button.addEventListener("click", () => {
    experiment.dataset.selected = button.dataset.directory;
    for (const option of buttons) {
      option.setAttribute("aria-pressed", String(option === button));
    }
  });
}

controls.hidden = false;
