import { OpenAPI } from "./api-client";

// Configure base URL based on environment
if (typeof window === "undefined") {
  // Server-side (Server Components, Server Actions, NextAuth)
  // Docker internal network
  OpenAPI.BASE = "http://backend:8000";
} else {
  // Client-side (Browser)
  // Relative path, handled by Next.js rewrites/proxy
  OpenAPI.BASE = "";
}

export * from "./api-client";
