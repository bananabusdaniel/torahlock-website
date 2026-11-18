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

// Native scrolling supports swipe without JavaScript; controls add keyboard access.
(() => {
  document.querySelectorAll(".review-carousel").forEach((carousel) => {
    const track = carousel.querySelector(".review-track");
    const cards = [...carousel.querySelectorAll(".review-card")];
    const controls = carousel.querySelector(".review-controls");
    const position = carousel.querySelector(".review-position");
    if (!track || cards.length < 2 || !controls) return;
    const mobile = window.matchMedia("(max-width: 760px)");
    const cardPosition = (card) =>
      card.getBoundingClientRect().left -
      track.getBoundingClientRect().left +
      track.scrollLeft;
    const currentIndex = () =>
      cards.reduce(
        (best, card, index) =>
          Math.abs(cardPosition(card) - track.scrollLeft) <
          Math.abs(cardPosition(cards[best]) - track.scrollLeft)
            ? index
            : best,
        0,
      );
    const update = () => {
      const index = currentIndex();
      position.textContent = `${index + 1} of ${cards.length}`;
      cards.forEach((card, i) =>
        card.setAttribute("aria-current", String(i === index)),
      );
    };
    const move = (step) => {
      if (!mobile.matches) return;
      const index = (currentIndex() + step + cards.length) % cards.length;
      track.scrollTo({
        left: cardPosition(cards[index]),
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth",
      });
    };
    carousel
      .querySelector(".review-previous")
      .addEventListener("click", () => move(-1));
    carousel
      .querySelector(".review-next")
      .addEventListener("click", () => move(1));
    track.addEventListener("scroll", update, { passive: true });
    track.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
        event.preventDefault();
        move(event.key === "ArrowRight" ? 1 : -1);
      }
    });
    const syncMode = () => {
      controls.hidden = !mobile.matches;
      track.tabIndex = mobile.matches ? 0 : -1;
      track.setAttribute(
        "aria-label",
        mobile.matches
          ? "Swipe or use arrow keys to browse reviews"
          : "App Store review",
      );
      carousel.setAttribute(
        "aria-label",
        mobile.matches ? "Five-star App Store reviews" : "App Store review",
      );
      if (mobile.matches) {
        carousel.setAttribute("aria-roledescription", "carousel");
        carousel.dataset.enhanced = "true";
      } else {
        carousel.removeAttribute("aria-roledescription");
        delete carousel.dataset.enhanced;
      }
      cards.forEach((card, index) => {
        card.hidden = !mobile.matches && index > 0;
        if (mobile.matches) {
          card.setAttribute("aria-roledescription", "slide");
          card.setAttribute("aria-label", `${index + 1} of ${cards.length}`);
        } else {
          card.removeAttribute("aria-roledescription");
          card.removeAttribute("aria-label");
        }
      });
      track.scrollTo({ left: 0, behavior: "auto" });
      update();
    };
    mobile.addEventListener("change", syncMode);
    syncMode();
  });
})();
