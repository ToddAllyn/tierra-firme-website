// Sends visitors on the old pages.dev address and on www to the main domain, keeping the path.
// Branch previews (<branch>.tierra-firme.pages.dev) are left alone so they can still be reviewed.
const MAIN = 'tierrafirme.lat';
const OLD_HOSTS = new Set(['tierra-firme.pages.dev', 'www.tierrafirme.lat']);

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (OLD_HOSTS.has(url.hostname)) {
    url.hostname = MAIN;
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
