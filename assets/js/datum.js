// Setzt das heutige Datum in die Kopfzeile (Fallback: statischer Text im HTML).
(function () {
  var el = document.getElementById("heute");
  if (!el) return;
  el.textContent = new Date().toLocaleDateString("de-DE", {
    weekday: "long", day: "numeric", month: "long", year: "numeric"
  });
})();
