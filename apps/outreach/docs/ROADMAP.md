# Trucking Outreach Application Roadmap

## Done in the first build

- SvelteKit app scaffold
- Freightdev landing page
- Project intake form
- Validation for bad submissions
- Local JSONL inquiry logging
- Resend-ready email notification endpoint
- Secret key documentation
- Build and check scripts

## Next build targets

1. Add a real lead/admin dashboard
   - View submitted inquiries
   - Mark status: new, contacted, quoted, won, lost
   - Add notes and next follow-up date

2. Add package/pricing page
   - Starter landing page
   - Growth website + intake system
   - Custom system package

3. Add reusable trucking client templates
   - Carrier landing page
   - Dispatcher landing page
   - Driver recruiting page
   - Repair/service shop page

4. Add deployment target
   - Node adapter is already configured
   - Choose host: VPS, Cloudflare, Render, Railway, or existing /ws deployment pattern

5. Add real email sending
   - Paste `RESEND_API_KEY` into `.env.secrets` or deployment secrets
   - Set `RESEND_FROM_EMAIL` to a verified sender/domain
   - Set `CONTACT_FORM_TO_EMAIL=jesse.freightdev@gmail.com`

## Definition of done for future features

- Built
- Checked
- Verified with real request/output
- No fake production-like data left behind
- Secrets documented by key, not value
