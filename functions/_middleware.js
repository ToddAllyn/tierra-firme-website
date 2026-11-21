// Sends visitors on the old pages.dev address and on the bare domain to the main address,
// www.tierrafirme.lat, keeping the path. Branch previews (<branch>.tierra-firme.pages.dev)
// are left alone so they can still be reviewed.
const MAIN = 'www.tierrafirme.lat';
const OLD_HOSTS = new Set(['tierra-firme.pages.dev', 'tierrafirme.lat']);

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (OLD_HOSTS.has(url.hostname)) {
    url.hostname = MAIN;
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
