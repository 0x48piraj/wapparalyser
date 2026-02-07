let services = [];
let selected = new Set();
let serviceMap = {};
let impliedMap = {};
let implied = new Set();

const PRESET_KEY = "wapparalyser.presets";

const elGrid = document.getElementById("services");
const elStack = document.getElementById("selected-stack");
const elOutput = document.getElementById("output");

refreshPresetList();

fetch("/api/services")
  .then(r => r.json())
  .then(data => {
    services = data;

    // build lookup tables
    data.forEach(s => {
      serviceMap[s.name] = s;
      impliedMap[s.name] = (s.implies || []).map(i => i.split(";")[0]);
    });

    renderServices(data);
  });

/* Service grid */
function renderServices(list) {
  elGrid.innerHTML = "";
  list.forEach(s => {
    const div = document.createElement("div");
    div.className = "service";
    if (selected.has(s.name)) div.classList.add("selected");
    if (implied.has(s.name)) div.classList.add("implied");
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
  renderServices(services);
}

function expandImpliedServices(baseServices) {
  const expanded = new Set(baseServices);
  const queue = [...baseServices];

  while (queue.length) {
    const name = queue.pop();
    const implies = impliedMap[name] || [];

    implies.forEach(dep => {
      if (!expanded.has(dep)) {
        expanded.add(dep);
        queue.push(dep);
      }
    });
  }

  return expanded;
}

/* Stack view */
function renderStack() {
  elStack.innerHTML = "";

  implied.clear();

  let displaySet = new Set(selected);

  if (document.getElementById("expand-implies").checked) {
    displaySet = expandImpliedServices(selected);
    displaySet.forEach(s => {
      if (!selected.has(s)) implied.add(s);
    });
  }

  if (displaySet.size === 0) {
    elStack.textContent = "No services selected";
    elStack.classList.add("empty");
    return;
  }

  elStack.classList.remove("empty");

  displaySet.forEach(name => {
    const tag = document.createElement("span");
    tag.className = "stack-item";

    if (implied.has(name)) {
      tag.classList.add("implied");
      tag.textContent = `${name} (implied)`;
    } else {
      tag.textContent = name;
    }

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

document.getElementById("expand-implies").onchange = () => {
  renderStack();
  renderServices(services);
};

function loadPresets() {
  return JSON.parse(localStorage.getItem(PRESET_KEY) || "{}");
}

function savePresets(presets) {
  localStorage.setItem(PRESET_KEY, JSON.stringify(presets));
}

function refreshPresetList() {
  const presets = loadPresets();
  const select = document.getElementById("preset-list");

  select.innerHTML = `<option value="">Load preset…</option>`;

  Object.keys(presets).forEach(name => {
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = name;
    select.appendChild(opt);
  });
}

document.getElementById("save-preset").onclick = () => {
  if (selected.size === 0) return;

  const name = document.getElementById("preset-name").value.trim();
  if (!name) return;

  const presets = loadPresets();

  if (presets[name] && !confirm(`Overwrite existing preset "${name}"?`)) {
    return;
  }

  presets[name] = {
    services: [...selected],
    expand: document.getElementById("expand-implies").checked,
    seed: document.getElementById("seed").value || ""
  };

  savePresets(presets);
  refreshPresetList();

  document.getElementById("preset-name").value = "";
};

document.getElementById("preset-list").onchange = (e) => {
  const name = e.target.value;
  if (!name) return;

  const presets = loadPresets();
  const preset = presets[name];
  if (!preset) return;

  selected.clear();
  preset.services.forEach(s => selected.add(s));

  document.getElementById("expand-implies").checked = preset.expand;
  document.getElementById("seed").value = preset.seed || "";

  renderStack();
  renderServices(services);
};

document.getElementById("delete-preset").onclick = () => {
  const select = document.getElementById("preset-list");
  const name = select.value;
  if (!name) return;

  const presets = loadPresets();
  delete presets[name];

  savePresets(presets);
  refreshPresetList();
};
