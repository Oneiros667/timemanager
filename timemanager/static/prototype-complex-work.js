(() => {
  "use strict";

  const root = document.querySelector(".prototype-page");
  if (!root) return;

  const announce = (message) => {
    const status = document.querySelector("[data-prototype-status]");
    if (status) status.textContent = message;
  };

  const showView = (name) => {
    document.querySelectorAll("[data-prototype-panel]").forEach((panel) => {
      panel.hidden = panel.getAttribute("data-prototype-panel") !== name;
    });
    document.querySelectorAll("[data-prototype-view]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.getAttribute("data-prototype-view") === name));
    });
    document.querySelector(`[data-prototype-panel="${name}"]`)?.querySelector("button, input")?.focus();
  };

  document.querySelectorAll("[data-prototype-view]").forEach((button) => {
    button.addEventListener("click", () => showView(button.getAttribute("data-prototype-view")));
  });
  document.querySelectorAll("[data-open-task]").forEach((button) => button.addEventListener("click", () => showView("task")));
  document.querySelectorAll("[data-open-project]").forEach((button) => button.addEventListener("click", () => showView("project")));

  document.querySelector("[data-prototype-capture]")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const input = event.currentTarget.elements.title;
    const title = input.value.trim();
    if (!title) return;
    const row = document.createElement("article");
    row.className = "task-row prototype-task-row";
    const copy = document.createElement("div");
    copy.className = "task-copy";
    const name = document.createElement("span");
    name.textContent = title;
    const context = document.createElement("span");
    context.textContent = "Captured just now";
    const details = document.createElement("button");
    details.type = "button";
    details.className = "text-button";
    details.textContent = "Add details";
    details.addEventListener("click", () => showView("task"));
    copy.append(name, context, details);
    row.append(copy);
    document.querySelector("[data-prototype-captured]")?.append(row);
    input.value = "";
    input.focus();
    announce(`Captured ${title}. Add details is available.`);
  });

  document.querySelector("[data-prototype-low-capacity]")?.addEventListener("click", (event) => {
    const enabled = document.body.classList.toggle("low-capacity");
    event.currentTarget.setAttribute("aria-pressed", String(enabled));
    event.currentTarget.textContent = enabled ? "Standard view" : "Low capacity";
    announce(enabled ? "Low Capacity presentation enabled." : "Standard presentation enabled.");
  });

  const inlineEditor = document.querySelector("[data-inline-editor]");
  document.querySelector("[data-inline-edit]")?.addEventListener("click", () => {
    if (inlineEditor) {
      inlineEditor.hidden = !inlineEditor.hidden;
      if (!inlineEditor.hidden) inlineEditor.querySelector("input")?.focus();
    }
  });
  inlineEditor?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(inlineEditor);
    document.querySelector("[data-open-task]").textContent = data.get("title");
    document.querySelector("[data-today-secondary]").textContent = `Next: ${data.get("next_action")}`;
    const state = document.querySelector("[data-inline-save-state]");
    if (state) state.textContent = "Saved";
    announce("Task details saved in this prototype.");
  });

  const setupSyntheticAutosave = (selector, stateSelector) => {
    let timer;
    document.querySelectorAll(selector).forEach((field) => {
      field.addEventListener("input", () => {
        const status = document.querySelector(stateSelector);
        if (status) status.textContent = "Saving…";
        window.clearTimeout(timer);
        timer = window.setTimeout(() => {
          if (status) status.textContent = "Saved";
          announce("Changes saved in this prototype.");
        }, 750);
      });
      field.addEventListener("blur", () => {
        window.clearTimeout(timer);
        const status = document.querySelector(stateSelector);
        if (status) status.textContent = "Saved";
      });
    });
  };
  setupSyntheticAutosave("[data-prototype-title], [data-prototype-next], [data-prototype-done]", "[data-save-state]");
  setupSyntheticAutosave("[data-prototype-project-title], [data-prototype-outcome]", "[data-project-save-state]");

  const addListItem = (list, value) => {
    const item = document.createElement("li");
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.textContent = "○";
    toggle.setAttribute("aria-label", `Mark ${value} complete`);
    const text = document.createElement("span");
    text.textContent = value;
    const edit = document.createElement("button");
    edit.type = "button";
    edit.textContent = "Edit";
    edit.addEventListener("click", () => {
      const editor = document.createElement("input");
      editor.value = text.textContent;
      editor.setAttribute("aria-label", `Edit ${text.textContent}`);
      text.replaceWith(editor);
      editor.focus();
      const saveEdit = () => {
        const revised = editor.value.trim() || value;
        text.textContent = revised;
        editor.replaceWith(text);
        announce(`Step updated to ${revised}.`);
      };
      editor.addEventListener("blur", saveEdit, { once: true });
      editor.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          editor.blur();
        }
      });
    });
    item.append(toggle, text, edit);
    list.append(item);
    toggle.addEventListener("click", () => {
      const complete = toggle.textContent === "✓";
      toggle.textContent = complete ? "○" : "✓";
      item.classList.toggle("is-complete", !complete);
      announce(`${value} ${complete ? "restored" : "completed"}.`);
    });
  };

  document.querySelector("[data-step-form]")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const input = event.currentTarget.elements.step;
    const value = input.value.trim();
    if (!value) return;
    addListItem(document.querySelector("[data-prototype-steps]"), value);
    input.value = "";
    input.focus();
    announce(`Added step: ${value}.`);
  });

  document.querySelector("[data-project-task-form]")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const input = event.currentTarget.elements.task;
    const value = input.value.trim();
    if (!value) return;
    const item = document.createElement("article");
    const text = document.createElement("span");
    text.textContent = value;
    item.append(text);
    document.querySelector("[data-project-ready]").append(item);
    input.value = "";
    input.focus();
    announce(`Added project task: ${value}.`);
  });

  document.querySelector("[data-add-blocker]")?.addEventListener("click", () => {
    const form = document.querySelector("[data-blocker-form]");
    if (form) {
      form.hidden = false;
      form.querySelector("input[name=reason]")?.focus();
    }
  });
  document.querySelector("[data-blocker-form]")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const label = data.get("kind") === "task" ? "Needs" : "Waiting for";
    document.querySelector("[data-blocker-summary]").innerHTML = `<p>${label}: ${String(data.get("reason")).replace(/[<>&]/g, "")}</p>`;
    event.currentTarget.hidden = true;
    announce("Blocker added. Today was not rearranged.");
  });

  document.querySelector("[data-complete-prerequisite]")?.addEventListener("click", (event) => {
    event.currentTarget.textContent = "Completed";
    document.querySelector("[data-next-ready]").textContent = "Gather invoices";
    announce("Prerequisite completed. Gather invoices is ready but was not added to Today.");
  });
  document.querySelector("[data-remove-blocker]")?.addEventListener("click", (event) => {
    const task = event.currentTarget.closest("article");
    document.querySelector("[data-project-ready]").append(task);
    task.querySelector("small")?.remove();
    event.currentTarget.remove();
    announce("Blocker removed. The task is ready and remains outside Today.");
  });
  document.querySelector("[data-keep-blocked]")?.addEventListener("click", () => {
    announce("Blocked task kept in Today.");
  });
  document.querySelector("[data-replace-blocked]")?.addEventListener("click", (event) => {
    event.currentTarget.closest("article")?.remove();
    announce("Blocked task removed from Today. Choose a replacement when ready.");
  });
  document.querySelector("[data-remove-today-blocker]")?.addEventListener("click", (event) => {
    const task = event.currentTarget.closest("article");
    task?.classList.remove("is-blocked");
    task?.querySelector(".task-copy span")?.replaceChildren("Ready when you are");
    event.currentTarget.remove();
    announce("Blocker removed. The task stayed in Today.");
  });

  const promotionDialog = document.querySelector("[data-promotion-dialog]");
  document.querySelector("[data-promote-step]")?.addEventListener("click", () => promotionDialog?.showModal());
  document.querySelector("[data-confirm-promotion]")?.addEventListener("click", () => {
    announce("Step promoted to a project task after Prepare tax return.");
  });

  document.querySelector("[data-prototype-reset]")?.addEventListener("click", () => window.location.reload());
})();
