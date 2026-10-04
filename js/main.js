(function () {
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (!toggle || !nav) return;

  function setOpen(open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }

  toggle.addEventListener("click", function () {
    setOpen(!nav.classList.contains("is-open"));
  });

  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      setOpen(false);
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });
})();

// Scoping-call form on the contact page. The form posts to big5.drelijah.org,
// which redirects back here with ?sent=1 or ?error=…
(function () {
  var form = document.querySelector("[data-enquiry-form]");
  if (!form) return;
  var params = new URLSearchParams(window.location.search);

  var need = params.get("need");
  if (need && form.need.querySelector('option[value="' + need + '"]')) {
    form.need.value = need;
  }
  var from = params.get("from");
  if (from && from.charAt(0) === "/") form.from.value = from.slice(0, 200);
  form.started.value = String(Date.now());

  var sent = document.querySelector("[data-enquiry-sent]");
  var error = document.querySelector("[data-enquiry-error]");
  if (params.get("sent") === "1") {
    sent.hidden = false;
    form.hidden = true;
  } else if (params.get("error")) {
    var messages = {
      invalid: "Please check your name, email and what you need, then try again.",
      verify: "The spam check did not complete. Please try again.",
      server: "Something went wrong on our side. Please try again in a moment."
    };
    error.querySelector("[data-enquiry-error-text]").textContent =
      messages[params.get("error")] || messages.invalid;
    error.hidden = false;
  }

  var sitekey = form.getAttribute("data-turnstile-sitekey");
  if (sitekey) {
    var widget = document.createElement("div");
    widget.className = "cf-turnstile";
    widget.setAttribute("data-sitekey", sitekey);
    form.querySelector("[data-turnstile-slot]").appendChild(widget);
    var script = document.createElement("script");
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }

  // Re-enable the button if the visitor comes back via the Back button.
  window.addEventListener("pageshow", function () {
    var button = form.querySelector('button[type="submit"]');
    button.disabled = false;
    button.textContent = "Request the scoping call";
  });

  form.addEventListener("submit", function () {
    var button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    button.textContent = "Sending…";
  });
})();
