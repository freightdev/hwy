# SECRETS.md

This file documents the secret keys used by the Trucking Outreach project.

Do not put actual secret values in this file.
Actual values belong in `.env.secrets` or the deployment platform's secret manager.

## Email account

- `FREIGHTDEV_EMAIL_ADDRESS`
  - Business email address used for outreach and client communication.
  - Example purpose: `jesse.freightdev@gmail.com`.

- `FREIGHTDEV_EMAIL_APP_PASSWORD`
  - App-specific password for the business email account.
  - Prefer a Gmail App Password with 2FA enabled instead of the real account password.

## Resend email sending

Use Resend for outbound email when possible. The free tier supports a limited daily send volume, which is useful for early outreach/testing.

- `RESEND_API_KEY`
  - API key from Resend.
  - Paste the value only into `.env.secrets` or your deployment secret manager.
  - Expected format usually starts with `re_`.

- `RESEND_FROM_EMAIL`
  - Verified sender email/domain used by Resend.
  - Example: `outreach@yourdomain.com` once a domain is verified.

- `RESEND_FROM_NAME`
  - Display name used on outbound emails.
  - Example: `Freightdev`.

## SMTP sending

Use SMTP only if not using Resend or if reply-reading/mailbox integration requires it.

- `SMTP_HOST`
  - SMTP server hostname.
  - Gmail default: `smtp.gmail.com`.

- `SMTP_PORT`
  - SMTP server port.
  - Gmail TLS default: `587`.

- `SMTP_USERNAME`
  - Username for SMTP authentication.
  - Usually the business email address.

- `SMTP_PASSWORD`
  - Password or app password for SMTP authentication.

- `SMTP_FROM_NAME`
  - Display name used on outgoing emails.

- `SMTP_FROM_EMAIL`
  - From email address used on outgoing emails.

## IMAP reply reading

- `IMAP_HOST`
  - IMAP server hostname.
  - Gmail default: `imap.gmail.com`.

- `IMAP_PORT`
  - IMAP server port.
  - Gmail SSL default: `993`.

- `IMAP_USERNAME`
  - Username for IMAP authentication.
  - Usually the business email address.

- `IMAP_PASSWORD`
  - Password or app password for IMAP authentication.

## Google OAuth

Use these if the project connects to Gmail/Google through OAuth instead of SMTP/IMAP passwords.

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`
- `GOOGLE_REDIRECT_URI`

## CRM / storage integrations

- `AIRTABLE_API_KEY`
- `AIRTABLE_BASE_ID`
- `AIRTABLE_TABLE_NAME`
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`

## Website / form notifications

- `CONTACT_FORM_TO_EMAIL`
  - Email address that receives form submissions.

- `CONTACT_FORM_FROM_EMAIL`
  - Email address used by the form system when sending notifications.

- `CONTACT_FORM_WEBHOOK_SECRET`
  - Shared secret used to verify incoming form/webhook requests.

## SMS / phone integrations

Use only if SMS or phone automation is added.

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`

## AI/provider keys

Use only if outreach drafting, enrichment, summarization, or agent workflows call external AI APIs.

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `OPENROUTER_API_KEY`

## Lead data / enrichment providers

Use only if the project connects to external lead or data enrichment providers.

- `APOLLO_API_KEY`
- `HUNTER_API_KEY`
- `CLEARBIT_API_KEY`
- `GOOGLE_MAPS_API_KEY`

## App/session security

- `APP_SECRET_KEY`
  - General app secret for signing/verifying internal tokens.

- `JWT_SECRET`
  - Secret used to sign JWTs, if JWT auth is used.

- `ENCRYPTION_KEY`
  - Key used for encrypting stored sensitive data.

## Deployment/database

- `DATABASE_URL`
  - Database connection string.

- `REDIS_URL`
  - Redis connection string, if queues/cache/session storage use Redis.

## Rules

- Never commit `.env.secrets` with real values.
- Never paste real passwords into project docs.
- Prefer OAuth or app-specific passwords over master account passwords.
- Rotate any secret that is accidentally exposed.
- Give every environment its own secrets: local, staging, production.
