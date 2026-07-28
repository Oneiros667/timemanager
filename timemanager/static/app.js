(() => {
  "use strict";
  document.documentElement.classList.add("js");

  const DRAFT_STORAGE_PREFIX = "timemanager-draft-v1:";
  const DRAFT_TAB_STORAGE_KEY = "timemanager-draft-tab-v1";
  const DRAFT_MAX_AGE_MS = 24 * 60 * 60 * 1000;
  let fallbackDraftTabId = null;

  const draftAccount = () => document.body.dataset.draftAccount || "";

  const draftTabId = () => {
    try {
      let tabId = window.sessionStorage.getItem(DRAFT_TAB_STORAGE_KEY);
      if (!tabId) {
        tabId = window.crypto.randomUUID();
        window.sessionStorage.setItem(DRAFT_TAB_STORAGE_KEY, tabId);
      }
      return tabId;
    } catch (_error) {
      fallbackDraftTabId ||= window.crypto.randomUUID();
      return fallbackDraftTabId;
    }
  };

  const draftScopePrefix = (scope) => {
    const account = draftAccount();
    return account && scope
      ? `${DRAFT_STORAGE_PREFIX}${account}:${scope}:`
      : null;
  };

  const draftKey = (scope) => {
    const scopePrefix = draftScopePrefix(scope);
    return scopePrefix ? `${scopePrefix}${draftTabId()}` : null;
  };

  const removeStoredDraft = (key) => {
    if (!key) return;
    try {
      window.localStorage.removeItem(key);
    } catch (_error) {
      // Autosave remains usable when browser storage is unavailable.
    }
  };

  const readStoredDraft = (key) => {
    if (!key) return null;
    try {
      const serialized = window.localStorage.getItem(key);
      if (!serialized) return null;
      const draft = JSON.parse(serialized);
      if (
        draft.version !== 1
        || !Number.isFinite(draft.savedAt)
        || Date.now() - draft.savedAt > DRAFT_MAX_AGE_MS
        || typeof draft.fields !== "object"
        || draft.fields === null
      ) {
        removeStoredDraft(key);
        return null;
      }
      return draft;
    } catch (_error) {
      removeStoredDraft(key);
      return null;
    }
  };

  const readNewestStoredDraft = (scope, preferredKey) => {
    const scopePrefix = draftScopePrefix(scope);
    if (!scopePrefix) return null;
    try {
      const candidates = [];
      for (let index = 0; index < window.localStorage.length; index += 1) {
        const key = window.localStorage.key(index);
        if (!key?.startsWith(scopePrefix)) continue;
        const draft = readStoredDraft(key);
        if (draft) candidates.push({ key, draft });
      }
      return candidates.find(({ key }) => key === preferredKey)
        || candidates.sort((left, right) => (
          right.draft.savedAt - left.draft.savedAt
        ))[0]
        || null;
    } catch (_error) {
      return null;
    }
  };

  const clearAccountDrafts = () => {
    const accountPrefix = `${DRAFT_STORAGE_PREFIX}${draftAccount()}:`;
    if (!draftAccount()) return;
    try {
      for (let index = window.localStorage.length - 1; index >= 0; index -= 1) {
        const key = window.localStorage.key(index);
        if (key?.startsWith(accountPrefix)) {
          window.localStorage.removeItem(key);
        }
      }
    } catch (_error) {
      // Sign-out still proceeds when browser storage is unavailable.
    }
  };

  const pruneExpiredDrafts = () => {
    try {
      const keys = [];
      for (let index = 0; index < window.localStorage.length; index += 1) {
        const key = window.localStorage.key(index);
        if (key?.startsWith(DRAFT_STORAGE_PREFIX)) {
          keys.push(key);
        }
      }
      keys.forEach((key) => readStoredDraft(key));
    } catch (_error) {
      // Autosave remains usable when browser storage is unavailable.
    }
  };

  const setupDraftClearing = () => {
    pruneExpiredDrafts();
    document.querySelectorAll("form[data-clear-drafts]").forEach((form) => {
      form.addEventListener("submit", () => {
        document.body.dataset.draftsDiscarding = "true";
        clearAccountDrafts();
      });
    });
  };

  const registerServiceWorker = () => {
    if (document.body.classList.contains("prototype-page")) {
      return;
    }
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker.register("/sw.js").catch(() => {
          // The app remains usable when service workers are unavailable.
        });
      });
    }
  };

  const setupFlashes = () => {
    document.querySelectorAll("[data-dismiss-flash]").forEach((button) => {
      button.addEventListener("click", () => button.closest(".flash")?.remove());
    });
  };

  const setupLowCapacityMode = () => {
    const toggle = document.querySelector("[data-mode-toggle]");
    if (!toggle) {
      return;
    }

    const label = toggle.querySelector("[data-mode-label]");
    const applyMode = (enabled) => {
      document.body.classList.toggle("low-capacity", enabled);
      toggle.setAttribute("aria-pressed", String(enabled));
      if (label) {
        label.textContent = enabled ? "Standard view" : "Low capacity";
      }
    };

    let enabled = false;
    try {
      enabled = window.localStorage.getItem("timemanager-low-capacity") === "true";
    } catch (_error) {
      enabled = false;
    }
    applyMode(enabled);

    toggle.addEventListener("click", () => {
      enabled = !enabled;
      applyMode(enabled);
      try {
        window.localStorage.setItem("timemanager-low-capacity", String(enabled));
      } catch (_error) {
        // The view still works when storage is unavailable.
      }
    });
  };

  const setupCaptureShortcut = () => {
    const capture = document.querySelector("#capture-title");
    if (!capture) {
      return;
    }

    document.addEventListener("keydown", (event) => {
      const target = event.target;
      const isTyping = target instanceof HTMLInputElement
        || target instanceof HTMLTextAreaElement
        || target instanceof HTMLSelectElement;
      if (!isTyping && !event.metaKey && !event.ctrlKey && event.key.toLowerCase() === "q") {
        event.preventDefault();
        capture.focus();
      }
    });
  };

  const setupConfirmations = () => {
    document.querySelectorAll("form[data-confirm]").forEach((form) => {
      form.addEventListener("submit", (event) => {
        if (!window.confirm(form.getAttribute("data-confirm") || "Continue?")) {
          event.preventDefault();
          return;
        }
        const fieldName = form.getAttribute("data-confirm-field");
        if (fieldName && !form.elements.namedItem(fieldName)) {
          const confirmation = document.createElement("input");
          confirmation.type = "hidden";
          confirmation.name = fieldName;
          confirmation.value = "1";
          form.append(confirmation);
        }
      });
    });
  };

  const setupInlineEditors = () => {
    document.querySelectorAll("[data-inline-edit-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        const editor = document.querySelector(
          `[data-inline-edit="${button.getAttribute("data-inline-edit-toggle")}"]`,
        );
        if (!editor) return;
        editor.hidden = !editor.hidden;
        if (!editor.hidden) {
          editor.querySelector("input:not([type=hidden])")?.focus();
        } else {
          button.focus();
        }
      });
    });
  };

  const setupDependencySearch = () => {
    document.querySelectorAll("[data-dependency-search]").forEach((search) => {
      const form = search.closest("form");
      const select = form?.querySelector("select[name=prerequisite_task_id]");
      if (!(select instanceof HTMLSelectElement)) return;
      const options = [...select.options];
      search.addEventListener("input", () => {
        const query = search.value.trim().toLowerCase();
        options.forEach((option, index) => {
          option.hidden = index > 0 && !option.text.toLowerCase().includes(query);
        });
        const firstMatch = options.find((option, index) => index > 0 && !option.hidden);
        if (query && firstMatch) select.value = firstMatch.value;
      });
    });
  };

  const setupAutosave = () => {
    document.querySelectorAll("[data-autosave-form]").forEach((form) => {
      const status = form.querySelector("[data-save-state]");
      const revision = form.querySelector("[data-revision]");
      const storageKey = draftKey(form.dataset.draftScope);
      let restoredSourceKey = null;
      const fields = [...form.querySelectorAll(
        "input:not([type=hidden]):not([type=submit]):not([type=button]), textarea, select",
      )].filter((field) => field.name);
      let timer = null;
      let saving = false;
      let dirty = false;
      let changeVersion = 0;
      let requiresExplicitSave = false;

      const captureFields = () => Object.fromEntries(
        fields.map((field) => [
          field.name,
          field instanceof HTMLInputElement && field.type === "checkbox"
            ? field.checked
            : field.value,
        ]),
      );

      const applyFields = (values) => {
        fields.forEach((field) => {
          if (!Object.hasOwn(values, field.name)) return;
          if (field instanceof HTMLInputElement && field.type === "checkbox") {
            field.checked = Boolean(values[field.name]);
          } else if (typeof values[field.name] === "string") {
            field.value = values[field.name];
          }
        });
      };

      let savedFields = captureFields();

      const persistDraft = () => {
        if (!storageKey) return;
        try {
          window.localStorage.setItem(storageKey, JSON.stringify({
            version: 1,
            savedAt: Date.now(),
            revision: Number(revision?.value || 0),
            requiresExplicitSave,
            fields: captureFields(),
          }));
        } catch (_error) {
          // Network autosave remains the fallback when storage is unavailable.
        }
      };

      const fieldsMatch = (left, right) => (
        JSON.stringify(left) === JSON.stringify(right)
      );

      const clearDraft = ({ acknowledgedFields = null } = {}) => {
        removeStoredDraft(storageKey);
        if (!restoredSourceKey || restoredSourceKey === storageKey) return;
        const sourceDraft = readStoredDraft(restoredSourceKey);
        if (
          acknowledgedFields
          && sourceDraft
          && fieldsMatch(sourceDraft.fields, acknowledgedFields)
        ) {
          removeStoredDraft(restoredSourceKey);
        }
      };

      const renderActions = (message, actions) => {
        if (!status) return;
        status.textContent = `${message} `;
        actions.forEach(({ label, run }) => {
          const button = document.createElement("button");
          button.type = "button";
          button.className = "text-button";
          button.textContent = label;
          button.addEventListener("click", run);
          status.append(button);
        });
      };

      const renderFailure = (message) => {
        renderActions("", [{
          label: `${message} — Retry`,
          run: () => save(),
        }]);
      };

      const discardDraft = () => {
        window.clearTimeout(timer);
        applyFields(savedFields);
        clearDraft();
        removeStoredDraft(restoredSourceKey);
        dirty = false;
        saving = false;
        requiresExplicitSave = false;
        if (status) status.textContent = "Saved";
      };

      const renderConflict = (currentTitle = "") => {
        const currentCopy = currentTitle
          ? ` Current saved title: “${currentTitle}”.`
          : "";
        renderActions(
          `Saved version changed.${currentCopy} Draft restored but not saved.`,
          [
            {
              label: "Save this draft",
              run: () => {
                requiresExplicitSave = false;
                persistDraft();
                save({ explicit: true });
              },
            },
            { label: "Discard draft", run: discardDraft },
          ],
        );
      };

      const save = async ({ explicit = false } = {}) => {
        window.clearTimeout(timer);
        if (saving || !dirty) return;
        if (requiresExplicitSave && !explicit) {
          renderConflict();
          return;
        }
        const savingVersion = changeVersion;
        const submittedFields = captureFields();
        saving = true;
        if (status) status.textContent = "Saving…";
        try {
          const response = await window.fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: {
              Accept: "application/json",
              "X-Requested-With": "fetch",
            },
          });
          const result = await response.json();
          if (response.status === 409) {
            if (revision) revision.value = String(result.revision);
            if (result.current && typeof result.current === "object") {
              savedFields = { ...savedFields, ...result.current };
            }
            requiresExplicitSave = true;
            persistDraft();
            renderConflict(result.current?.title || "");
            return;
          }
          if (!response.ok) throw new Error("save failed");
          if (revision) revision.value = String(result.revision);
          if (form.querySelector("[data-task-revision]")) {
            document.querySelectorAll("[data-task-revision]").forEach((field) => {
              field.value = String(result.revision);
            });
          }
          if (form.querySelector("[data-project-revision]")) {
            document.querySelectorAll("[data-project-revision]").forEach((field) => {
              field.value = String(result.revision);
            });
          }
          dirty = changeVersion !== savingVersion;
          requiresExplicitSave = false;
          savedFields = submittedFields;
          if (dirty) {
            persistDraft();
          } else {
            clearDraft({ acknowledgedFields: submittedFields });
          }
          if (status) status.textContent = dirty ? "Unsaved" : "Saved";
        } catch (_error) {
          persistDraft();
          renderFailure("Couldn’t save");
        } finally {
          saving = false;
          if (
            dirty
            && changeVersion !== savingVersion
            && !requiresExplicitSave
          ) {
            timer = window.setTimeout(save, 750);
          }
        }
      };

      const storedCandidate = readNewestStoredDraft(
        form.dataset.draftScope,
        storageKey,
      );
      const storedDraft = storedCandidate?.draft;
      if (storedDraft) {
        restoredSourceKey = storedCandidate.key;
        applyFields(storedDraft.fields);
        form.hidden = false;
        dirty = true;
        changeVersion = 1;
        const currentRevision = Number(revision?.value || 0);
        requiresExplicitSave = Boolean(storedDraft.requiresExplicitSave)
          || storedDraft.revision !== currentRevision;
        if (requiresExplicitSave) {
          renderConflict();
        } else {
          renderActions(
            "Unsaved draft restored.",
            [{ label: "Save now", run: () => save({ explicit: true }) }],
          );
        }
      }

      fields.forEach((field) => {
        field.addEventListener("input", () => {
          changeVersion += 1;
          dirty = true;
          persistDraft();
          window.clearTimeout(timer);
          if (requiresExplicitSave) {
            renderConflict();
          } else {
            if (status) status.textContent = "Unsaved";
            timer = window.setTimeout(save, 750);
          }
        });
        field.addEventListener("blur", save);
      });
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        changeVersion += 1;
        dirty = true;
        persistDraft();
        save({ explicit: true });
      });
      window.addEventListener("beforeunload", (event) => {
        if (
          (dirty || saving)
          && document.body.dataset.draftsDiscarding !== "true"
        ) {
          event.preventDefault();
          event.returnValue = "";
        }
      });
    });
  };

  const setupRapidEntry = () => {
    document.querySelectorAll("[data-rapid-entry]").forEach((form) => {
      const input = form.querySelector("input[name=title]");
      const status = form.querySelector("[data-rapid-status]");
      if (!input) return;
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const title = input.value.trim();
        if (!title) return;
        if (status) status.textContent = "Adding…";
        try {
          const response = await window.fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: {
              Accept: "application/json",
              "X-Requested-With": "fetch",
            },
          });
          if (!response.ok) throw new Error("add failed");
          const result = await response.json();
          if (result.task_revision) {
            document.querySelectorAll("[data-task-revision]").forEach((field) => {
              field.value = String(result.task_revision);
            });
          }
          if (result.project_revision) {
            document.querySelectorAll("[data-project-revision]").forEach((field) => {
              field.value = String(result.project_revision);
            });
          }
          input.value = "";
          input.focus();
          if (status) status.textContent = `Added “${title}”`;
          let list = form.parentElement?.querySelector(".component-list")
            || document.querySelector(".project-task-list");
          if (list) {
            if (list.matches(".component-list") && list.children.length >= 3) {
              let overflow = form.parentElement?.querySelector("details[data-component-overflow]");
              if (!overflow) {
                overflow = document.createElement("details");
                overflow.setAttribute("data-component-overflow", "");
                const summary = document.createElement("summary");
                const overflowList = document.createElement("ol");
                overflowList.className = "component-list";
                overflowList.start = 4;
                overflow.append(summary, overflowList);
                form.before(overflow);
              }
              list = overflow.querySelector(".component-list");
              const summary = overflow.querySelector("summary");
              if (summary) {
                const count = list.children.length + 1;
                summary.textContent = `${count} more ${count === 1 ? "step" : "steps"}`;
              }
            }
            if (result.html && list.matches(".component-list")) {
              list.insertAdjacentHTML("beforeend", result.html);
            } else {
              const item = document.createElement(list.tagName === "OL" ? "li" : "article");
              item.className = "newly-added";
              const copy = document.createElement("span");
              copy.textContent = title;
              item.append(copy);
              list.append(item);
            }
          }
        } catch (_error) {
          if (status) status.textContent = "Couldn’t add — your text is still here";
        }
      });
    });
    document.querySelector("[data-focus-rapid-entry]")?.addEventListener("click", () => {
      document.querySelector("[data-rapid-entry] input[name=title]")?.focus();
    });
  };

  const setupFocusTimer = () => {
    const dialog = document.querySelector("#focus-dialog");
    if (!(dialog instanceof HTMLDialogElement)) {
      return;
    }

    const title = dialog.querySelector("[data-focus-title]");
    const display = dialog.querySelector("[data-timer-display]");
    const toggle = dialog.querySelector("[data-timer-toggle]");
    const reset = dialog.querySelector("[data-timer-reset]");
    const note = dialog.querySelector("[data-timer-note]");
    const durationButtons = [...dialog.querySelectorAll("[data-duration]")];
    let selectedSeconds = 5 * 60;
    let remainingSeconds = selectedSeconds;
    let timerId = null;
    let deadline = null;

    const render = () => {
      const minutes = Math.floor(remainingSeconds / 60);
      const seconds = remainingSeconds % 60;
      if (display) {
        display.textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
      }
    };

    const pause = () => {
      if (timerId !== null) {
        window.clearInterval(timerId);
        timerId = null;
      }
      deadline = null;
      if (toggle) {
        toggle.textContent = remainingSeconds === selectedSeconds ? "Start" : "Continue";
      }
    };

    const finish = () => {
      pause();
      remainingSeconds = 0;
      render();
      if (toggle) {
        toggle.textContent = "Continue";
      }
      if (note) {
        note.textContent = "Boundary reached. Continue, pause, or stop—you choose.";
      }
    };

    const tick = () => {
      if (deadline === null) {
        return;
      }
      remainingSeconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      render();
      if (remainingSeconds === 0) {
        finish();
      }
    };

    const start = () => {
      if (remainingSeconds === 0) {
        remainingSeconds = selectedSeconds;
      }
      deadline = Date.now() + remainingSeconds * 1000;
      timerId = window.setInterval(tick, 250);
      if (toggle) {
        toggle.textContent = "Pause";
      }
      if (note) {
        note.textContent = "You only need to stay with this moment.";
      }
    };

    const resetTimer = () => {
      pause();
      remainingSeconds = selectedSeconds;
      render();
      if (note) {
        note.textContent = "Starting is the win.";
      }
    };

    document.querySelectorAll("[data-focus-task]").forEach((button) => {
      button.addEventListener("click", () => {
        if (title) {
          title.textContent = button.getAttribute("data-focus-task") || "Focus session";
        }
        resetTimer();
        dialog.showModal();
      });
    });

    durationButtons.forEach((button) => {
      button.addEventListener("click", () => {
        selectedSeconds = Number(button.getAttribute("data-duration")) * 60;
        durationButtons.forEach((candidate) => {
          candidate.setAttribute("aria-pressed", String(candidate === button));
        });
        resetTimer();
      });
    });

    toggle?.addEventListener("click", () => {
      if (timerId === null) {
        start();
      } else {
        tick();
        pause();
        if (note) {
          note.textContent = "Paused. Return when you are ready.";
        }
      }
    });
    reset?.addEventListener("click", resetTimer);
    dialog.querySelector("[data-focus-close]")?.addEventListener("click", () => {
      pause();
      dialog.close();
    });
    dialog.addEventListener("cancel", pause);
    render();
  };

  registerServiceWorker();
  setupFlashes();
  setupDraftClearing();
  setupLowCapacityMode();
  setupCaptureShortcut();
  setupConfirmations();
  setupInlineEditors();
  setupDependencySearch();
  setupAutosave();
  setupRapidEntry();
  setupFocusTimer();
})();
