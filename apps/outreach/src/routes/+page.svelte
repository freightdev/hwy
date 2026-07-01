<script lang="ts">
  type IntakeValues = {
    name: string;
    company: string;
    email: string;
    phone: string;
    need: string;
    message: string;
  };

  const offers = [
    {
      title: 'Trucking landing pages',
      text: 'A clean, mobile-first page that makes a carrier, dispatcher, broker, repair shop, or recruiting operation look real and reachable.'
    },
    {
      title: 'Lead and quote forms',
      text: 'Turn calls, texts, PDFs, and scattered inbox messages into structured intake that can be followed up and measured.'
    },
    {
      title: 'Simple business systems',
      text: 'Small CRMs, driver application flows, document upload pages, customer intake, dispatch support, and practical automation.'
    }
  ];

  const workflow = ['Audit what is broken', 'Define the money task', 'Build the first working system', 'Measure leads and follow-up'];

  let values: IntakeValues = { name: '', company: '', email: '', phone: '', need: '', message: '' };
  let errors: Record<string, string> = {};
  let submitting = false;
  let success: { storedAt: string; email: { sent: boolean; reason: string } } | null = null;

  async function submitInquiry() {
    submitting = true;
    errors = {};
    success = null;

    const response = await fetch('/api/inquiries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values)
    });

    const result = await response.json();
    submitting = false;

    if (!response.ok || !result.ok) {
      errors = result.errors ?? { form: 'Something went wrong. Email jesse.freightdev@gmail.com directly.' };
      return;
    }

    success = { storedAt: result.storedAt, email: result.email };
    values = { name: '', company: '', email: '', phone: '', need: '', message: '' };
  }
</script>

<svelte:head>
  <title>Freightdev | Websites and systems for trucking companies</title>
</svelte:head>

<main class="shell">
  <section class="hero">
    <nav class="nav" aria-label="Main navigation">
      <strong>Freightdev</strong>
      <a href="mailto:jesse.freightdev@gmail.com">jesse.freightdev@gmail.com</a>
    </nav>

    <div class="hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">Built by trucking experience, not generic tech guesses.</p>
        <h1>Websites, landing pages, and simple systems for trucking companies.</h1>
        <p class="lead">
          Freightdev helps trucking businesses clean up their online presence, capture real leads,
          and replace messy manual processes with practical tools that fit how freight work actually happens.
        </p>
        <div class="actions">
          <a class="button primary" href="#contact">Start a project</a>
          <a class="button secondary" href="#offers">See what we build</a>
        </div>
      </div>

      <aside class="proof-card" aria-label="Project focus">
        <span>First wedge</span>
        <h2>Professional web presence + intake flow</h2>
        <p>
          Start with a landing page and lead form. Grow into CRM, follow-up, recruiting, or custom operations systems after the first win.
        </p>
        <ul>
          <li>Mobile-first</li>
          <li>Trucking-specific copy</li>
          <li>Lead capture</li>
          <li>Resend-ready notifications</li>
        </ul>
      </aside>
    </div>
  </section>

  <section id="offers" class="section">
    <p class="eyebrow">What we can sell right now</p>
    <h2>Start simple. Build toward the full system.</h2>
    <div class="cards">
      {#each offers as offer}
        <article class="card">
          <h3>{offer.title}</h3>
          <p>{offer.text}</p>
        </article>
      {/each}
    </div>
  </section>

  <section class="section split">
    <div>
      <p class="eyebrow">How Freightdev works</p>
      <h2>No fake business data. No magic. Just useful systems.</h2>
      <p>
        Every build starts by finding the actual bottleneck: no website, weak credibility, lost leads,
        ugly forms, no follow-up, or manual workflows that waste time.
      </p>
    </div>
    <ol class="steps">
      {#each workflow as item, index}
        <li><span>{index + 1}</span>{item}</li>
      {/each}
    </ol>
  </section>

  <section id="contact" class="section contact">
    <div>
      <p class="eyebrow">Project intake</p>
      <h2>Tell me what your trucking business needs built.</h2>
      <p>
        Use this form for a landing page, website, driver application, quote form, CRM, or custom trucking workflow.
      </p>
    </div>

    {#if success}
      <div class="success" role="status">
        <h3>Inquiry saved.</h3>
        <p>Timestamp: {success.storedAt}</p>
        <p>Email notification: {success.email.sent ? 'sent through Resend' : 'not sent yet; inquiry is stored locally'}.</p>
        <button class="button primary" type="button" on:click={() => (success = null)}>Send another request</button>
      </div>
    {:else}
      <form on:submit|preventDefault={submitInquiry}>
        {#if errors.form}<p class="error full">{errors.form}</p>{/if}
        <label>
          Your name
          <input name="name" autocomplete="name" bind:value={values.name} />
          {#if errors.name}<small>{errors.name}</small>{/if}
        </label>
        <label>
          Company
          <input name="company" autocomplete="organization" bind:value={values.company} />
          {#if errors.company}<small>{errors.company}</small>{/if}
        </label>
        <label>
          Email
          <input name="email" type="email" autocomplete="email" bind:value={values.email} />
          {#if errors.email}<small>{errors.email}</small>{/if}
        </label>
        <label>
          Phone
          <input name="phone" autocomplete="tel" bind:value={values.phone} />
        </label>
        <label>
          What do you need?
          <select name="need" bind:value={values.need}>
            <option value="">Choose one</option>
            <option>Simple landing page</option>
            <option>Full company website</option>
            <option>Lead / quote form</option>
            <option>Driver application flow</option>
            <option>CRM or follow-up system</option>
            <option>Custom trucking system</option>
          </select>
          {#if errors.need}<small>{errors.need}</small>{/if}
        </label>
        <label class="full">
          What is broken or missing right now?
          <textarea name="message" rows="5" bind:value={values.message}></textarea>
          {#if errors.message}<small>{errors.message}</small>{/if}
        </label>
        <button class="button primary" type="submit" disabled={submitting}>{submitting ? 'Sending...' : 'Send project request'}</button>
      </form>
    {/if}
  </section>
</main>
