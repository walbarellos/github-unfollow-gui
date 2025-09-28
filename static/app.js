let DATA = null;
let CURRENT_TAB = "following_only"; // default

async function loadData() {
  const elCount = document.getElementById("counts");
  const res = await fetch("/api/data");
  DATA = await res.json();

  elCount.innerHTML = `
    <span class="badge badge-soft me-2">Seguindo: ${DATA.counts.following}</span>
    <span class="badge badge-soft me-2">Seguidores: ${DATA.counts.followers}</span>
    <span class="badge badge-soft me-2">Não retribuem: ${DATA.counts.following_only}</span>
    <span class="badge badge-soft me-2">Mútuos: ${DATA.counts.mutuals}</span>
    <span class="badge badge-soft">Eles te seguem e você não: ${DATA.counts.not_followed_back_by_you}</span>
  `;
  document.getElementById("dryrun").textContent = DATA.dry_run ? "ON (seguro)" : "OFF";
  renderTable();
}

function getActiveList() {
  return (DATA && DATA[CURRENT_TAB]) ? [...DATA[CURRENT_TAB]] : [];
}

function applyFilters(list) {
  const q = document.getElementById("filterSearch").value.trim().toLowerCase();
  const minFollowers = parseInt(document.getElementById("filterMinFollowers").value || "0", 10);
  const type = document.getElementById("filterType").value;
  const location = document.getElementById("filterLocation").value.trim().toLowerCase();

  return list.filter(u => {
    const matchesQ = q === "" || (
      (u.login && u.login.toLowerCase().includes(q)) ||
      (u.name && u.name.toLowerCase().includes(q)) ||
      (u.bio && u.bio.toLowerCase().includes(q)) ||
      (u.company && u.company.toLowerCase().includes(q))
    );
    const matchesFollowers = (u.followers || 0) >= minFollowers;
    const matchesType = type === "ANY" || (u.type === type);
    const matchesLoc = location === "" || (u.location || "").toLowerCase().includes(location);
    return matchesQ && matchesFollowers && matchesType && matchesLoc;
  });
}

function sortList(list) {
  const sortBy = document.getElementById("sortBy").value;
  const dir = document.getElementById("sortDir").value;

  list.sort((a, b) => {
    const get = (u) => {
      if (sortBy === "followers") return u.followers || 0;
      if (sortBy === "following") return u.following || 0;
      if (sortBy === "repos") return u.public_repos || 0;
      if (sortBy === "name") return (u.name || u.login || "").toLowerCase();
      if (sortBy === "created") return (u.created_at || "");
      if (sortBy === "updated") return (u.updated_at || "");
      return (u.login || "").toLowerCase();
    };
    const va = get(a), vb = get(b);
    if (va < vb) return dir === "asc" ? -1 : 1;
    if (va > vb) return dir === "asc" ? 1 : -1;
    return 0;
  });
  return list;
}

function renderTable() {
  const tbody = document.getElementById("tbody");
  const list = sortList(applyFilters(getActiveList()));

  tbody.innerHTML = list.map(u => `
    <tr>
      <td><input class="form-check-input sel" type="checkbox" value="${u.login}"></td>
      <td>
        <img src="${u.avatar_url}" class="avatar me-2" alt="">
        <a href="${u.html_url}" target="_blank">${u.login}</a><br>
        <small class="text-secondary">${u.name || ""}</small>
      </td>
      <td>${u.bio ? `<small>${u.bio}</small>` : ""}</td>
      <td>
        <span class="badge badge-soft me-1">Followers: ${u.followers ?? 0}</span>
        <span class="badge badge-soft me-1">Following: ${u.following ?? 0}</span>
        <span class="badge badge-soft">Repos: ${u.public_repos ?? 0}</span>
      </td>
      <td>
        ${(u.location || "")}<br>
        ${u.company ? `<small>${u.company}</small>` : ""}
      </td>
      <td>
        <small>Type: ${u.type}</small><br>
        <small>Created: ${u.created_at?.slice(0,10) || ""}</small><br>
        <small>Updated: ${u.updated_at?.slice(0,10) || ""}</small>
      </td>
    </tr>
  `).join("");
}

function switchTab(tab) {
  CURRENT_TAB = tab;
  document.querySelectorAll(".tabbtn").forEach(b => b.classList.remove("active"));
  document.getElementById(`btn-${tab}`).classList.add("active");
  renderTable();
}

function selectAll(val) {
  document.querySelectorAll(".sel").forEach(cb => { cb.checked = val; });
}

async function doUnfollow() {
  const selected = [...document.querySelectorAll(".sel:checked")].map(cb => cb.value);
  if (selected.length === 0) {
    alert("Nenhum usuário selecionado.");
    return;
  }
  const res = await fetch("/api/unfollow", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ logins: selected })
  });
  const data = await res.json();
  const pre = document.getElementById("results");
  pre.textContent = JSON.stringify(data, null, 2);
  if (!data.dry_run) {
    // Após execução real, atualize dataset
    await loadData();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Filtros e eventos
  ["filterSearch","filterMinFollowers","filterType","filterLocation","sortBy","sortDir"]
    .forEach(id => document.getElementById(id).addEventListener("input", renderTable));
  document.getElementById("btn-select-all").onclick = () => selectAll(true);
  document.getElementById("btn-clear-all").onclick = () => selectAll(false);
  document.getElementById("btn-unfollow").onclick = doUnfollow;

  document.getElementById("btn-following_only").onclick = () => switchTab("following_only");
  document.getElementById("btn-mutuals").onclick = () => switchTab("mutuals");
  document.getElementById("btn-nfby").onclick = () => switchTab("not_followed_back_by_you");

  loadData();
});
