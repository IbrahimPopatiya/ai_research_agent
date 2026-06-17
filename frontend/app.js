const API = '/api';

async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

// Stats
async function loadStats() {
    try {
        const stats = await fetchJSON(`${API}/stats`);
        document.getElementById('stat-tools').textContent = stats.tools;
        document.getElementById('stat-posts').textContent = stats.posts;
        document.getElementById('stat-news').textContent = stats.news;
        document.getElementById('stat-total').textContent = stats.total;
    } catch {
        // silently fail on stats
    }
}

// Tools
async function loadTools() {
    try {
        const tools = await fetchJSON(`${API}/tools`);
        const tbody = document.querySelector('#tools-table tbody');
        const empty = document.getElementById('tools-empty');

        if (tools.length === 0) {
            tbody.innerHTML = '';
            empty.style.display = 'block';
            return;
        }

        empty.style.display = 'none';
        tbody.innerHTML = tools.map(t => `
            <tr>
                <td><strong>${esc(t.name)}</strong></td>
                <td class="description" title="${esc(t.description || '')}">${esc(t.description || '-')}</td>
                <td class="stars">${t.stars.toLocaleString()}</td>
                <td>${esc(t.language || '-')}</td>
                <td><a href="${esc(t.url)}" target="_blank" rel="noopener">View</a></td>
            </tr>
        `).join('');
    } catch {
        // fail silently
    }
}

// Posts
async function loadPosts() {
    try {
        const posts = await fetchJSON(`${API}/posts`);
        const tbody = document.querySelector('#posts-table tbody');
        const empty = document.getElementById('posts-empty');

        if (posts.length === 0) {
            tbody.innerHTML = '';
            empty.style.display = 'block';
            return;
        }

        empty.style.display = 'none';
        tbody.innerHTML = posts.map(p => `
            <tr>
                <td>${esc(p.title)}</td>
                <td><span class="source-badge ${p.source.toLowerCase()}">${esc(p.source)}</span></td>
                <td class="stars">${p.score ?? '-'}</td>
                <td><a href="${esc(p.url)}" target="_blank" rel="noopener">View</a></td>
            </tr>
        `).join('');
    } catch {
        // fail silently
    }
}

// Collect
async function collect(source) {
    const btn = document.getElementById(`btn-${source}`);
    const status = document.getElementById('collect-status');

    btn.disabled = true;
    btn.classList.add('loading');
    status.textContent = `Collecting from ${source}...`;
    status.className = 'status-message';

    try {
        const data = await fetchJSON(`${API}/collect/${source}`, { method: 'POST' });
        status.textContent = data.message;
        loadStats();
        loadTools();
        loadPosts();
    } catch (e) {
        status.textContent = `Error: ${e.message}`;
        status.className = 'status-message error';
    } finally {
        btn.disabled = false;
        btn.classList.remove('loading');
    }
}

// Report
async function generateReport() {
    const btn = document.getElementById('btn-report');
    const content = document.getElementById('report-content');

    btn.disabled = true;
    btn.classList.add('loading');
    content.textContent = 'Generating report...';

    try {
        const data = await fetchJSON(`${API}/report`);
        content.textContent = data.report;
    } catch (e) {
        content.textContent = `Error generating report: ${e.message}`;
    } finally {
        btn.disabled = false;
        btn.classList.remove('loading');
    }
}

// Tabs
function switchTab(name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

    document.querySelector(`.tab[onclick="switchTab('${name}')"]`).classList.add('active');
    document.getElementById(`tab-${name}`).classList.add('active');
}

// Escape HTML
function esc(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadTools();
    loadPosts();
});
