// No "server-only" import here: proxy.ts needs this too, and keeping this file
// dependency-free avoids pulling next/headers into the proxy bundle.
export const SESSION_COOKIE = "yanextfab_session";
