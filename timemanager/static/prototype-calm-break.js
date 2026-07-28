(() => {
  const form = document.querySelector("[data-calm-builder]");
  if (!form) return;

  const empty = document.querySelector("[data-calm-empty]");
  const plan = document.querySelector("[data-calm-plan]");
  const reason = document.querySelector("[data-calm-reason]");
  const guidelines = document.querySelector("[data-calm-guidelines]");
  const checkIn = document.querySelector("[data-calm-check-in]");
  const status = document.querySelector("[data-calm-status]");
  const responseStatus = document.querySelector("[data-calm-response-status]");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const selected = data.getAll("guideline");
    const custom = String(data.get("custom_guideline") || "").trim();
    if (custom) selected.push(custom);
    if (selected.length === 0) selected.push("Choose your own quiet reset");

    reason.textContent = String(data.get("reason") || "").trim();
    guidelines.replaceChildren(
      ...selected.map((text) => {
        const item = document.createElement("li");
        item.textContent = text;
        return item;
      }),
    );
    checkIn.textContent = String(data.get("check_in"));
    empty.hidden = true;
    plan.hidden = false;
    responseStatus.textContent = "";
    status.textContent = "The calm-break plan is ready to review together.";
    plan.querySelector("button").focus();
  });

  document.querySelector("[data-calm-actions]").addEventListener("click", (event) => {
    const button = event.target.closest("[data-calm-response]");
    if (!button) return;
    responseStatus.textContent = `${button.dataset.calmResponse}. Nothing was saved or reported.`;
  });

  document.querySelector("[data-calm-reset]").addEventListener("click", () => {
    form.reset();
    empty.hidden = false;
    plan.hidden = true;
    responseStatus.textContent = "";
    status.textContent = "The synthetic scenario was reset.";
    form.elements.reason.focus();
  });
})();
