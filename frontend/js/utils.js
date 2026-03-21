// ============================================================
// AI-RecruitX — Utilities Layer (js/utils.js)
// Toast notifications, skeletons, animations, helpers
// ============================================================

// ======================== TOAST SYSTEM ========================

let toastContainer = null;

function ensureToastContainer() {
    if (toastContainer) return;
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.style.cssText = `
        position: fixed; top: 24px; right: 24px; z-index: 9999;
        display: flex; flex-direction: column; gap: 8px;
        pointer-events: none;
    `;
    document.body.appendChild(toastContainer);
}

const TOAST_ICONS = {
    success: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
    error: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    warning: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    info: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
};

const TOAST_COLORS = {
    success: { bg: 'rgba(16,185,129,0.12)', border: 'rgba(16,185,129,0.25)' },
    error: { bg: 'rgba(239,68,68,0.12)', border: 'rgba(239,68,68,0.25)' },
    warning: { bg: 'rgba(245,158,11,0.12)', border: 'rgba(245,158,11,0.25)' },
    info: { bg: 'rgba(99,102,241,0.12)', border: 'rgba(99,102,241,0.25)' }
};

/**
 * Show a toast notification.
 * @param {string} message
 * @param {'success'|'error'|'warning'|'info'} type
 * @param {number} duration — ms before auto-dismiss
 */
function showToast(message, type = 'info', duration = 3000) {
    ensureToastContainer();
    const colors = TOAST_COLORS[type] || TOAST_COLORS.info;
    const icon = TOAST_ICONS[type] || TOAST_ICONS.info;

    const toast = document.createElement('div');
    toast.style.cssText = `
        display: flex; align-items: center; gap: 10px;
        padding: 12px 18px; border-radius: 10px;
        background: ${colors.bg};
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        border: 1px solid ${colors.border};
        color: #f8fafc; font-size: 13px; font-family: 'Inter', sans-serif;
        pointer-events: auto; min-width: 280px; max-width: 420px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        transform: translateX(120%); transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
    `;
    toast.innerHTML = `
        <span style="flex-shrink:0">${icon}</span>
        <span style="flex:1">${message}</span>
        <button onclick="this.parentElement.remove()" style="
            background:none; border:none; color:#94a3b8; cursor:pointer;
            font-size:16px; padding:0 0 0 8px; line-height:1;
        ">×</button>
    `;

    toastContainer.appendChild(toast);
    requestAnimationFrame(() => {
        toast.style.transform = 'translateX(0)';
    });

    setTimeout(() => {
        toast.style.transform = 'translateX(120%)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 350);
    }, duration);
}


// ======================== SKELETON LOADING ========================

/**
 * Create skeleton loading HTML lines.
 * @param {number} lines
 * @returns {string} HTML string
 */
function createSkeleton(lines = 3) {
    let html = '';
    const widths = [100, 85, 70, 90, 60];
    for (let i = 0; i < lines; i++) {
        const w = widths[i % widths.length];
        html += `<div class="skeleton-line" style="width:${w}%; height:14px; border-radius:6px; margin-bottom:10px;"></div>`;
    }
    return html;
}

/**
 * Fill a table body with skeleton loading rows.
 */
function showTableSkeleton(tbody, rows = 5, cols = 4) {
    let html = '';
    for (let r = 0; r < rows; r++) {
        html += '<tr>';
        for (let c = 0; c < cols; c++) {
            html += `<td><div class="skeleton-line" style="width:${60 + Math.random() * 30}%; height:14px; border-radius:6px;"></div></td>`;
        }
        html += '</tr>';
    }
    tbody.innerHTML = html;
}

/**
 * Create skeleton cards for grid loading.
 */
function createCardSkeleton(count = 4) {
    let html = '';
    for (let i = 0; i < count; i++) {
        html += `
            <div class="card skeleton-card" style="padding:24px; min-height:180px;">
                <div class="skeleton-line" style="width:60%; height:18px; border-radius:6px; margin-bottom:16px;"></div>
                <div class="skeleton-line" style="width:90%; height:12px; border-radius:6px; margin-bottom:8px;"></div>
                <div class="skeleton-line" style="width:75%; height:12px; border-radius:6px; margin-bottom:20px;"></div>
                <div style="display:flex; gap:8px;">
                    <div class="skeleton-line" style="width:60px; height:24px; border-radius:12px;"></div>
                    <div class="skeleton-line" style="width:60px; height:24px; border-radius:12px;"></div>
                    <div class="skeleton-line" style="width:60px; height:24px; border-radius:12px;"></div>
                </div>
            </div>
        `;
    }
    return html;
}


// ======================== ANIMATIONS ========================

/**
 * Initialize scroll-triggered animations using Intersection Observer.
 * Any element with class .animate-on-scroll fades and slides in when visible.
 */
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const delay = el.dataset.delay || '0';
                el.style.transitionDelay = delay + 's';
                el.classList.add('scroll-visible');
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    elements.forEach((el, i) => {
        if (!el.dataset.delay) {
            el.dataset.delay = (i * 0.08).toFixed(2);
        }
        observer.observe(el);
    });
}

/**
 * Animate a counter from 0 to target value.
 * @param {HTMLElement} element
 * @param {number} target
 * @param {number} duration — ms
 */
function animateCounter(element, target, duration = 2000) {
    const start = performance.now();
    const isFloat = String(target).includes('.');

    function easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easeOutQuart(progress);
        const current = easedProgress * target;

        if (isFloat) {
            element.textContent = current.toFixed(1);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            if (isFloat) {
                element.textContent = target.toFixed(1);
            } else {
                element.textContent = target.toLocaleString();
            }
        }
    }

    requestAnimationFrame(update);
}

/**
 * Animate a progress bar's width.
 * @param {HTMLElement} bar
 * @param {number} targetWidth — percentage 0-100
 * @param {number} delay — ms
 */
function animateProgressBar(bar, targetWidth, delay = 0) {
    bar.style.width = '0%';
    setTimeout(() => {
        bar.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
        bar.style.width = targetWidth + '%';
    }, delay);
}

/**
 * Stagger children animation using Intersection Observer.
 */
function initStaggerChildren(containerSelector) {
    const containers = document.querySelectorAll(containerSelector);
    containers.forEach(container => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const children = container.children;
                    Array.from(children).forEach((child, i) => {
                        child.style.opacity = '0';
                        child.style.transform = 'translateY(20px)';
                        child.style.transition = `opacity 0.5s ease ${i * 0.08}s, transform 0.5s ease ${i * 0.08}s`;
                        requestAnimationFrame(() => {
                            child.style.opacity = '1';
                            child.style.transform = 'translateY(0)';
                        });
                    });
                    observer.unobserve(container);
                }
            });
        }, { threshold: 0.1 });
        observer.observe(container);
    });
}


// ======================== HELPERS ========================

/**
 * Format ISO date string to readable format.
 * "2026-01-15T..." → "Jan 15, 2026"
 */
function formatDate(dateString) {
    if (!dateString) return '—';
    const d = new Date(dateString);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/**
 * Format a 0–1 float score as a percentage string.
 * 0.924 → "92.4%"
 */
function formatScore(score) {
    return (score * 100).toFixed(1) + '%';
}

/**
 * Get color class name based on score.
 * ≥0.8 → 'success', ≥0.6 → 'warning', <0.6 → 'danger'
 */
function scoreColor(score) {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'danger';
}

/**
 * Truncate text to a max length.
 */
function truncate(text, length = 100) {
    if (!text) return '';
    if (text.length <= length) return text;
    return text.substring(0, length).trim() + '...';
}

/**
 * Export array of objects to CSV and trigger download.
 */
function exportToCSV(data, filename = 'export.csv') {
    if (!data || !data.length) return;
    const headers = Object.keys(data[0]);
    const csvRows = [headers.join(',')];

    for (const row of data) {
        const values = headers.map(h => {
            let val = row[h];
            if (Array.isArray(val)) val = val.join('; ');
            if (typeof val === 'string') val = '"' + val.replace(/"/g, '""') + '"';
            return val ?? '';
        });
        csvRows.push(values.join(','));
    }

    const csvString = csvRows.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}


// ======================== PAGE INIT ========================

/**
 * Standard page initialization:
 * - Fade-in body
 * - Init scroll animations
 * - Init Lucide icons
 */
function initPage() {
    // Fade in body
    document.body.style.opacity = '0';
    requestAnimationFrame(() => {
        document.body.style.transition = 'opacity 0.4s ease';
        document.body.style.opacity = '1';
    });

    // Init scroll animations
    initScrollAnimations();

    // Create Lucide icons if available
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Auto-init on DOMContentLoaded
document.addEventListener('DOMContentLoaded', initPage);


// ======================== SIDEBAR RENDERER ========================

/**
 * Render the shared sidebar into an element with id="sidebar".
 * @param {string} activePage — current page identifier, e.g. 'dashboard'
 */
function renderSidebar(activePage) {
    const user = getUser();
    const initials = getUserInitials();
    const userName = user?.name || 'User';
    const userEmail = user?.email || '';

    const navItems = [
        { id: 'dashboard', label: 'Dashboard', icon: 'layout-dashboard', href: 'dashboard.html' },
        { id: 'jobs', label: 'Jobs', icon: 'briefcase', href: 'jobs.html' },
        { id: 'upload', label: 'Upload Resumes', icon: 'upload', href: 'upload.html' },
        { id: 'results', label: 'Results', icon: 'bar-chart-3', href: 'results.html' },
        { id: 'assistant', label: 'AI Assistant', icon: 'message-circle', href: 'assistant.html' }
    ];

    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    sidebar.innerHTML = `
        <div class="sidebar-logo">
            <a href="index.html" class="logo-link">
                <span class="logo-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="6" fill="url(#lg)"/><defs><linearGradient id="lg" x1="0" y1="0" x2="24" y2="24"><stop stop-color="#6366f1"/><stop offset="0.5" stop-color="#8b5cf6"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs><path d="M7 8h10M7 12h7M7 16h10" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg></span>
                <span class="logo-text gradient-text-accent">AI-RecruitX</span>
            </a>
        </div>
        <nav class="sidebar-nav">
            ${navItems.map(item => `
                <a href="${item.href}" class="nav-item ${activePage === item.id ? 'active' : ''}" onclick="event.preventDefault(); navigate('${item.href}');">
                    <i data-lucide="${item.icon}"></i>
                    <span>${item.label}</span>
                </a>
            `).join('')}
        </nav>
        <div class="sidebar-footer">
            <div class="sidebar-user">
                <div class="user-avatar">${initials}</div>
                <div class="user-info">
                    <div class="user-name">${userName}</div>
                    <div class="user-email" title="${userEmail}">${userEmail}</div>
                </div>
            </div>
            <button class="logout-btn" onclick="logout()">
                <i data-lucide="log-out"></i>
                <span>Logout</span>
            </button>
        </div>
    `;

    // Re-init Lucide icons inside sidebar
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}
