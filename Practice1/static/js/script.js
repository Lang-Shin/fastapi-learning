document.addEventListener("DOMContentLoaded", () => {
  initChecklistToggle();
  initStepsToggle();
  initSearch();
});

/**
 * Clicking an ingredient toggles its "completed" class,
 * which CSS uses to fill the checkbox and strike the text.
 */
function initChecklistToggle() {
  const list = document.getElementById("ingredients-list");
  if (!list) return;

  list.querySelectorAll(".checklist__item").forEach((item) => {
    item.setAttribute("tabindex", "0");
    item.setAttribute("role", "checkbox");
    item.setAttribute("aria-checked", "false");

    const toggle = () => {
      item.classList.toggle("completed");
      const isChecked = item.classList.contains("completed");
      item.setAttribute("aria-checked", isChecked ? "true" : "false");
    };

    item.addEventListener("click", toggle);
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggle();
      }
    });
  });
}

/**
 * Same idea for cooking steps — click a step to cross it off
 * as you work through the recipe.
 */
function initStepsToggle() {
  const list = document.getElementById("steps-list");
  if (!list) return;

  list.querySelectorAll(".steps__item").forEach((item) => {
    item.setAttribute("tabindex", "0");
    item.setAttribute("role", "checkbox");
    item.setAttribute("aria-checked", "false");

    const toggle = () => {
      item.classList.toggle("completed");
      const isChecked = item.classList.contains("completed");
      item.setAttribute("aria-checked", isChecked ? "true" : "false");
    };

    item.addEventListener("click", toggle);
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggle();
      }
    });
  });
}

/**
 * Live-filters the sidebar recipe list as the user types.
 * Matches against each item's data-title attribute (lowercased
 * server-side by Jinja2), so the comparison here stays simple.
 */
function initSearch() {
  const input = document.getElementById("recipe-search");
  const list = document.getElementById("recipe-list");
  if (!input || !list) return;

  const items = Array.from(list.querySelectorAll(".recipe-list__item"));

  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();

    items.forEach((item) => {
      const title = item.dataset.title || "";
      const matches = title.includes(query);
      item.classList.toggle("is-hidden", !matches);
    });
  });
}