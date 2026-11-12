const API_URL = "http://localhost:3000/api/tickets";
const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

let tickets = [];
let selectedId = null;

const statusClass = s => "status-" + s.toLowerCase().replaceAll(" ", "-");
const badge = s => `<span class="status-pill ${statusClass(s)}">${s}</span>`;
const priorityBadge = p => `<span class="priority-pill priority-${p.toLowerCase().replace("í", "i")}">${p}</span>`;

// Cargar tickets desde MySQL
async function loadTicketsFromDB() {
  try {
    const res = await fetch(API_URL);
    const json = await res.json();
    if (json.success) {
      tickets = json.data;
      renderDashboard();
      renderTickets();
    }
  } catch (err) {
    console.error("Error cargando tickets de MySQL:", err);
  }
}

function navigate(page) {
  $$(".page").forEach(p => p.classList.toggle("active", p.id === "page-" + page));
  $$(".nav-link").forEach(b => b.classList.toggle("active", b.dataset.page === page));
  const names = { dashboard: "Dashboard", "new-ticket": "Asignación de soportes", assigned: "Soportes asignados" };
  $("#crumb").textContent = names[page];
  $("#sidebar").classList.remove("open");
  if (page === "dashboard") renderDashboard();
  if (page === "assigned") renderTickets();
}

$$("[data-page]").forEach(b => b.addEventListener("click", () => navigate(b.dataset.page)));
$$("[data-go]").forEach(b => b.addEventListener("click", () => navigate(b.dataset.go)));
$("#mobileMenu").addEventListener("click", () => $("#sidebar").classList.toggle("open"));
$("#today").textContent = new Intl.DateTimeFormat("es-CO", { day: "2-digit", month: "short", year: "numeric" }).format(new Date());

function renderDashboard() {
  const total = tickets.length, count = s => tickets.filter(t => t.status === s).length;
  $("#totalStat").textContent = total;
  $("#newStat").textContent = count("Nuevo");
  $("#pendingStat").textContent = count("Pendiente");
  $("#doneStat").textContent = count("Finalizado");
  $("#assignedCount").textContent = tickets.filter(t => t.status !== "Finalizado").length;

  $("#recentRows").innerHTML = tickets.slice(0, 5).map(t => `
    <tr>
      <td class="ticket-id">${t.id}</td>
      <td><span class="person-cell">${t.requester}</span><span class="sub-cell">${t.date}</span></td>
      <td>${t.category}</td>
      <td>${badge(t.status)}</td>
    </tr>`).join("");

  const n = count("Nuevo"), p = count("Pendiente"), e = count("En proceso"), f = count("Finalizado");
  const colors = ["#5796dc", "#e9a33d", "#9a7ad7", "#2eaa68"], vals = [n, p, e, f];
  let start = 0;
  const stops = vals.map((v, i) => {
    let end = start + (total ? v / total * 360 : 0);
    let seg = `${colors[i]} ${start}deg ${end}deg`;
    start = end;
    return seg;
  });

  $("#statusSummary").innerHTML = `<div class="donut" style="background:conic-gradient(${total ? stops.join(", ") : "#e9eef0 0deg 360deg"})"><div class="donut-inner"><strong>${total}</strong><small>Solicitudes</small></div></div>`;
}

function renderTickets() {
  const q = $("#searchInput").value.toLowerCase(), s = $("#statusFilter").value, p = $("#priorityFilter").value;
  const filtered = tickets.filter(t => (!s || t.status === s) && (!p || t.priority === p) && [t.id, t.requester, t.category, t.location, t.technician].join(" ").toLowerCase().includes(q));
  
  $("#ticketRows").innerHTML = filtered.length ? filtered.map(t => `
    <tr>
      <td class="ticket-id">${t.id}<span class="sub-cell">${t.date}</span></td>
      <td><span class="person-cell">${t.requester}</span><span class="sub-cell">${t.userType}</span></td>
      <td>${t.category}<span class="sub-cell">${t.location}</span></td>
      <td>${priorityBadge(t.priority)}</td>
      <td>${t.technician || "Por asignar"}</td>
      <td>${badge(t.status)}</td>
      <td><button class="action-button" data-detail="${t.id}">Ver detalle</button></td>
    </tr>`).join("") : `<tr><td colspan="7" class="empty-row">No se encontraron solicitudes con esos filtros.</td></tr>`;
  
  $("#resultCount").textContent = `${filtered.length} solicitud(es)`;
  $$("[data-detail]").forEach(b => b.addEventListener("click", () => openDetail(b.dataset.detail)));
}

["searchInput", "statusFilter", "priorityFilter"].forEach(id => $("#" + id).addEventListener(id === "searchInput" ? "input" : "change", renderTickets));

// Guardar nuevo ticket en MySQL
$("#ticketForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const d = Object.fromEntries(new FormData(e.target).entries());
  const id = "ST-2026-" + String(tickets.length + 1).padStart(3, "0");
  const newTicket = {
    ...d,
    id,
    date: new Intl.DateTimeFormat("es-CO", { day: "2-digit", month: "short", year: "numeric" }).format(new Date()),
    status: "Nuevo",
    technician: d.technician || "Por asignar"
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTicket)
    });
    const json = await res.json();

    if (json.success) {
      e.target.reset();
      await loadTicketsFromDB(); // Recarga los datos reales desde MySQL
      if (typeof showToast === "function") showToast(`Solicitud ${id} registrada correctamente`);
      navigate("assigned");
    } else {
      alert("Error al guardar: " + json.error);
    }
  } catch (err) {
    console.error("Error enviando ticket:", err);
  }
});

function openDetail(id) {
  selectedId = id;
  const t = tickets.find(x => x.id === id);
  if (!t) return;
  $("#modalTitle").textContent = t.id;
  $("#modalBody").innerHTML = `<div class="detail-grid">
    <div class="detail-item"><small>Solicitante</small><strong>${t.requester}</strong></div><div class="detail-item"><small>Correo</small><strong>${t.email}</strong></div>
    <div class="detail-item"><small>Tipo de usuario / Área</small><strong>${t.userType} · ${t.area || "No especificada"}</strong></div><div class="detail-item"><small>Fecha de reporte</small><strong>${t.date}</strong></div>
    <div class="detail-item"><small>Tipo de novedad</small><strong>${t.category}</strong></div><div class="detail-item"><small>Ubicación</small><strong>${t.location}</strong></div>
    <div class="detail-item"><small>Equipo</small><strong>${t.equipment || "No especificado"}</strong></div><div class="detail-item"><small>Prioridad</small><strong>${priorityBadge(t.priority)}</strong></div>
    <div class="detail-item detail-description"><small>Descripción del problema</small><p>${t.description}</p></div></div>
    <div class="modal-edit"><label>Estado de la solicitud<select id="editStatus">${["Nuevo", "Pendiente", "En proceso", "Finalizado"].map(x => `<option ${t.status === x ? "selected" : ""}>${x}</option>`).join("")}</select></label>
    <label>Técnico responsable<select id="editTech">${["Por asignar", "Andrés Martínez", "Laura Gómez", "Carlos Rodríguez"].map(x => `<option ${t.technician === x ? "selected" : ""}>${x}</option>`).join("")}</select></label></div>`;
  $("#detailModal").classList.add("show");
}

function closeModal() { $("#detailModal").classList.remove("show"); }
$("#closeModal").addEventListener("click", closeModal);
$("#closeModal2").addEventListener("click", closeModal);
$("#detailModal").addEventListener("click", e => { if (e.target.id === "detailModal") closeModal(); });

// Actualizar estado y técnico en MySQL
$("#saveStatus").addEventListener("click", async () => {
  const status = $("#editStatus").value;
  const technician = $("#editTech").value;

  try {
    const res = await fetch(`${API_URL}/${selectedId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, technician })
    });
    const json = await res.json();

    if (json.success) {
      closeModal();
      await loadTicketsFromDB(); // Refresca dashboard y tabla
      if (typeof showToast === "function") showToast("Los cambios de la solicitud fueron guardados.");
    }
  } catch (err) {
    console.error("Error actualizando ticket:", err);
  }
});

// ⚠️ PEGA AQUÍ DEBAJO TU FUNCIÓN showToast() ORIGINAL QUE SE CORTÓ AL FINAL

// Iniciar cargando los datos desde MySQL
document.addEventListener("DOMContentLoaded", loadTicketsFromDB);
