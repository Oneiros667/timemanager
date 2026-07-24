(() => {
  "use strict";

  const registerServiceWorker = () => {
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
  setupLowCapacityMode();
  setupCaptureShortcut();
  setupFocusTimer();
})();
