// ============================================================
// AI-RecruitX — Auth Layer (js/auth.js)
// Token management, auth guards, navigation
// ============================================================

const TOKEN_KEY = 'ai_recruitx_token';
const USER_KEY = 'ai_recruitx_user';

/** Check if user is logged in */
function isLoggedIn() {
    return !!localStorage.getItem(TOKEN_KEY);
}

/** Get stored JWT token */
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

/** Get stored user object */
function getUser() {
    try {
        return JSON.parse(localStorage.getItem(USER_KEY) || 'null');
    } catch {
        return null;
    }
}

/** Save auth credentials after login/register */
function saveAuth(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

/** Clear auth and redirect to login */
function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    navigate('login.html');
}

/**
 * Auth guard — call at top of every protected page.
 * Redirects to login if not authenticated.
 * Returns the stored user object.
 */
function requireAuth() {
    if (!isLoggedIn()) {
        navigate('login.html');
        return null;
    }
    return getUser();
}

/**
 * Redirect guard — call at top of public auth pages.
 * If already logged in, send to dashboard.
 */
function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        navigate('dashboard.html');
    }
}

/**
 * Navigate to another page with a smooth fade-out transition.
 * @param {string} page — relative path like 'dashboard.html'
 */
function navigate(page) {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease';
    setTimeout(() => {
        window.location.href = page;
    }, 300);
}

/**
 * Get user initials from stored name.
 * "Manmath Patel" → "MP", "Anup" → "A"
 */
function getUserInitials() {
    const user = getUser();
    if (!user || !user.name) return '?';
    const parts = user.name.trim().split(/\s+/);
    if (parts.length >= 2) {
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return parts[0][0].toUpperCase();
}
