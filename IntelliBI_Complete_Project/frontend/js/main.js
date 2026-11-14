const API_BASE = "http://127.0.0.1:8000";
const byId = (id) => document.getElementById(id);

async function checkBackend() {
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    if (!response.ok) throw new Error("Backend unavailable");
    byId("backendStatus").textContent = "Backend connected";
    document.querySelector(".status-dot").style.background = "#279b72";
  } catch {
    byId("backendStatus").textContent = "Backend not connected — start FastAPI on port 8000";
    document.querySelector(".status-dot").style.background = "#d49a32";
  }
}

function renderTable(records) {
  const table = byId("previewTable");
  table.replaceChildren();
  if (!records || records.length === 0) {
    table.innerHTML = "<tbody><tr><td>No preview rows available.</td></tr></tbody>";
    return;
  }
  const columns = Object.keys(records[0]);
  const thead = document.createElement("thead");
  const headRow = document.createElement("tr");
  columns.forEach((name) => {
    const th = document.createElement("th"); th.textContent = name; headRow.appendChild(th);
  });
  thead.appendChild(headRow);
  const tbody = document.createElement("tbody");
  records.forEach((record) => {
    const tr = document.createElement("tr");
    columns.forEach((name) => {
      const td = document.createElement("td");
      td.textContent = record[name] == null ? "" : String(record[name]);
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.append(thead, tbody);
}

function showResults(data) {
  const summary = data.summary;
  byId("results").classList.remove("hidden");
  byId("resultTitle").textContent = `Dataset overview: ${data.filename}`;
  byId("rowsStat").textContent = summary.rows;
  byId("columnsStat").textContent = summary.columns;
  byId("missingStat").textContent = summary.missing_values;
  byId("duplicatesStat").textContent = summary.duplicate_rows;
  const chips = byId("columnNames"); chips.replaceChildren();
  summary.column_names.forEach((name) => {
    const span = document.createElement("span"); span.className = "chip"; span.textContent = name; chips.appendChild(span);
  });
  renderTable(summary.preview);

  const agentContainer = byId("agentResults"); agentContainer.replaceChildren();
  (data.analysis?.agents || []).forEach((agent) => {
    const card = document.createElement("div"); card.className = "agent-card";
    const heading = document.createElement("strong"); heading.textContent = agent.agent;
    const paragraph = document.createElement("p");
    paragraph.textContent = agent.finding || JSON.stringify(agent.details || {});
    card.append(heading, paragraph); agentContainer.appendChild(card);
  });
  const list = byId("recommendations"); list.replaceChildren();
  const decision = (data.analysis?.agents || []).find((a) => a.agent === "Decision Agent");
  (decision?.recommendations || []).forEach((recommendation) => {
    const li = document.createElement("li"); li.textContent = recommendation; list.appendChild(li);
  });
}

async function uploadDataset() {
  const file = byId("datasetFile").files[0];
  const status = byId("uploadStatus");
  if (!file) { status.textContent = "Please choose a CSV or Excel file first."; return; }
  if (file.size > 10 * 1024 * 1024) { status.textContent = "File exceeds the 10 MB limit."; return; }
  const formData = new FormData();
  formData.append("file", file);
  byId("uploadBtn").disabled = true;
  status.textContent = "Uploading and analyzing dataset…";
  try {
    const response = await fetch(`${API_BASE}/api/datasets/upload`, { method: "POST", body: formData });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Upload failed.");
    showResults(result);
    status.textContent = result.message;
    await loadDatasets();
  } catch (error) {
    status.textContent = `Error: ${error.message}. Check that the backend is running.`;
  } finally {
    byId("uploadBtn").disabled = false;
  }
}

async function loadDatasets() {
  const list = byId("datasetList");
  try {
    const response = await fetch(`${API_BASE}/api/datasets`);
    const result = await response.json();
    list.replaceChildren();
    if (!result.datasets.length) {
      const li = document.createElement("li"); li.textContent = "No datasets uploaded yet."; list.appendChild(li); return;
    }
    result.datasets.forEach((dataset) => {
      const li = document.createElement("li");
      li.textContent = `#${dataset.id} — ${dataset.filename} (uploaded ${dataset.uploaded_at})`;
      list.appendChild(li);
    });
  } catch {
    list.innerHTML = "<li>Unable to load datasets. Is the backend running?</li>";
  }
}

byId("uploadBtn").addEventListener("click", uploadDataset);
byId("refreshDatasets").addEventListener("click", loadDatasets);
checkBackend();
loadDatasets();
