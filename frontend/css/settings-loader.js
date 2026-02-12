/**
 * Settings Loader — Reads saved settings from localStorage
 * and applies them (e.g., dark/light mode) on every page.
 * Include this script in all HTML pages.
 */
(function() {
  // Load settings
  const settings = JSON.parse(localStorage.getItem("settings") || "{}");

  // Dark mode: default is ON (dark). If user turned it OFF, apply light mode.
  if (settings.darkMode === false) {
    document.body.classList.add("light-mode");
  }
})();
