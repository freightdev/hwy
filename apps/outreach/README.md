# Trucking Outreach / Freightdev

A working SvelteKit application for selling Freightdev websites, landing pages, forms, and simple systems to trucking companies.

## What exists now

- Public Freightdev landing page
- Project intake form
- Local inquiry logging to `data/inquiries.jsonl`
- Resend-ready email notification path
- Secret key inventory in `SECRETS.md`
- Local secret template in `.env.secrets`

## Local setup

```bash
cd /ws/projects/trucking-outreach
npm install
cp .env.example .env
npm run dev
```

Open the dev URL printed by Vite.

## Resend setup

Add these values to `.env` for local development or your deployment secret manager for production:

```bash
RESEND_API_KEY=your_resend_key
RESEND_FROM_EMAIL=verified_sender@example.com
RESEND_FROM_NAME=Freightdev
CONTACT_FORM_TO_EMAIL=jesse.freightdev@gmail.com
```

Use a Resend-verified sender/domain for `RESEND_FROM_EMAIL`.
If `RESEND_API_KEY` is missing, form submissions are still saved locally but no email notification is sent.

## Commands

```bash
npm run check
npm run build
npm run dev
```

## Notes

Do not commit real secrets. `.env`, `.env.*`, `.env.secrets`, and local inquiry logs are ignored by git.
