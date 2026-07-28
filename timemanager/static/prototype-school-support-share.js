(() => {
  const form = document.querySelector("[data-school-share-form]");
  if (!form) return;

  const medicationInput = form.querySelector('[value="Medication administration plan"]');
  const warning = document.querySelector("[data-role-warning]");
  const empty = document.querySelector("[data-school-empty]");
  const preview = document.querySelector("[data-school-preview]");
  const result = document.querySelector("[data-school-result]");
  const status = document.querySelector("[data-school-status]");

  function updateRoleBoundary() {
    const healthProfessional =
      form.elements.recipient.value === "School health professional";
    medicationInput.disabled = !healthProfessional;
    if (!healthProfessional) medicationInput.checked = false;
    warning.hidden = healthProfessional;
  }

  form.elements.recipient.forEach((input) => {
    input.addEventListener("change", updateRoleBoundary);
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const fields = data.getAll("field");
    if (fields.length === 0) {
      status.textContent = "Select at least one field to disclose.";
      form.querySelector('[name="field"]').focus();
      return;
    }

    document.querySelector("[data-school-recipient]").textContent =
      String(data.get("recipient"));
    document.querySelector("[data-school-purpose]").textContent =
      String(data.get("purpose"));
    document.querySelector("[data-school-expiry]").textContent =
      String(data.get("expiry"));
    document.querySelector("[data-school-fields]").replaceChildren(
      ...fields.map((text) => {
        const item = document.createElement("li");
        item.textContent = text;
        return item;
      }),
    );
    document.querySelector("[data-school-medication-note]").hidden =
      !fields.includes("Medication administration plan");
    document.querySelector("[data-school-preview-title]").textContent =
      "Disclosure preview";
    empty.hidden = true;
    preview.hidden = false;
    result.textContent = "";
    status.textContent = "Disclosure preview ready. Nothing has been shared.";
    document.querySelector("[data-school-confirm]").focus();
  });

  document.querySelector("[data-school-confirm]").addEventListener("click", () => {
    result.textContent =
      "Synthetic share confirmed. No invitation, record, or message was created.";
  });

  document.querySelector("[data-school-edit]").addEventListener("click", () => {
    form.elements.recipient[0].focus();
  });

  document.querySelector("[data-school-reset]").addEventListener("click", () => {
    form.reset();
    updateRoleBoundary();
    empty.hidden = false;
    preview.hidden = true;
    document.querySelector("[data-school-preview-title]").textContent =
      "Nothing has been shared";
    result.textContent = "";
    status.textContent = "The synthetic scenario was reset.";
    form.elements.recipient[0].focus();
  });

  const signalPreview = document.querySelector("[data-child-signal-preview]");
  const signalResult = document.querySelector("[data-child-signal-result]");
  const signalMessage = document.querySelector("[data-child-signal-message]");

  document.querySelector("[data-child-signal-options]").addEventListener(
    "click",
    (event) => {
      const button = event.target.closest("[data-child-signal]");
      if (!button) return;
      signalMessage.textContent = button.dataset.childSignal;
      signalPreview.hidden = false;
      signalResult.textContent = "";
      document.querySelector("[data-child-signal-confirm]").focus();
    },
  );

  document.querySelector("[data-child-signal-confirm]").addEventListener(
    "click",
    () => {
      signalResult.textContent =
        "Synthetic message confirmed. No person was contacted and nothing was saved.";
    },
  );

  document.querySelector("[data-child-signal-cancel]").addEventListener(
    "click",
    () => {
      signalPreview.hidden = true;
      signalResult.textContent = "Message cancelled.";
      document.querySelector("[data-child-signal-options] button").focus();
    },
  );

  updateRoleBoundary();
})();
