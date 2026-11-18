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
