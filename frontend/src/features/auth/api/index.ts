import { AuthRequest, AuthResponse, RegisterRequest, User } from '../types';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
const API_PREFIX = `${API_BASE}/api/auth`;

export const login = async (request: AuthRequest): Promise<AuthResponse> => {
    const response = await fetch(`${API_PREFIX}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
    });
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Login failed');
    }
    return response.json();
};

export const register = async (request: RegisterRequest): Promise<User> => {
    const response = await fetch(`${API_PREFIX}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
    });
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Registration failed');
    }
    return response.json();
};

export const fetchMe = async (token: string): Promise<User> => {
    const response = await fetch(`${API_PREFIX}/me`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
        throw new Error('Failed to fetch user');
    }
    return response.json();
};
