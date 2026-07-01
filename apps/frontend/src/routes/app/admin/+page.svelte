<script>
  import { onMount } from 'svelte';
  import { get, patch } from '$lib/api.js';
  import { error as toastError, success as toastSuccess } from '$lib/stores/toast.js';

  let loading = true;
  let users = [];
  let roles = [];
  let permissions = [];
  let saving = '';

  $: groupedPermissions = permissions.reduce((groups, permission) => {
    groups[permission.group] = [...(groups[permission.group] || []), permission];
    return groups;
  }, {});

  async function loadAdmin() {
    loading = true;
    const [userResult, permissionResult] = await Promise.all([
      get('/admin/users'),
      get('/admin/permissions')
    ]);
    loading = false;
    if (userResult.error) toastError(userResult.error);
    if (permissionResult.error) toastError(permissionResult.error);
    users = userResult.data?.users || [];
    roles = permissionResult.data?.roles || [];
    permissions = permissionResult.data?.permissions || [];
  }

  function hasPermission(role, permissionKey) {
    return role.permissions?.includes(permissionKey);
  }

  async function togglePermission(role, permissionKey) {
    if (role.locked) return;
    saving = `${role.key}:${permissionKey}`;
    const next = !hasPermission(role, permissionKey);
    const { error: err } = await patch(`/admin/permissions/${role.key}/${permissionKey}`, { allowed: next });
    saving = '';
    if (err) { toastError(err); return; }
    toastSuccess('Permission updated');
    await loadAdmin();
  }

  async function changeRole(user, roleLabel) {
    const { error: err } = await patch(`/admin/users/${user.id}/role`, { role: roleLabel });
    if (err) { toastError(err); return; }
    toastSuccess('User role updated');
    await loadAdmin();
  }

  onMount(loadAdmin);
</script>

<svelte:head><title>Admin | HWY TMS</title></svelte:head>

<div class="admin-page">
  <header class="hero">
    <div>
      <div class="eyebrow">HWY Admin</div>
      <h1>Admin Command Center</h1>
      <p>Manage users, roles, and permissions for the whole trucking operating system.</p>
    </div>
    <a href="/signup" class="invite">Invite user</a>
  </header>

  {#if loading}
    <div class="loading">Loading users and permissions…</div>
  {:else}
    <section class="role-strip" aria-label="Role summary">
      {#each roles as role}
        <article class="role-card" class:locked={role.locked}>
          <div class="role-top"><h2>{role.label}</h2>{#if role.locked}<span>Locked</span>{/if}</div>
          <p>{role.description}</p>
          <strong>{role.member_count} people</strong>
        </article>
      {/each}
    </section>

    <section class="panel">
      <div class="panel-head">
        <div><h2>Team access</h2><p>Assign people to roles without touching password or company data.</p></div>
      </div>
      <div class="user-list">
        {#each users as person}
          <div class="user-row">
            <div class="avatar">{(person.name || person.email || '?').slice(0,1).toUpperCase()}</div>
            <div class="user-main">
              <strong>{person.name || person.email}</strong>
              <span>{person.email}</span>
            </div>
            <select aria-label={`Role for ${person.name || person.email}`} value={person.role_key} on:change={(event) => changeRole(person, event.currentTarget.value)}>
              {#each roles as role}
                <option value={role.key}>{role.label}</option>
              {/each}
            </select>
          </div>
        {/each}
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div><h2>Role permissions</h2><p>Admin is locked so HWY cannot lose an owner. Other roles are adjustable.</p></div>
      </div>
      <div class="permission-groups">
        {#each Object.entries(groupedPermissions) as [group, groupPermissions]}
          <div class="permission-group">
            <h3>{group}</h3>
            {#each groupPermissions as permission}
              <div class="permission-row">
                <div><strong>{permission.label}</strong><span>{permission.description}</span></div>
                <div class="toggles">
                  {#each roles as role}
                    <button
                      class:enabled={hasPermission(role, permission.key)}
                      class:locked={role.locked}
                      disabled={role.locked || saving === `${role.key}:${permission.key}`}
                      title={`${role.label}: ${permission.label}`}
                      on:click={() => togglePermission(role, permission.key)}
                    >{role.label.slice(0,3)}</button>
                  {/each}
                </div>
              </div>
            {/each}
          </div>
        {/each}
      </div>
    </section>
  {/if}
</div>

<style>
  .admin-page{min-height:100vh;background:#0b0f17;color:#f8fafc;padding:18px 18px 94px}.hero{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;padding:22px;border-radius:28px;background:radial-gradient(circle at 10% 0%,rgba(37,99,235,.28),transparent 40%),#111827;border:1px solid #1f2937}.eyebrow{color:#93c5fd;text-transform:uppercase;letter-spacing:.14em;font-size:11px;font-weight:900}.hero h1{font-size:clamp(30px,9vw,58px);letter-spacing:-.06em;line-height:.95;margin:8px 0}.hero p{color:#a8b3c7;line-height:1.55;margin:0}.invite{background:#2563eb;color:white;border-radius:14px;padding:12px 14px;font-weight:900;white-space:nowrap}.loading,.panel,.role-card{background:#111827;border:1px solid #1f2937;border-radius:24px}.loading{padding:28px;margin-top:14px;color:#cbd5e1}.role-strip{display:grid;gap:10px;margin:14px 0}.role-card{padding:18px}.role-card.locked{border-color:#2563eb}.role-top{display:flex;align-items:center;justify-content:space-between;gap:10px}.role-card h2{margin:0;font-size:18px}.role-card span{font-size:11px;color:#93c5fd;background:rgba(37,99,235,.18);border-radius:999px;padding:5px 8px}.role-card p{color:#94a3b8;font-size:13px;line-height:1.45}.role-card strong{font-size:13px}.panel{padding:18px;margin-top:14px}.panel-head{display:flex;justify-content:space-between;gap:12px;margin-bottom:14px}.panel h2{margin:0}.panel p{margin:5px 0 0;color:#94a3b8;font-size:13px}.user-list{display:grid;gap:10px}.user-row{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:center;padding:12px;border-radius:18px;background:#0b1220;border:1px solid #1e293b}.avatar{width:44px;height:44px;border-radius:15px;background:#1d4ed8;display:grid;place-items:center;font-weight:900}.user-main{min-width:0}.user-main strong,.user-main span{display:block;overflow:hidden;text-overflow:ellipsis}.user-main span{color:#94a3b8;font-size:12px}select{grid-column:1/-1;width:100%;background:#0f172a;border:1px solid #334155;color:#f8fafc;border-radius:13px;padding:11px}.permission-groups{display:grid;gap:12px}.permission-group{background:#0b1220;border:1px solid #1e293b;border-radius:20px;padding:14px}.permission-group h3{margin:0 0 12px;color:#93c5fd}.permission-row{display:grid;gap:12px;padding:12px 0;border-top:1px solid #1e293b}.permission-row:first-of-type{border-top:0}.permission-row strong,.permission-row span{display:block}.permission-row span{color:#94a3b8;font-size:12px;margin-top:3px}.toggles{display:flex;gap:6px;flex-wrap:wrap}.toggles button{border:1px solid #334155;background:#111827;color:#94a3b8;border-radius:999px;padding:8px 10px;font-size:11px;font-weight:900}.toggles button.enabled{background:#14532d;border-color:#22c55e;color:#dcfce7}.toggles button.locked{opacity:.55;cursor:not-allowed}
  @media(min-width:760px){.admin-page{padding:28px 34px 100px}.role-strip{grid-template-columns:repeat(3,1fr)}.user-row{grid-template-columns:auto 1fr 180px}select{grid-column:auto}.permission-row{grid-template-columns:minmax(220px,1fr) auto;align-items:center}}
</style>
