// Season switch: cross-fades the summer/winter carousels.
(function () {
  const sws = document.querySelectorAll(".season");
  const car = document.querySelector(".season-carousel");
  if (!sws.length || !car) return;
  let season = "summer";
  function set(s) {
    season = s;
    const w = s === "winter";
    sws.forEach(sw => {
      sw.classList.toggle("winter", w);
      sw.querySelectorAll(".lb").forEach(b => b.classList.toggle("on", b.dataset.season === s));
      sw.querySelector(".switch").setAttribute("aria-checked", w);
    });
    car.classList.toggle("is-winter", w);
    document.body.classList.toggle("is-winter", w);
    car.querySelector(".winter-carousel").setAttribute("aria-hidden", !w);
    car.querySelector(".summer-carousel").setAttribute("aria-hidden", w);
  }
  sws.forEach(sw => {
    sw.querySelector(".switch").addEventListener("click", () => set(season === "summer" ? "winter" : "summer"));
    sw.querySelectorAll(".lb").forEach(b => b.addEventListener("click", () => set(b.dataset.season)));
  });
})();

// Trip planning form: exact vs flexible dates; demo submit (no backend).
(function () {
  const form = document.getElementById("trip-form");
  if (!form) return;
  form.querySelectorAll('input[name="date_mode"]').forEach(r => r.addEventListener("change", () => {
    form.querySelectorAll(".date-panel").forEach(p => p.hidden = p.dataset.mode !== r.value);
  }));
  const setLength = () => form.classList.toggle("is-single", form.querySelector('input[name="trip_length"]:checked').value === "single");
  form.querySelectorAll('input[name="trip_length"]').forEach(r => r.addEventListener("change", setLength));
  setLength();
  const start = form.querySelector("#start_date"), end = form.querySelector("#end_date");
  start.min = new Date().toISOString().slice(0, 10);
  start.addEventListener("change", () => { end.min = start.value; if (end.value && end.value < start.value) end.value = start.value; });
  // Stepper
  const steps = [...form.querySelectorAll("fieldset")];
  const back = form.querySelector('[data-step="back"]'), next = form.querySelector('[data-step="next"]');
  const submit = form.querySelector('button[type="submit"]'), count = form.querySelector(".step-count");
  const bar = form.querySelector(".step-progress span");
  let cur = 0;
  steps.forEach(f => f.classList.add("step"));
  function show(i) {
    cur = i;
    steps.forEach((f, j) => f.classList.toggle("current", j === i));
    back.hidden = i === 0;
    next.hidden = i === steps.length - 1;
    submit.hidden = i !== steps.length - 1;
    count.textContent = `Question ${i + 1} of ${steps.length}`;
    bar.style.width = `${((i + 1) / steps.length) * 100}%`;
  }
  function valid() {
    const bad = [...steps[cur].querySelectorAll("input, select")].find(el => !el.checkValidity());
    if (bad) { bad.reportValidity(); return false; }
    return true;
  }
  next.addEventListener("click", () => { if (valid()) show(cur + 1); });
  back.addEventListener("click", () => show(cur - 1));
  form.addEventListener("keydown", e => {
    if (e.key === "Enter" && e.target.tagName === "INPUT" && cur < steps.length - 1) { e.preventDefault(); next.click(); }
  });
  show(0);

  form.addEventListener("submit", e => {
    e.preventDefault();
    if (!valid()) return;
    steps.forEach(f => f.classList.remove("current"));
    form.querySelector(".step-nav").hidden = true;
    bar.style.width = "100%";
    form.querySelector(".form-thanks").hidden = false;
  });
})();

// Navbar menu links are turned off.
document.querySelectorAll("a[data-disabled-link]").forEach(a => a.addEventListener("click", e => {
  if (!a.matches('[data-bs-toggle="dropdown"]')) e.preventDefault();
}));
