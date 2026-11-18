(() => {
  const toggle = document.querySelector(".menu-toggle");
  const links = document.querySelector(".site-links");
  if (toggle && links) {
    const closeMenu = () => {
      toggle.setAttribute("aria-expanded", "false");
      toggle.textContent = "Menu";
      links.removeAttribute("data-open");
    };
    toggle.addEventListener("click", () => {
      const isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      toggle.textContent = isOpen ? "Menu" : "Close";
      links.toggleAttribute("data-open", !isOpen);
    });
    links.addEventListener("click", (e) => {
      if (e.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", (e) => {
      if (
        e.key === "Escape" &&
        toggle.getAttribute("aria-expanded") === "true"
      ) {
        closeMenu();
        toggle.focus();
      }
    });
  }
  const activate = (group, tab, focus = false) => {
    group.querySelectorAll("[role=tab]").forEach((button) => {
      const selected = button === tab;
      button.setAttribute("aria-selected", String(selected));
      button.tabIndex = selected ? 0 : -1;
      const panel = document.getElementById(
        button.getAttribute("aria-controls"),
      );
      if (panel) panel.hidden = !selected;
    });
    if (focus) tab.focus();
  };
  document.querySelectorAll("[role=tablist]").forEach((group) => {
    group.addEventListener("click", (e) => {
      const tab = e.target.closest("[role=tab]");
      if (tab) activate(group, tab);
    });
    group.addEventListener("keydown", (e) => {
      const tabs = [...group.querySelectorAll("[role=tab]")];
      const index = tabs.indexOf(document.activeElement);
      if (index < 0) return;
      let next;
      if (e.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (e.key === "ArrowLeft") next = (index + tabs.length - 1) % tabs.length;
      if (e.key === "Home") next = 0;
      if (e.key === "End") next = tabs.length - 1;
      if (next !== undefined) {
        e.preventDefault();
        activate(group, tabs[next], true);
      }
    });
  });
})();

// Progressive enhancement: the standard form POST remains available without JS.
(() => {
  const form = document.querySelector(".waitlist-form");
  if (!form || !window.fetch || !window.AbortController) return;
  const email = form.querySelector('input[type="email"]');
  const submit = form.querySelector('button[type="submit"]');
  const status = form.querySelector(".waitlist-status");
  let sending = false;
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (sending || form.dataset.state === "success") return;
    if (!form.reportValidity()) return;
    if (form.elements._honey.value) return;
    sending = true;
    submit.disabled = true;
    submit.textContent = "Joining…";
    form.dataset.state = "sending";
    form.setAttribute("aria-busy", "true");
    status.textContent = "";
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const data = Object.fromEntries(new FormData(form));
      data.email = data.email.trim();
      const endpoint = form.action.replace(
        "https://formsubmit.co/",
        "https://formsubmit.co/ajax/",
      );
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(data),
        signal: controller.signal,
      });
      if (!response.ok) throw new Error("Submission unavailable");
      const result = await response.json();
      if (result.success !== true && result.success !== "true")
        throw new Error("Submission not confirmed");
      form.dataset.state = "success";
      email.disabled = true;
      submit.textContent = "You’re on the list";
      status.textContent =
        "We’ll email you when Torah Lock launches on Android.";
    } catch (error) {
      form.dataset.state = "error";
      status.replaceChildren(
        document.createTextNode(
          "We couldn’t confirm your signup. Please try again, or ",
        ),
      );
      const contact = document.createElement("a");
      contact.href =
        "mailto:support@torahlock.app?subject=Torah%20Lock%20Android%20waitlist";
      contact.textContent = "email us";
      status.append(contact, document.createTextNode("."));
      submit.disabled = false;
      submit.textContent = "Try again";
    } finally {
      clearTimeout(timeout);
      sending = false;
      form.removeAttribute("aria-busy");
    }
  });
})();
