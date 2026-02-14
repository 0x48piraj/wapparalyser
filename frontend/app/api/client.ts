import { API_BASE } from "./config";

export type NginxExport = { nginx: string };
export type CaddyExport = { caddy: string };

export async function apiGet(path: string) {
  const res = await fetch(`${API_BASE}${path}`);

  if (!res.ok)
    throw new Error(await res.text());

  return res.json();
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok)
    throw new Error(await res.text());

  return res.json() as Promise<T>;
}
