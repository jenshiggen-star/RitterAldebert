// Teilen-Leiste für Beiträge. Datenschutzfreundlich: lädt nichts von Dritten,
// Daten gehen erst beim Anklicken an den gewählten Dienst.
// Einbinden: <div class="share"></div> im Artikel + <script src="../assets/js/teilen.js"></script>
(function () {
  var boxes = document.querySelectorAll(".share");
  if (!boxes.length) return;

  var url = location.href.split("#")[0];
  var title = document.title.replace(/\s+–\s+RitterAldebert$/, "");
  var descEl = document.querySelector('meta[name="description"]');
  var text = title + (descEl ? " – " + descEl.content : "");
  var enc = encodeURIComponent;

  function el(tag, attrs, label) {
    var e = document.createElement(tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    e.textContent = label;
    return e;
  }

  function copy(btn) {
    var done = function () {
      var old = btn.textContent;
      btn.textContent = "Link kopiert ✓";
      setTimeout(function () { btn.textContent = old; }, 2000);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(done, function () { prompt("Link kopieren:", url); });
    } else {
      prompt("Link kopieren:", url);
    }
  }

  boxes.forEach(function (box) {
    box.setAttribute("role", "group");
    box.setAttribute("aria-label", "Beitrag teilen");
    box.appendChild(el("span", { "class": "share-label" }, "Teilen"));

    if (navigator.share) {
      var native = el("button", { type: "button", "class": "share-btn share-main" }, "Teilen …");
      native.addEventListener("click", function () {
        navigator.share({ title: title, text: text, url: url }).catch(function () {});
      });
      box.appendChild(native);
    }
    box.appendChild(el("a", { "class": "share-btn", href: "https://wa.me/?text=" + enc(title + " " + url), target: "_blank", rel: "noopener noreferrer" }, "WhatsApp"));
    box.appendChild(el("a", { "class": "share-btn", href: "mailto:?subject=" + enc(title) + "&body=" + enc(text + "\n\n" + url) }, "E-Mail"));
    var c = el("button", { type: "button", "class": "share-btn" }, "Link kopieren");
    c.addEventListener("click", function () { copy(c); });
    box.appendChild(c);
  });
})();
