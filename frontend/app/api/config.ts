const base = import.meta.env.VITE_API_BASE;

if (!base) {
  throw new Error("VITE_API_BASE is not defined in .env");
}

export const SERVER_BASE = base;
export const API_BASE = `${base}/api/v1`;
export const PROXY_BASE = `${base}/proxy`;
export const STATIC_BASE = `${base}/static`;
