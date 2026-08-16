const CHANGELOG_REPO = 'https://github.com/4DRIAN0RTIZ/autoCover';

let changelogData = null;

async function loadChangelogData() {
  if (changelogData) return changelogData;

  const res = await fetch('changelog.json');
  if (!res.ok) throw new Error('changelog.json not found');

  changelogData = await res.json();
  return changelogData;
}

async function updateHeroBadgeRelease() {
  const field = document.getElementById('hero-badge-release');
  if (!field) return;

  try {
    const releases = await loadChangelogData();
    const version = releases?.[0]?.version || 'unreleased';
    field.textContent = version;
  } catch (error) {
    console.error('Error fetching changelog.json:', error);
    field.textContent = 'unreleased';
  }
}

const CHANGELOG_GROUP_TAGS = {
  Features: 'tag-feat',
  'Bug Fixes': 'tag-fix',
  Documentation: 'tag-docs',
  Refactor: 'tag-refactor',
  Performance: 'tag-feat',
};

function changelogTagClass(group) {
  return CHANGELOG_GROUP_TAGS[group] || 'tag-chore';
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

async function loadChangelog() {
  const container = document.getElementById('changelog-content');
  if (!container) return;

  try {
    const releases = await loadChangelogData();

    const withCommits = (releases || []).filter(r => (r.commits || []).length > 0);
    if (withCommits.length === 0) {
      renderChangelogEmpty(container);
      return;
    }

    const unreleased = withCommits.filter(r => !r.version);
    const latestTagged = withCommits.find(r => r.version);
    const visible = [...unreleased, ...(latestTagged ? [latestTagged] : [])];

    const latestTimestamp = visible[0]?.commits?.[0]?.author?.timestamp;
    const footerUpdated = document.getElementById('footer-updated');
    if (footerUpdated && latestTimestamp) {
      const date = new Date(latestTimestamp * 1000).toISOString().slice(0, 10);
      footerUpdated.textContent = `Last updated: ${date}`;
    }

    container.innerHTML = visible.map(release => {
      const version = release.version || 'Unreleased';
      const date = release.timestamp
        ? new Date(release.timestamp * 1000).toISOString().slice(0, 10)
        : '';

      const entries = (release.commits || []).map(c => {
        const tagClass = changelogTagClass(c.group);
        const label = c.group || 'Other';
        const sha = (c.id || '').slice(0, 7);
        const url = c.id ? `${CHANGELOG_REPO}/commit/${c.id}` : null;
        return `
          <div class="changelog-entry">
            <span class="tag ${tagClass}">${escapeHtml(label)}</span>
            <span>${escapeHtml(c.message || '')}</span>
            ${url ? `<a href="${url}" target="_blank" rel="noopener">${sha}</a>` : ''}
          </div>`;
      }).join('');

      return `
        <div class="changelog-version">
          <h3>${escapeHtml(version)} ${date ? `<span class="changelog-date">— ${date}</span>` : ''}</h3>
          ${entries}
        </div>`;
    }).join('');
  } catch (e) {
    renderChangelogEmpty(container);
  }
}

function renderChangelogEmpty(container) {
  container.innerHTML = '<p class="changelog-empty">No changelog entries yet — check back after the next release.</p>';
}

document.addEventListener('DOMContentLoaded', async () => {
  document.querySelectorAll('.code-block, details.code-details').forEach(block => {
    const header = block.querySelector('.code-header') || block.querySelector('summary');
    const body = block.querySelector('.code-body');
    if (!header || !body) return;

    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.textContent = 'copy';
    copyBtn.addEventListener('click', e => {
      e.preventDefault();
      navigator.clipboard.writeText(body.innerText.trim()).then(() => {
        copyBtn.textContent = 'copied!';
        copyBtn.classList.add('copied');
        setTimeout(() => {
          copyBtn.textContent = 'copy';
          copyBtn.classList.remove('copied');
        }, 1500);
      });
    });
    header.appendChild(copyBtn);
  });

  await Promise.all([
    updateHeroBadgeRelease(),
    loadChangelog(),
  ]);
});
