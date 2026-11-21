// POST /subscribe  { email, source, lanes? }
// Stores the subscriber in the TF_SUBSCRIBERS KV namespace (Tierra Firme's own list,
// separate from any member's list). Sends a welcome email only when RESEND_API_KEY,
// UNSUB_SECRET and NEWSLETTER_FROM are set. Capture works without them.

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// Lane choices from the signup form. Records created before lanes existed have no
// `lanes` field; treat that as "all lanes" when reading.
const LANES = ['cre', 'capital', 'research'];
const cleanLanes = (v) => Array.isArray(v) ? [...new Set(v.map(String).filter(x => LANES.includes(x)))] : [];

export async function hmac(secret, value) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(value));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}

export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); } catch { return json({ ok: false, error: 'Send a valid email address.' }, 400); }
  const email = String(data.email || '').trim().toLowerCase();
  if (!EMAIL_RE.test(email) || email.length > 254) return json({ ok: false, error: 'Enter a valid email address.' }, 400);
  if (!env.TF_SUBSCRIBERS) return json({ ok: false, error: 'The list is not connected yet. Try again soon.' }, 503);

  const key = 'sub:' + email;
  const existing = await env.TF_SUBSCRIBERS.get(key, 'json');
  const lanes = cleanLanes(data.lanes);
  const now = new Date().toISOString();

  if (existing && existing.status === 'active') {
    // Already subscribed: merge any new lane choices, keep everything else.
    const merged = [...new Set([...(existing.lanes || []), ...lanes])];
    if (merged.length !== (existing.lanes || []).length) {
      await env.TF_SUBSCRIBERS.put(key, JSON.stringify({ ...existing, lanes: merged, updated: now }));
    }
    return json({ ok: true, already: true });
  }

  await env.TF_SUBSCRIBERS.put(key, JSON.stringify({
    email, status: 'active', source: String(data.source || '').slice(0, 80),
    lanes: [...new Set([...(existing?.lanes || []), ...lanes])],
    created: existing?.created || now, updated: now,
  }));

  if (env.RESEND_API_KEY && env.UNSUB_SECRET && env.NEWSLETTER_FROM) {
    try {
      const origin = new URL(request.url).origin;
      const token = await hmac(env.UNSUB_SECRET, email);
      const unsub = `${origin}/unsubscribe?e=${encodeURIComponent(email)}&t=${token}`;
      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: env.NEWSLETTER_FROM,
          to: email,
          subject: "Welcome to the Tierra Firme Newsletter",
          headers: { 'List-Unsubscribe': `<${unsub}>`, 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click' },
          html: `<div style="font-family:Georgia,serif;max-width:560px;color:#13212f">
            <h2 style="font-weight:600">Welcome to the Tierra Firme Newsletter.</h2>
            <p>You will receive short, sourced briefings on Colombia and Latin America, and every Investor Lab 2027 update before anyone else. It is free.</p>
            <p>Tierra Firme is educational content. Nothing we send is investment, tax or legal advice.</p>
            <p style="font-size:13px;color:#56616e">Don't want these? <a href="${unsub}">Unsubscribe in one click</a>.<br>${env.MAILING_ADDRESS || ''}</p>
          </div>`,
        }),
      });
    } catch (_) { /* subscriber is stored; email is best effort */ }
  }
  return json({ ok: true });
}

export const onRequestGet = () => json({ ok: false, error: 'Use POST.' }, 405);
