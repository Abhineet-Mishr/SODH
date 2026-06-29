export interface AuthRequest {
    email: string;
    password: string;
}

export interface RegisterRequest extends AuthRequest {
    security_key: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export interface User {
    id: number;
    email: string;
    credits: number;
}
