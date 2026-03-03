// Load monitoring results and update dashboard
async function loadResults() {
  try {
    const response = await fetch("/results.json"); // Flask serves this file
    const data = await response.json();

    // --- Aggregate metrics (checks perspective) ---
    const totalChecks = data.length;
    const upChecks = data.filter(d => d.status === "UP").length;
    const avgUptime = ((upChecks / totalChecks) * 100).toFixed(1) + "%";
    const avgLatency = (data.reduce((sum, d) => sum + (d.latency_ms || 0), 0) / totalChecks).toFixed(0) + "ms";
    const incidents = data.filter(d => d.status === "DOWN").length;

    // --- Group by service ---
    const services = {};
    data.forEach(d => {
      if (!services[d.name]) services[d.name] = { checks: 0, up: 0, latency: 0, incidents: 0, timestamps: [] };
      services[d.name].checks++;
      if (d.status === "UP") services[d.name].up++;
      if (d.status === "DOWN") services[d.name].incidents++;
      services[d.name].latency += d.latency_ms || 0;
      services[d.name].timestamps.push({ t: d.timestamp, status: d.status, latency: d.latency_ms });
    });

    // --- Compute healthy services ---
    const totalServices = Object.keys(services).length;
    const healthyServices = Object.values(services).filter(s => s.up === s.checks).length;

    // --- Update KPI cards ---
    document.getElementById("kpi-cards").innerHTML = `
      <div class="card"><p class="kpi-label">Avg Uptime</p><p class="kpi-value">${avgUptime}</p></div>
      <div class="card"><p class="kpi-label">Avg Response</p><p class="kpi-value">${avgLatency}</p></div>
      <div class="card"><p class="kpi-label">Total Incidents</p><p class="kpi-value">${incidents}</p></div>
      <div class="card"><p class="kpi-label">Services Healthy</p><p class="kpi-value">${healthyServices} / ${totalServices}</p></div>
    `;

    // --- Populate service summary table ---
    const tbody = document.getElementById("service-summary");
    tbody.innerHTML = "";
    Object.keys(services).forEach(name => {
      const s = services[name];
      const uptime = ((s.up / s.checks) * 100).toFixed(1);
      const avgResp = (s.latency / s.checks).toFixed(0);
      const statusClass = uptime > 98 ? "healthy" : uptime > 95 ? "degraded" : "down";
      tbody.innerHTML += `
        <tr>
          <td>${name}</td>
          <td>${uptime}%</td>
          <td>${avgResp}ms</td>
          <td>${s.incidents}</td>
          <td><span class="status-badge ${statusClass}">${statusClass.charAt(0).toUpperCase() + statusClass.slice(1)}</span></td>
        </tr>
      `;
    });

    // --- Charts ---
    if (window.uptimeChart) window.uptimeChart.destroy();
    if (window.statusChart) window.statusChart.destroy();
    if (window.responseChart) window.responseChart.destroy();
    if (window.incidentChart) window.incidentChart.destroy();

    // Uptime trend (line chart)
    const uptimeCtx = document.getElementById("uptime-chart").getContext("2d");
    window.uptimeChart = new Chart(uptimeCtx, {
      type: 'line',
      data: {
        labels: data.map(d => d.timestamp),
        datasets: Object.keys(services).map(name => ({
          label: name,
          data: services[name].timestamps.map(t => t.status === "UP" ? 100 : 0),
          borderColor: getColor(name),
          fill: false
        }))
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });

    // Status distribution (pie chart)
    const statusCounts = {
      Healthy: data.filter(d => d.status === "UP").length,
      Down: data.filter(d => d.status === "DOWN").length,
      Degraded: data.filter(d => d.status === "DEGRADED").length
    };
    const statusCtx = document.getElementById("status-chart").getContext("2d");
    window.statusChart = new Chart(statusCtx, {
      type: 'pie',
      data: {
        labels: Object.keys(statusCounts),
        datasets: [{
          data: Object.values(statusCounts),
          backgroundColor: ["#10b981", "#ef4444", "#f59e0b"]
        }]
      }
    });

    // Response time (area chart with distinct colors)
    const responseCtx = document.getElementById("response-chart").getContext("2d");
    window.responseChart = new Chart(responseCtx, {
      type: 'line',
      data: {
        labels: data.map(d => d.timestamp),
        datasets: Object.keys(services).map(name => ({
          label: name,
          data: services[name].timestamps.map(t => t.latency),
          borderColor: getColor(name),                // distinct border color
          backgroundColor: getColor(name) + "33",     // semi-transparent fill
          fill: true,
          tension: 0.3                                // smooth curves
        }))
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } },
        scales: {
          y: { title: { display: true, text: "Latency (ms)" } },
          x: { title: { display: true, text: "Timestamp" } }
        }
      }
    });

    // Incident trend (bar chart)
    const incidentCtx = document.getElementById("incident-chart").getContext("2d");
    window.incidentChart = new Chart(incidentCtx, {
      type: 'bar',
      data: {
        labels: data.map(d => d.timestamp),
        datasets: [{
          label: "Incidents",
          data: data.map(d => d.status === "DOWN" ? 1 : 0),
          backgroundColor: "#ef4444"
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });

  } catch (err) {
    console.error("Error loading results.json:", err);
  }
}

// Helper: assign colors per service
function getColor(name) {
  const colors = {
    "Auth API": "#6366f1",          // Indigo
    "Payment Gateway": "#f59e0b",   // Amber
    "User Service": "#10b981",      // Emerald
    "Notification API": "#ef4444",  // Red
    "Storage Service": "#3b82f6"    // Blue
  };
  return colors[name] || "#6366f1"; // default Indigo
}

// Run on page load and refresh every 10s
loadResults();
setInterval(loadResults, 10000);
