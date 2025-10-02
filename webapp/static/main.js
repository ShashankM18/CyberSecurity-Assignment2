async function fetchJSON(url, opts={}) {
  const res = await fetch(url, Object.assign({ headers: { 'Content-Type': 'application/json' } }, opts));
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function fmtTime(ts) {
  const d = new Date(ts * 1000);
  return d.toLocaleString();
}

async function loadAgents() {
  try {
    const data = await fetchJSON('/api/agents');
    const tbody = document.querySelector('#agentsTable tbody');
    tbody.innerHTML = '';
    data.agents.forEach(a => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${a.agent_id}</td>
        <td>${a.trust.toFixed(3)}</td>
        <td>${a.isolated ? 'Yes' : 'No'}</td>
        <td class="row-actions">
          <button onclick="isolateAgent('${a.agent_id}')">Isolate</button>
          <button onclick="releaseAgent('${a.agent_id}')">Release</button>
        </td>`;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error('loadAgents failed', e);
  }
}

async function loadLedger() {
  try {
    const data = await fetchJSON('/api/ledger');
    document.querySelector('#ledgerInfo').textContent = `len=${data.length} valid=${data.valid}`;
    const tbody = document.querySelector('#ledgerTable tbody');
    tbody.innerHTML = '';
    data.chain.slice().reverse().forEach(b => {
      const tr = document.createElement('tr');
      let action = ''; let agent = ''; let reason = '';
      if (b.data) {
        action = b.data.action || '';
        agent = b.data.agent || '';
        reason = b.data.reason || '';
      }
      tr.innerHTML = `
        <td>${b.index}</td>
        <td>${fmtTime(b.timestamp)}</td>
        <td>${action}</td>
        <td>${agent}</td>
        <td>${reason}</td>
        <td><code>${(b.hash||'').slice(0, 12)}...</code></td>`;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error('loadLedger failed', e);
  }
}

async function observeAction() {
  const agentId = document.querySelector('#agentId').value.trim();
  const action = document.querySelector('#action').value;
  const status = document.querySelector('#observeStatus');
  if (!agentId) {
    status.textContent = 'Enter agent id';
    return;
  }
  try {
    const res = await fetchJSON('/api/observe', {
      method: 'POST', body: JSON.stringify({ agent_id: agentId, action })
    });
    status.textContent = `Trust=${res.trust.toFixed(3)} (malicious=${res.malicious})`;
    await Promise.all([loadAgents(), loadLedger()]);
  } catch (e) {
    status.textContent = e.message;
  }
}

async function isolateAgent(agentId) {
  try {
    await fetchJSON('/api/isolate', { method: 'POST', body: JSON.stringify({ agent_id: agentId, reason: 'manual' }) });
    await Promise.all([loadAgents(), loadLedger()]);
  } catch (e) { console.error(e); }
}

async function releaseAgent(agentId) {
  try {
    await fetchJSON('/api/release', { method: 'POST', body: JSON.stringify({ agent_id: agentId, reason: 'manual' }) });
    await Promise.all([loadAgents(), loadLedger()]);
  } catch (e) { console.error(e); }
}

async function runBenchmarks() {
  const trustOps = parseInt(document.querySelector('#bmTrust').value, 10) || 500;
  const blocks = parseInt(document.querySelector('#bmBlocks').value, 10) || 50;
  const difficulty = parseInt(document.querySelector('#bmDiff').value, 10) || 2;
  const isoOps = parseInt(document.querySelector('#bmIso').value, 10) || 100;
  const out = document.querySelector('#bmOut');
  out.textContent = 'Running...';
  try {
    const res = await fetchJSON('/api/benchmark', { method: 'POST', body: JSON.stringify({ trust_ops: trustOps, blocks, difficulty, iso_ops: isoOps }) });
    out.textContent = JSON.stringify(res, null, 2);
  } catch (e) {
    out.textContent = e.message;
  }
}

async function tick() {
  await Promise.all([loadAgents(), loadLedger()]);
}

setInterval(tick, 3000);
window.addEventListener('load', tick);
