import { AuthRequest, AuthResponse, RegisterRequest, User } from '../types';

const API_BASE = (import.meta.env.VITE_API_URL ?? 'http://localhost:8000').replace(/\/+$/, '');
const API_PREFIX = `${API_BASE}/api/auth`;

export const authApi = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
      const response = await fetch(`${API_PREFIX}/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
      });
      if (!response.ok) {
          const error = await response.json().catch(() => ({}));
          throw { response: { data: { detail: error.detail || 'Login failed' } } };
      }
      return response.json();
  },

  register: async (email: string, password: string, security_key: string): Promise<User> => {
      const response = await fetch(`${API_PREFIX}/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, security_key }),
      });
      if (!response.ok) {
          const error = await response.json().catch(() => ({}));
          throw { response: { data: { detail: error.detail || 'Registration failed' } } };
      }
      const data = await response.json();
      // Auto login after register to get token since backend register returns just User usually,
      // but let's check backend return format
      return data;
  },

  fetchMe: async (token: string): Promise<User> => {
      const response = await fetch(`${API_PREFIX}/me`, {
          headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
          throw new Error('Failed to fetch user');
      }
      return response.json();
  },

  forgotPassword: async (email: string, security_key: string, new_password: string): Promise<any> => {
      const response = await fetch(`${API_PREFIX}/forgot-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, security_key, new_password }),
      });
      if (!response.ok) {
          const error = await response.json().catch(() => ({}));
          throw { response: { data: { detail: error.detail || 'Password reset failed' } } };
      }
      return response.json();
  }
};
