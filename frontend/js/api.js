// ============================================================
// AI-RecruitX — API Layer (js/api.js)
// All backend communication goes through this module
// ============================================================

const BASE_URL = 'http://localhost:8000';

/**
 * Build auth headers. Omit Content-Type for FormData requests.
 */
function getHeaders(isFormData = false) {
    const headers = {
        'Authorization': 'Bearer ' + getToken()
    };
    if (!isFormData) {
        headers['Content-Type'] = 'application/json';
    }
    return headers;
}

/**
 * Central fetch wrapper with error handling.
 * Handles 401 (auto-logout), 429 (rate limit), network errors.
 */
async function apiFetch(endpoint, options = {}) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);

        if (response.status === 401) {
            logout();
            throw new Error('Session expired. Please log in again.');
        }

        if (response.status === 429) {
            throw new Error('Too many attempts, please wait a moment.');
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error (${response.status}). Please try again.`);
        }

        return await response.json();
    } catch (error) {
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            throw new Error('Connection failed. Is the server running?');
        }
        throw error;
    }
}

// ======================== AUTH ========================

/**
 * Register a new user.
 * POST /auth/register  → { id, email, name }
 */
async function apiRegister(name, email, password) {
    return apiFetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
    });
}

/**
 * Login user.
 * POST /auth/login  → { access_token, token_type }
 */
async function apiLogin(email, password) {
    return apiFetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
}

// ======================== JOBS ========================

/**
 * List jobs (paginated).
 * GET /jobs/?page=N&page_size=N  → { items, page, page_size, total }
 */
async function getJobs(page = 1, pageSize = 20) {
    return apiFetch(`/jobs/?page=${page}&page_size=${pageSize}`, {
        headers: getHeaders()
    });
}

/**
 * Create a new job posting.
 * POST /jobs/create  → JobResponse
 */
async function createJob(title, description, requiredSkills) {
    return apiFetch('/jobs/create', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ title, description, required_skills: requiredSkills })
    });
}

// ======================== CANDIDATES ========================

/**
 * List candidates (paginated).
 * GET /candidates/?page=N&page_size=N  → { items, page, page_size, total }
 */
async function getCandidates(page = 1, pageSize = 20) {
    return apiFetch(`/candidates/?page=${page}&page_size=${pageSize}`, {
        headers: getHeaders()
    });
}

/**
 * Get a single candidate by ID.
 * GET /candidates/{id}  → CandidateResponse
 */
async function getCandidate(id) {
    return apiFetch(`/candidates/${id}`, {
        headers: getHeaders()
    });
}

// ======================== RESUME ========================

/**
 * Upload a single resume PDF.
 * POST /resume/upload  → CandidateResponse
 */
async function uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);
    return apiFetch('/resume/upload', {
        method: 'POST',
        headers: getHeaders(true),
        body: formData
    });
}

/**
 * Upload multiple resume PDFs in batch.
 * POST /resume/upload-batch  → CandidateResponse[]
 */
async function uploadBatch(files) {
    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }
    return apiFetch('/resume/upload-batch', {
        method: 'POST',
        headers: getHeaders(true),
        body: formData
    });
}

// ======================== SCREENING ========================

/**
 * Run AI screening for a job.
 * POST /screening/run  → CandidateRankingResponse[]
 */
async function runScreening(jobId) {
    return apiFetch('/screening/run', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ job_id: jobId })
    });
}

// ======================== ASSISTANT ========================

/**
 * Query the AI assistant. Optionally with job context.
 * POST /assistant/query  → { response: string }
 */
async function queryAssistant(query, jobId = null) {
    const body = { query };
    if (jobId) body.job_id = jobId;
    return apiFetch('/assistant/query', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(body)
    });
}

// ======================== HEALTH ========================

/**
 * Health check.
 * GET /health  → { status, database }
 */
async function checkHealth() {
    return apiFetch('/health');
}
