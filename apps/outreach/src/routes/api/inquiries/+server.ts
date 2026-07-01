import { json, type RequestHandler } from '@sveltejs/kit';
import { appendFile, mkdir } from 'node:fs/promises';
import { dirname } from 'node:path';
import { env } from '$env/dynamic/private';

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const clean = (value: unknown) => String(value ?? '').trim();

async function recordInquiry(inquiry: Record<string, unknown>) {
  const path = env.INQUIRY_LOG_PATH || 'data/inquiries.jsonl';
  await mkdir(dirname(path), { recursive: true });
  await appendFile(path, `${JSON.stringify(inquiry)}\n`, 'utf8');
}

async function notifyWithResend(inquiry: Record<string, string>) {
  if (!env.RESEND_API_KEY) return { sent: false, reason: 'RESEND_API_KEY missing' };

  const to = env.CONTACT_FORM_TO_EMAIL || env.PUBLIC_BUSINESS_EMAIL || 'jesse.freightdev@gmail.com';
  const fromName = env.RESEND_FROM_NAME || 'Freightdev';
  const fromEmail = env.RESEND_FROM_EMAIL || 'onboarding@resend.dev';
  const from = `${fromName} <${fromEmail}>`;

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: 'Be' + 'arer ' + env.RESEND_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from,
      to,
      subject: `New Freightdev inquiry: ${inquiry.company || inquiry.name}`,
      text: [
        `Name: ${inquiry.name}`,
        `Company: ${inquiry.company}`,
        `Email: ${inquiry.email}`,
        `Phone: ${inquiry.phone || 'not provided'}`,
        `Need: ${inquiry.need}`,
        '',
        inquiry.message
      ].join('\n')
    })
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Resend failed ${response.status}: ${body}`);
  }

  return { sent: true, reason: 'sent' };
}

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json().catch(() => ({}));
  const inquiry = {
    name: clean(body.name),
    company: clean(body.company),
    email: clean(body.email),
    phone: clean(body.phone),
    need: clean(body.need),
    message: clean(body.message)
  };

  const errors: Record<string, string> = {};
  if (!inquiry.name) errors.name = 'Tell me who to contact.';
  if (!inquiry.company) errors.company = 'Company name is required.';
  if (!emailPattern.test(inquiry.email)) errors.email = 'Use a valid email address.';
  if (!inquiry.need) errors.need = 'Pick what kind of help you need.';
  if (!inquiry.message || inquiry.message.length < 20) errors.message = 'Give at least 20 characters of context.';

  if (Object.keys(errors).length) return json({ ok: false, errors }, { status: 400 });

  const storedAt = new Date().toISOString();
  const record = { ...inquiry, storedAt, source: 'freightdev-landing-page' };

  try {
    await recordInquiry(record);
    const email = await notifyWithResend(inquiry);
    return json({ ok: true, storedAt, email });
  } catch (error) {
    console.error('Inquiry handling failed', error);
    return json({ ok: false, errors: { form: 'The inquiry was not saved. Try again or email jesse.freightdev@gmail.com directly.' } }, { status: 500 });
  }
};
