// GET /unsubscribe?e=&t=  (link in emails)   POST /unsubscribe  (one-click List-Unsubscribe)
import { hmac } from './subscribe.js';

const page = (title, msg, status = 200) => new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${title} | Tierra Firme</title>
<style>body{margin:0;background:#061327;color:#fff;font-family:Georgia,serif;display:flex;min-height:100vh;align-items:center;justify-content:center;padding:24px}
main{max-width:520px}h1{font-weight:600;color:#fff}p{color:rgba(255,255,255,.78);font-family:Inter,Arial,sans-serif;line-height:1.6}a{color:#e9a825}</style></head>
<body><main><h1>${title}</h1><p>${msg}</p><p><a href="/">Back to Tierra Firme</a></p></main></body></html>`,
  { status, headers: { 'Content-Type': 'text/html; charset=utf-8' } });

async function remove(url, env) {
  const email = String(url.searchParams.get('e') || '').trim().toLowerCase();
  const token = String(url.searchParams.get('t') || '');
  if (!email || !token || !env.UNSUB_SECRET || !env.TF_SUBSCRIBERS) return false;
  if (token !== await hmac(env.UNSUB_SECRET, email)) return false;
  const key = 'sub:' + email;
  const rec = (await env.TF_SUBSCRIBERS.get(key, 'json')) || { email };
  await env.TF_SUBSCRIBERS.put(key, JSON.stringify({ ...rec, status: 'unsubscribed', updated: new Date().toISOString() }));
  return true;
}

export async function onRequestGet({ request, env }) {
  return (await remove(new URL(request.url), env))
    ? page("You're unsubscribed", 'You will not get more email from Tierra Firme. You can rejoin anytime from the site.')
    : page('Link not valid', 'This unsubscribe link is not valid or has expired. Reply to any email from us and we will remove you.', 400);
}

export async function onRequestPost({ request, env }) {
  const ok = await remove(new URL(request.url), env);
  return new Response(ok ? 'ok' : 'invalid', { status: ok ? 200 : 400 });
}
