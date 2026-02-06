let services = [];
let selected = new Set();

const elGrid = document.getElementById("services");
const elStack = document.getElementById("selected-stack");
const elOutput = document.getElementById("output");

fetch("/api/services")
  .then(r => r.json())
  .then(data => {
    services = data;
    renderServices(data);
  });

/* Service grid */
function renderServices(list) {
  elGrid.innerHTML = "";
  list.forEach(s => {
    const div = document.createElement("div");
    div.className = "service";
    const icon = s.icon ? `<img src="/static/icons/${s.icon}" alt="${s.name}">` : "";
    div.innerHTML = `${icon}<span>${s.name}</span>`;
    div.onclick = () => toggleService(s.name, div);
    elGrid.appendChild(div);
  });
}

function toggleService(name, el) {
  if (selected.has(name)) {
    selected.delete(name);
    el.classList.remove("selected");
  } else {
    selected.add(name);
    el.classList.add("selected");
  }
  renderStack();
}

/* Stack view */
function renderStack() {
  elStack.innerHTML = "";

  if (selected.size === 0) {
    elStack.textContent = "No services selected";
    elStack.classList.add("empty");
    return;
  }

  elStack.classList.remove("empty");

  selected.forEach(name => {
    const tag = document.createElement("span");
    tag.className = "stack-item";
    tag.textContent = name;
    elStack.appendChild(tag);
  });
}

/* Search */
document.getElementById("search").oninput = (e) => {
  const q = e.target.value.toLowerCase();
  renderServices(
    services.filter(s => s.name.toLowerCase().includes(q))
  );
};

/* Preview */
document.getElementById("preview").onclick = () => {
  if (selected.size === 0) return;

  fetch("/api/emulate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      services: [...selected],
      expand_implies: document.getElementById("expand-implies").checked,
      seed: document.getElementById("seed").value || null
    })
  })
  .then(r => r.json())
  .then(data => {
    elOutput.textContent = JSON.stringify(data, null, 2);
  });
};

/* Proxy launcher */
document.getElementById("launch").onclick = () => {
  if (selected.size === 0) return;

  const target = document.getElementById("target").value;
  if (!target) return;

  const params = new URLSearchParams({
    target: target,
    services: [...selected].join(","),
    expand_implies: document.getElementById("expand-implies").checked ? "1" : "0",
    seed: document.getElementById("seed").value || ""
  });

  window.open(`/proxy?${params.toString()}`, "_blank");
};

/* nginx / Caddy export */
function exportConfig(url) {
  if (selected.size === 0) return;

  fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      services: [...selected]
    })
  })
  .then(r => {
    if (!r.ok) throw new Error("Export failed");
    return r.json();
  })
  .then(data => {
    elOutput.textContent = Object.values(data)[0];
  });
}

document.getElementById("export-nginx").onclick = () => {
  exportConfig("/api/export/nginx");
};

document.getElementById("export-caddy").onclick = () => {
  exportConfig("/api/export/caddy");
};
