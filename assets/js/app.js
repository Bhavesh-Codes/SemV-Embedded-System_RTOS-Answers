/**
 * Embedded Systems & RTOS Study Guide - Technical Datasheet Design System
 * 
 * Features:
 * - 0. In-place toggling (no scroll jump, no accordion collapse, no full re-render)
 * - 1. Persistent text highlighting (4 colors, cross-element, touch, export/import)
 * - 2. 100% Offline KaTeX math rendering with fallback
 * - 3. Technical typography & type scale
 * - 4. Accessibility (:focus-visible, aria-expanded, aria-pressed, role="progressbar")
 * - 5. Print stylesheet support
 * - 6. Search hotkeys ('/', Ctrl+K, Esc, arrow key navigation)
 * - 7. Compact layout & SVG filter icons
 * - 8. Technical datasheet visual identity & Dark theme toggle
 * - 9. Dynamic question counts & zero CORS file:// execution
 */

// ==========================================================================
// Safe Storage with In-Memory Fallback
// ==========================================================================
const storage = {
  _mem: {},
  getItem(key) {
    try {
      const val = localStorage.getItem(key);
      return val !== null ? val : (this._mem[key] || null);
    } catch (e) {
      return this._mem[key] || null;
    }
  },
  setItem(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      this._mem[key] = String(value);
    }
  },
  removeItem(key) {
    try {
      localStorage.removeItem(key);
    } catch (e) {
      delete this._mem[key];
    }
  }
};

// ==========================================================================
// Global Application State
// ==========================================================================
let studyData = [];
let currentModuleId = 1;
let currentFilter = 'all'; // 'all', 'starred', 'completed', 'uncompleted', 'high-pyq', 'musa', 'syllabus'
let searchQuery = '';
let searchResultsList = [];
let selectedSearchIndex = -1;

// User Data Sets
let starredQuestions = new Set();
let completedQuestions = new Set();
let starredModules = new Set();
let questionHighlights = {}; // { [qId]: [ { id, color, text, prefix, suffix, offsetHint } ] }

// Active Highlight Selection Context
let currentSelectionRange = null;
let currentHighlightTarget = null; // clicked existing <mark>

// DOM Elements
const sidebarNav = document.getElementById('sidebar-nav');
const contentContainer = document.getElementById('content-container');
const searchInput = document.getElementById('search-input');
const searchDropdown = document.getElementById('search-dropdown');
const filterChips = document.querySelectorAll('.filter-chip');
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');
const backToTopBtn = document.getElementById('back-to-top');
const expandAllBtn = document.getElementById('btn-expand-all');
const collapseAllBtn = document.getElementById('btn-collapse-all');
const themeToggleBtn = document.getElementById('btn-theme-toggle');
const themeIconSun = document.getElementById('theme-icon-sun');
const themeIconMoon = document.getElementById('theme-icon-moon');
const highlightToolbar = document.getElementById('highlight-toolbar');
const backupModal = document.getElementById('backup-modal');
const btnExportImport = document.getElementById('btn-export-import');
const btnCloseModal = document.getElementById('btn-close-modal');
const btnDoExport = document.getElementById('btn-do-export');
const importFileInput = document.getElementById('import-file-input');

// ==========================================================================
// Initialization
// ==========================================================================
document.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  loadSavedUserData();
  setupEventListeners();
  await loadAllModuleData();
  computeGlobalStats();
  renderSidebar();
  renderCurrentModule();
});

// Theme Management
function initTheme() {
  const savedTheme = storage.getItem('es_theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const activeTheme = savedTheme ? savedTheme : (prefersDark ? 'dark' : 'light');
  applyTheme(activeTheme);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  storage.setItem('es_theme', theme);
  if (themeIconSun && themeIconMoon) {
    if (theme === 'dark') {
      themeIconSun.style.display = 'inline';
      themeIconMoon.style.display = 'none';
    } else {
      themeIconSun.style.display = 'none';
      themeIconMoon.style.display = 'inline';
    }
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

// User Data Loading & Persistence
function loadSavedUserData() {
  try {
    const stars = storage.getItem('es_starred_questions');
    if (stars) starredQuestions = new Set(JSON.parse(stars));

    const comp = storage.getItem('es_completed_questions');
    if (comp) completedQuestions = new Set(JSON.parse(comp));

    const modStars = storage.getItem('es_starred_modules');
    if (modStars) starredModules = new Set(JSON.parse(modStars));

    const hls = storage.getItem('es_highlights');
    if (hls) questionHighlights = JSON.parse(hls);
  } catch (e) {
    console.warn('Error reading saved user data:', e);
  }
}

function saveUserData() {
  storage.setItem('es_starred_questions', JSON.stringify(Array.from(starredQuestions)));
  storage.setItem('es_completed_questions', JSON.stringify(Array.from(completedQuestions)));
  storage.setItem('es_starred_modules', JSON.stringify(Array.from(starredModules)));
  storage.setItem('es_highlights', JSON.stringify(questionHighlights));
}

// Load Modules
async function loadAllModuleData() {
  studyData = [];
  for (let i = 1; i <= 6; i++) {
    if (window.embeddedStudyData && window.embeddedStudyData[i]) {
      studyData.push(window.embeddedStudyData[i]);
      continue;
    }
    try {
      const res = await fetch(`data/mod${i}_answers.json`);
      if (res.ok) studyData.push(await res.json());
    } catch (e) {
      if (window.embeddedStudyData && window.embeddedStudyData[i]) {
        studyData.push(window.embeddedStudyData[i]);
      }
    }
  }
  studyData.sort((a, b) => a.module - b.module);
}

// Compute dynamic stats and fill labels
function computeGlobalStats() {
  let totalQuestions = 0;
  let highYieldCount = 0;

  studyData.forEach(mod => {
    (mod.topics || []).forEach(t => {
      (t.questions || []).forEach(q => {
        totalQuestions++;
        const isHigh = (q.tags || []).some(tag => {
          const m = tag.match(/x(\d+)/i);
          return m && parseInt(m[1]) >= 3;
        });
        if (isHigh) highYieldCount++;
      });
    });
  });

  // Update DOM counts dynamically
  const totalElem = document.getElementById('total-questions-count');
  if (totalElem) totalElem.textContent = `${totalQuestions} Questions`;

  const totalStat = document.getElementById('syllabus-total-stat');
  if (totalStat) totalStat.textContent = totalQuestions;

  const highElem = document.getElementById('high-freq-count');
  if (highElem) highElem.textContent = `${highYieldCount} High-Yield`;

  const chipAll = document.getElementById('chip-count-all');
  if (chipAll) chipAll.textContent = totalQuestions;

  updateCountersInPlace();
}

// ==========================================================================
// 0. In-Place Toggles (Star & Complete) - No Scroll Jump, No Accordion Reset
// ==========================================================================
window.toggleStarQuestion = function(qId, event) {
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }

  const isStarred = starredQuestions.has(qId);
  if (isStarred) {
    starredQuestions.delete(qId);
  } else {
    starredQuestions.add(qId);
  }
  saveUserData();

  // Update card DOM in place
  const cardId = 'q-' + qId.replace(/\./g, '-');
  const card = document.getElementById(cardId);
  if (card) {
    card.classList.toggle('is-starred', !isStarred);
    const starBtn = card.querySelector('.btn-q-star');
    if (starBtn) {
      starBtn.classList.toggle('active', !isStarred);
      starBtn.setAttribute('aria-pressed', String(!isStarred));
      starBtn.setAttribute('title', !isStarred ? 'Unstar question' : 'Star question');
      const starSvg = starBtn.querySelector('svg');
      if (starSvg) {
        starSvg.setAttribute('fill', !isStarred ? 'var(--status-star)' : 'none');
      }
      const label = starBtn.querySelector('.btn-action-label');
      if (label) label.textContent = !isStarred ? 'Starred' : 'Star';
    }

    // If active filter is 'starred' and item unstarred, keep visible but dimmed
    if (currentFilter === 'starred') {
      card.classList.toggle('is-filter-dimmed', isStarred);
    }
  }

  updateCountersInPlace();
};

window.toggleCompleteQuestion = function(qId, event) {
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }

  const isCompleted = completedQuestions.has(qId);
  if (isCompleted) {
    completedQuestions.delete(qId);
  } else {
    completedQuestions.add(qId);
  }
  saveUserData();

  // Update card DOM in place
  const cardId = 'q-' + qId.replace(/\./g, '-');
  const card = document.getElementById(cardId);
  if (card) {
    card.classList.toggle('is-completed', !isCompleted);
    const tickBtn = card.querySelector('.btn-q-tick');
    if (tickBtn) {
      tickBtn.classList.toggle('active', !isCompleted);
      tickBtn.setAttribute('aria-pressed', String(!isCompleted));
      tickBtn.setAttribute('title', !isCompleted ? 'Mark uncompleted' : 'Mark completed');
      const label = tickBtn.querySelector('.btn-action-label');
      if (label) label.textContent = !isCompleted ? 'Completed' : 'Mark done';
    }

    // Completed badge in question meta
    const metaArea = card.querySelector('.question-meta');
    if (metaArea) {
      let badge = metaArea.querySelector('.badge-completed');
      if (!isCompleted && !badge) {
        badge = document.createElement('span');
        badge.className = 'badge badge-completed';
        badge.textContent = '✓ Completed';
        metaArea.prepend(badge);
      } else if (isCompleted && badge) {
        badge.remove();
      }
    }

    // If active filter is completed/uncompleted, keep visible but dimmed
    if (currentFilter === 'completed') {
      card.classList.toggle('is-filter-dimmed', isCompleted);
    } else if (currentFilter === 'uncompleted') {
      card.classList.toggle('is-filter-dimmed', !isCompleted);
    }
  }

  updateCountersInPlace();
};

window.toggleStarModule = function(modId, event) {
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }
  modId = parseInt(modId);

  const isStarred = starredModules.has(modId);
  if (isStarred) {
    starredModules.delete(modId);
  } else {
    starredModules.add(modId);
  }
  saveUserData();

  // Update module hero button in place
  const modHero = document.querySelector(`.module-section[id="module-${modId}"] .module-hero-slim`);
  if (modHero) {
    const starBtn = modHero.querySelector('.btn-module-star');
    if (starBtn) {
      starBtn.classList.toggle('starred', !isStarred);
      starBtn.setAttribute('aria-pressed', String(!isStarred));
      starBtn.querySelector('span').textContent = !isStarred ? '★ Starred' : '☆ Star module';
    }
  }

  updateCountersInPlace();
};

window.toggleCompleteAllModule = function(modId, event) {
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }
  modId = parseInt(modId);

  const mod = studyData.find(m => m.module === modId);
  if (!mod) return;

  const allQIds = [];
  (mod.topics || []).forEach(t => {
    (t.questions || []).forEach(q => allQIds.push(q.id));
  });

  const allDone = allQIds.every(id => completedQuestions.has(id));

  allQIds.forEach(id => {
    if (allDone) {
      completedQuestions.delete(id);
    } else {
      completedQuestions.add(id);
    }
    // Update individual cards currently displayed
    const card = document.getElementById('q-' + id.replace(/\./g, '-'));
    if (card) {
      card.classList.toggle('is-completed', !allDone);
      const tickBtn = card.querySelector('.btn-q-tick');
      if (tickBtn) {
        tickBtn.classList.toggle('active', !allDone);
        tickBtn.setAttribute('aria-pressed', String(!allDone));
        const label = tickBtn.querySelector('.btn-action-label');
        if (label) label.textContent = !allDone ? 'Completed' : 'Mark done';
      }
      const metaArea = card.querySelector('.question-meta');
      if (metaArea) {
        let badge = metaArea.querySelector('.badge-completed');
        if (!allDone && !badge) {
          badge = document.createElement('span');
          badge.className = 'badge badge-completed';
          badge.textContent = '✓ Completed';
          metaArea.prepend(badge);
        } else if (allDone && badge) {
          badge.remove();
        }
      }
    }
  });

  saveUserData();
  updateCountersInPlace();
};

// Update dependent counters, progress bars, and sidebar badges in place
function updateCountersInPlace() {
  let totalAll = 0;
  let completedAll = 0;
  let starredAll = 0;

  studyData.forEach(mod => {
    let modTotal = 0;
    let modCompleted = 0;
    let modHasStar = starredModules.has(mod.module);

    (mod.topics || []).forEach(t => {
      (t.questions || []).forEach(q => {
        totalAll++;
        modTotal++;
        if (completedQuestions.has(q.id)) {
          completedAll++;
          modCompleted++;
        }
        if (starredQuestions.has(q.id)) {
          starredAll++;
          modHasStar = true;
        }
      });
    });

    // Update sidebar nav item for this module
    const navItem = document.querySelector(`.nav-item[data-mod-id="${mod.module}"]`);
    if (navItem) {
      const badge = navItem.querySelector('.nav-item-meta');
      if (badge) {
        const isAll = modTotal > 0 && modCompleted === modTotal;
        badge.innerHTML = isAll 
          ? `<span class="nav-completed-badge">✓ Done</span>`
          : `<span class="nav-badge">${modCompleted}/${modTotal}</span>`;
      }
      const starIndicator = navItem.querySelector('.nav-star-indicator');
      if (modHasStar && !starIndicator) {
        const star = document.createElement('span');
        star.className = 'nav-star-indicator';
        star.textContent = '★';
        navItem.querySelector('.nav-item-title-wrapper').prepend(star);
      } else if (!modHasStar && starIndicator) {
        starIndicator.remove();
      }
    }

    // Update active module hero progress
    if (mod.module === currentModuleId) {
      const modHero = document.querySelector(`.module-section[id="module-${mod.module}"] .module-hero-slim`);
      if (modHero) {
        const pct = modTotal > 0 ? Math.round((modCompleted / modTotal) * 100) : 0;
        const progressFill = modHero.querySelector('.progress-bar-fill');
        if (progressFill) progressFill.style.width = `${pct}%`;

        const progressLabel = modHero.querySelector('.module-hero-progress-text');
        if (progressLabel) progressLabel.textContent = `${modCompleted} of ${modTotal} completed (${pct}%)`;

        const markAllBtn = modHero.querySelector('.btn-module-complete-all');
        if (markAllBtn) {
          const isAll = modTotal > 0 && modCompleted === modTotal;
          markAllBtn.classList.toggle('completed', isAll);
          markAllBtn.setAttribute('aria-pressed', String(isAll));
          markAllBtn.querySelector('span').textContent = isAll ? '✓ All done' : 'Mark all done';
        }
      }
    }
  });

  // Overall syllabus progress
  const pctAll = totalAll > 0 ? Math.round((completedAll / totalAll) * 100) : 0;
  const pctElem = document.getElementById('syllabus-progress-pct');
  if (pctElem) pctElem.textContent = `${pctAll}%`;

  const barElem = document.getElementById('syllabus-progress-bar');
  if (barElem) barElem.style.width = `${pctAll}%`;

  const trackElem = document.getElementById('syllabus-progress-track');
  if (trackElem) trackElem.setAttribute('aria-valuenow', pctAll);

  const compElem = document.getElementById('syllabus-completed-count');
  if (compElem) compElem.textContent = completedAll;

  const starElem = document.getElementById('syllabus-starred-count');
  if (starElem) starElem.textContent = starredAll;

  // Filter chip badge counts
  const filterStar = document.getElementById('filter-starred-count');
  if (filterStar) filterStar.textContent = starredAll;

  const filterComp = document.getElementById('filter-completed-count');
  if (filterComp) filterComp.textContent = completedAll;
}

// ==========================================================================
// Sidebar Rendering
// ==========================================================================
function renderSidebar() {
  if (!sidebarNav) return;
  sidebarNav.innerHTML = '';

  const navSection = document.createElement('div');
  navSection.className = 'nav-section-title';
  navSection.textContent = 'Curriculum modules';
  sidebarNav.appendChild(navSection);

  studyData.forEach(mod => {
    let qCount = 0;
    let completedInMod = 0;
    let hasStarInMod = starredModules.has(mod.module);

    (mod.topics || []).forEach(t => {
      (t.questions || []).forEach(q => {
        qCount++;
        if (completedQuestions.has(q.id)) completedInMod++;
        if (starredQuestions.has(q.id)) hasStarInMod = true;
      });
    });

    const isAll = qCount > 0 && completedInMod === qCount;

    const a = document.createElement('a');
    a.className = `nav-item ${mod.module === currentModuleId ? 'active' : ''}`;
    a.dataset.modId = mod.module;
    a.href = `#module-${mod.module}`;
    a.setAttribute('role', 'button');

    a.innerHTML = `
      <div class="nav-item-title-wrapper">
        ${hasStarInMod ? `<span class="nav-star-indicator">★</span>` : ''}
        <span>Mod ${mod.module}: ${escapeHtml(mod.title.split('&')[0].trim())}</span>
      </div>
      <div class="nav-item-meta">
        ${isAll ? `<span class="nav-completed-badge">✓ Done</span>` : `<span class="nav-badge">${completedInMod}/${qCount}</span>`}
      </div>
    `;

    a.addEventListener('click', (e) => {
      e.preventDefault();
      switchModule(mod.module);
      closeMobileSidebar();
    });

    sidebarNav.appendChild(a);
  });
}

function switchModule(modId) {
  currentModuleId = parseInt(modId);

  document.querySelectorAll('.nav-item').forEach(el => {
    const isActive = parseInt(el.dataset.modId) === currentModuleId;
    el.classList.toggle('active', isActive);
  });

  renderCurrentModule();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==========================================================================
// Module & Question Rendering (Slim Layout & Accessible Buttons)
// ==========================================================================
function renderCurrentModule() {
  if (!contentContainer) return;
  const mod = studyData.find(m => m.module === currentModuleId);
  if (!mod) {
    contentContainer.innerHTML = `<div style="padding:40px; text-align:center;">Loading curriculum...</div>`;
    return;
  }

  let totalModQuestions = 0;
  let completedMod = 0;
  (mod.topics || []).forEach(t => {
    (t.questions || []).forEach(q => {
      totalModQuestions++;
      if (completedQuestions.has(q.id)) completedMod++;
    });
  });

  const pct = totalModQuestions > 0 ? Math.round((completedMod / totalModQuestions) * 100) : 0;
  const isModStarred = starredModules.has(mod.module);
  const isAllDone = totalModQuestions > 0 && completedMod === totalModQuestions;

  let html = `
    <div class="module-section active" id="module-${mod.module}">
      <!-- Slim Module Hero Header -->
      <header class="module-hero-slim">
        <div class="module-hero-main">
          <div class="module-hero-title-area">
            <span class="module-hero-badge">Module ${mod.module}</span>
            <h1 class="module-hero-title">${escapeHtml(mod.title)}</h1>
          </div>
          <div class="module-hero-actions">
            <button type="button" class="btn-module-action btn-module-star ${isModStarred ? 'starred' : ''}" onclick="toggleStarModule(${mod.module}, event)" aria-pressed="${isModStarred}" aria-label="Star module ${mod.module}">
              <span>${isModStarred ? '★ Starred' : '☆ Star module'}</span>
            </button>
            <button type="button" class="btn-module-action btn-module-complete-all ${isAllDone ? 'completed' : ''}" onclick="toggleCompleteAllModule(${mod.module}, event)" aria-pressed="${isAllDone}" aria-label="Mark all questions in module ${mod.module} completed">
              <span>${isAllDone ? '✓ All done' : 'Mark all done'}</span>
            </button>
          </div>
        </div>
        <div class="module-hero-progress">
          <span class="module-hero-progress-text">${completedMod} of ${totalModQuestions} completed (${pct}%)</span>
          <div class="module-hero-progress-track" role="progressbar" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100" aria-label="Module ${mod.module} completion">
            <div class="progress-bar-fill" style="width:${pct}%;"></div>
          </div>
        </div>
      </header>
  `;

  let renderedCount = 0;

  (mod.topics || []).forEach(topic => {
    const questions = (topic.questions || []).filter(q => matchesFilter(q));
    if (questions.length === 0 && currentFilter !== 'all') return;
    renderedCount += questions.length;

    html += `
      <section class="topic-group" id="topic-${topic.id.replace('.', '-')}" aria-labelledby="heading-${topic.id.replace('.', '-')}">
        <div class="topic-header">
          <h2 class="topic-title" id="heading-${topic.id.replace('.', '-')}">
            <span class="topic-id-badge">${topic.id}</span>
            <span>${escapeHtml(topic.title)}</span>
          </h2>
          <span style="font-size:11.5px; color:var(--text-muted);">${questions.length} questions</span>
        </div>
        <div class="question-list">
    `;

    questions.forEach(q => {
      html += renderQuestionCard(q);
    });

    html += `
        </div>
      </section>
    `;
  });

  if (renderedCount === 0) {
    html += `
      <div style="padding: 32px 16px; text-align: center; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); margin: 20px 0;">
        <p style="font-size: 13.5px; color: var(--text-muted);">No questions match the current filter.</p>
      </div>
    `;
  }

  // Footer Prev / Next
  const prevMod = studyData.find(m => m.module === currentModuleId - 1);
  const nextMod = studyData.find(m => m.module === currentModuleId + 1);

  html += `
    <nav class="module-nav-footer" aria-label="Module pagination">
      ${prevMod ? `
        <button type="button" class="nav-page-btn" onclick="switchModule(${prevMod.module})" aria-label="Go to previous module">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
          Previous: Mod ${prevMod.module}
        </button>
      ` : `<div></div>`}
      ${nextMod ? `
        <button type="button" class="nav-page-btn" onclick="switchModule(${nextMod.module})" aria-label="Go to next module">
          Next: Mod ${nextMod.module}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      ` : `<div></div>`}
    </nav>
  </div>`;

  contentContainer.innerHTML = html;

  // Apply math & highlights to the newly rendered module
  applyMathInContainer(contentContainer);
  applyHighlightsToContainer(contentContainer);
  setupCodeCopyButtons();
}

function renderQuestionCard(q) {
  const isStarred = starredQuestions.has(q.id);
  const isCompleted = completedQuestions.has(q.id);
  const qHighlights = questionHighlights[q.id] || [];
  const hlCount = qHighlights.length;
  const safeId = `q-${q.id.replace(/\./g, '-')}`;
  const answerId = `answer-${q.id.replace(/\./g, '-')}`;

  let tagsHtml = '';
  if (isCompleted) {
    tagsHtml += `<span class="badge badge-completed">✓ Completed</span> `;
  }
  if (hlCount > 0) {
    tagsHtml += `<span class="badge badge-highlight-count" title="${hlCount} highlights">🖍 ${hlCount}</span> `;
  }

  (q.tags || []).forEach(tag => {
    const lower = tag.toLowerCase().trim();
    if (lower.startsWith('x')) {
      const freq = parseInt(lower.slice(1)) || 1;
      let cls = freq >= 5 ? 'badge-pyq-high' : (freq >= 2 ? 'badge-pyq-med' : 'badge-pyq-low');
      tagsHtml += `<span class="badge ${cls}">${escapeHtml(tag)}</span> `;
    } else if (lower.includes('musa')) {
      tagsHtml += `<span class="badge badge-musa">${escapeHtml(tag)}</span> `;
    } else if (lower.includes('syllabus')) {
      tagsHtml += `<span class="badge badge-syllabus">Syllabus</span> `;
    } else {
      tagsHtml += `<span class="badge badge-pyq-low">${escapeHtml(tag)}</span> `;
    }
  });

  return `
    <article class="question-card ${isStarred ? 'is-starred' : ''} ${isCompleted ? 'is-completed' : ''}" id="${safeId}" data-qid="${q.id}">
      <div class="question-header-btn" role="button" tabindex="0" onclick="toggleQuestion('${safeId}', event)" onkeydown="handleHeaderKeydown('${safeId}', event)" aria-expanded="false" aria-controls="${answerId}">
        <div class="question-title-area">
          <div class="question-actions-row">
            <!-- Star Button -->
            <button type="button" class="btn-q-action btn-q-star ${isStarred ? 'active' : ''}" onclick="toggleStarQuestion('${q.id}', event)" aria-pressed="${isStarred}" aria-label="${isStarred ? 'Unstar question' : 'Star question'}">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="${isStarred ? 'var(--status-star)' : 'none'}" stroke="currentColor" stroke-width="2" aria-hidden="true">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
              <span class="btn-action-label">${isStarred ? 'Starred' : 'Star'}</span>
            </button>

            <!-- Complete Button -->
            <button type="button" class="btn-q-action btn-q-tick ${isCompleted ? 'active' : ''}" onclick="toggleCompleteQuestion('${q.id}', event)" aria-pressed="${isCompleted}" aria-label="${isCompleted ? 'Mark uncompleted' : 'Mark completed'}">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span class="btn-action-label">${isCompleted ? 'Completed' : 'Mark done'}</span>
            </button>

            <span class="question-num">Question ${q.id}</span>
          </div>

          <div class="question-text">${escapeHtml(q.question)}</div>
        </div>

        <div class="question-meta">
          ${tagsHtml}
          <svg class="accordion-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </div>
      </div>

      <div class="answer-body" id="${answerId}">
        ${wrapTablesInContainer(q.answer_html || '<p class="not-found">Answer coming soon.</p>')}
        
        <div class="answer-footer-controls">
          <button type="button" class="btn-answer-subtle" onclick="clearQuestionHighlights('${q.id}')">
            Clear highlights
          </button>
        </div>
      </div>
    </article>
  `;
}

function wrapTablesInContainer(html) {
  return html.replace(/<table class="comparison-table">([\s\S]*?)<\/table>/gi, (match) => {
    return `<div class="table-wrapper">${match}</div>`;
  });
}

// Accordion Toggle
window.toggleQuestion = function(cardId, event) {
  if (event && event.target) {
    if (event.target.closest('.btn-q-action, .btn-answer-subtle, .code-copy-btn, mark.highlight')) {
      return;
    }
  }
  // Selecting text inside question header must not toggle accordion
  if (window.getSelection && window.getSelection().toString().trim().length > 0) {
    return;
  }
  const card = document.getElementById(cardId);
  if (!card) return;
  const isOpen = card.classList.toggle('open');
  const btn = card.querySelector('.question-header-btn');
  if (btn) btn.setAttribute('aria-expanded', String(isOpen));

  // When opened, ensure KaTeX math and highlights are rendered inside
  if (isOpen) {
    const answerBody = card.querySelector('.answer-body');
    if (answerBody) {
      applyMathInContainer(answerBody);
      const qId = card.getAttribute('data-qid');
      if (qId) applyHighlightsToAnswer(qId, answerBody);
    }
  }
};

window.handleHeaderKeydown = function(cardId, event) {
  if (event.key === 'Enter' || event.key === ' ') {
    if (event.target && event.target.classList.contains('question-header-btn')) {
      event.preventDefault();
      toggleQuestion(cardId, event);
    }
  }
};

function expandAllCurrent() {
  document.querySelectorAll('.question-card').forEach(card => {
    card.classList.add('open');
    const btn = card.querySelector('.question-header-btn');
    if (btn) btn.setAttribute('aria-expanded', 'true');
    const answerBody = card.querySelector('.answer-body');
    if (answerBody) {
      applyMathInContainer(answerBody);
      const qId = card.getAttribute('data-qid');
      if (qId) applyHighlightsToAnswer(qId, answerBody);
    }
  });
}

function collapseAllCurrent() {
  document.querySelectorAll('.question-card').forEach(card => {
    card.classList.remove('open');
    const btn = card.querySelector('.question-header-btn');
    if (btn) btn.setAttribute('aria-expanded', 'false');
  });
}

// Filter Logic
function matchesFilter(q) {
  if (currentFilter === 'all') return true;
  if (currentFilter === 'starred') return starredQuestions.has(q.id);
  if (currentFilter === 'completed') return completedQuestions.has(q.id);
  if (currentFilter === 'uncompleted') return !completedQuestions.has(q.id);

  const tags = (q.tags || []).map(t => t.toLowerCase());
  if (currentFilter === 'high-pyq') {
    return tags.some(t => {
      const m = t.match(/x(\d+)/i);
      return m && parseInt(m[1]) >= 3;
    });
  }
  if (currentFilter === 'musa') return tags.some(t => t.includes('musa'));
  if (currentFilter === 'syllabus') return tags.some(t => t.includes('syllabus'));
  return true;
}

// ==========================================================================
// 1. Persistent Highlighting Engine
// ==========================================================================
function initHighlightListeners() {
  // Listen for mouseup and touchend inside answer bodies
  document.addEventListener('mouseup', handleTextSelection);
  document.addEventListener('touchend', handleTextSelection);

  // Touch selection change support (debounced)
  let selTimeout = null;
  document.addEventListener('selectionchange', () => {
    clearTimeout(selTimeout);
    selTimeout = setTimeout(() => {
      const sel = window.getSelection();
      if (sel && !sel.isCollapsed && sel.rangeCount > 0) {
        handleTextSelection({ target: document.body });
      }
    }, 250);
  });

  // Esc closes toolbar
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && highlightToolbar && highlightToolbar.classList.contains('active')) {
      hideHighlightToolbar();
    }
  });

  // Toolbar color buttons
  document.querySelectorAll('.btn-hl-color').forEach(btn => {
    btn.addEventListener('click', () => {
      const color = btn.getAttribute('data-color');
      if (currentHighlightTarget) {
        // Change color of existing highlight
        updateExistingHighlightColor(currentHighlightTarget, color);
      } else if (currentSelectionRange) {
        // Create new highlight
        createNewHighlight(color);
      }
      hideHighlightToolbar();
    });
  });

  // Remove highlight button
  const removeBtn = document.getElementById('btn-hl-remove');
  if (removeBtn) {
    removeBtn.addEventListener('click', () => {
      if (currentHighlightTarget) {
        removeHighlightRecord(currentHighlightTarget);
      }
      hideHighlightToolbar();
    });
  }

  // Click on existing highlight to show options
  document.addEventListener('click', (e) => {
    const mark = e.target.closest('mark.highlight');
    if (mark) {
      e.stopPropagation();
      currentHighlightTarget = mark;
      currentSelectionRange = null;
      positionToolbarAtRect(mark.getBoundingClientRect());
    } else if (highlightToolbar && !highlightToolbar.contains(e.target)) {
      hideHighlightToolbar();
    }
  });
}

function handleTextSelection(e) {
  // If clicking inside toolbar, ignore
  if (highlightToolbar && highlightToolbar.contains(e.target)) return;

  const sel = window.getSelection();
  if (!sel || sel.isCollapsed || sel.rangeCount === 0) return;

  const range = sel.getRangeAt(0);
  // Ensure selection is inside an answer body
  const answerBody = range.commonAncestorContainer.nodeType === 1 
    ? range.commonAncestorContainer.closest('.answer-body')
    : range.commonAncestorContainer.parentElement.closest('.answer-body');

  if (!answerBody) return;

  // Ensure selection doesn't originate from katex
  if (range.startContainer.parentElement && range.startContainer.parentElement.closest('.katex')) return;

  currentSelectionRange = range.cloneRange();
  currentHighlightTarget = null;
  positionToolbarAtRect(range.getBoundingClientRect());
}

function positionToolbarAtRect(rect) {
  if (!highlightToolbar || !rect || rect.width === 0) return;
  highlightToolbar.classList.add('active');

  const toolbarWidth = highlightToolbar.offsetWidth || 180;
  const toolbarHeight = highlightToolbar.offsetHeight || 36;
  const scrollY = window.scrollY || document.documentElement.scrollTop;
  const scrollX = window.scrollX || document.documentElement.scrollLeft;

  let top = rect.top + scrollY - toolbarHeight - 8;
  if (top < scrollY + 10) {
    top = rect.bottom + scrollY + 8; // flip below if offscreen
  }

  let left = rect.left + scrollX + (rect.width / 2) - (toolbarWidth / 2);
  if (left < 10) left = 10;
  if (left + toolbarWidth > window.innerWidth - 10) left = window.innerWidth - toolbarWidth - 10;

  highlightToolbar.style.top = `${top}px`;
  highlightToolbar.style.left = `${left}px`;
}

function hideHighlightToolbar() {
  if (highlightToolbar) {
    highlightToolbar.classList.remove('active');
  }
  currentHighlightTarget = null;
  currentSelectionRange = null;
}

function createNewHighlight(color) {
  if (!currentSelectionRange) return;
  const range = currentSelectionRange;
  const answerBody = range.commonAncestorContainer.nodeType === 1 
    ? range.commonAncestorContainer.closest('.answer-body')
    : range.commonAncestorContainer.parentElement.closest('.answer-body');
  if (!answerBody) return;

  const card = answerBody.closest('.question-card');
  const qId = card ? card.getAttribute('data-qid') : null;
  if (!qId) return;

  const selectedText = range.toString().trim();
  if (!selectedText) return;

  // Remove and replace any overlapping highlights
  const existingMarks = answerBody.querySelectorAll('mark.highlight');
  existingMarks.forEach(mark => {
    try {
      if (range.intersectsNode(mark)) {
        const oldId = mark.getAttribute('data-highlight-id');
        if (oldId && questionHighlights[qId]) {
          questionHighlights[qId] = questionHighlights[qId].filter(h => h.id !== oldId);
        }
        const parent = mark.parentNode;
        while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
        parent.removeChild(mark);
        parent.normalize();
      }
    } catch (e) {}
  });

  const highlightId = 'hl_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5);

  // Compute prefix and suffix context (~30 chars)
  const fullText = answerBody.textContent || '';
  const rangeStartOffset = getCharacterOffsetWithin(range.startContainer, range.startOffset, answerBody);
  const prefix = fullText.substring(Math.max(0, rangeStartOffset - 30), rangeStartOffset);
  const suffix = fullText.substring(rangeStartOffset + selectedText.length, Math.min(fullText.length, rangeStartOffset + selectedText.length + 30));

  // Wrap text nodes in range
  wrapRangeInHighlight(range, color, highlightId);

  // Save highlight
  if (!questionHighlights[qId]) questionHighlights[qId] = [];
  questionHighlights[qId].push({
    id: highlightId,
    color,
    text: selectedText,
    prefix,
    suffix,
    offsetHint: rangeStartOffset
  });
  saveUserData();

  // Update highlight count badge in question header
  updateCardHighlightBadge(card, qId);
  window.getSelection().removeAllRanges();
}

function wrapRangeInHighlight(range, color, highlightId) {
  const commonAncestor = range.commonAncestorContainer;
  const startContainer = range.startContainer;
  const startOffset = range.startOffset;
  const endContainer = range.endContainer;
  const endOffset = range.endOffset;

  // Single text node case
  if (startContainer === endContainer && startContainer.nodeType === Node.TEXT_NODE) {
    // Ignore inside katex
    if (startContainer.parentElement && startContainer.parentElement.closest('.katex')) return;

    let targetNode = startContainer;
    if (endOffset < targetNode.length) {
      targetNode.splitText(endOffset);
    }
    if (startOffset > 0) {
      targetNode = targetNode.splitText(startOffset);
    }
    const mark = document.createElement('mark');
    mark.className = `highlight highlight-${color}`;
    mark.setAttribute('data-highlight-id', highlightId);
    targetNode.parentNode.replaceChild(mark, targetNode);
    mark.appendChild(targetNode);
    return;
  }

  // Cross-node case: walk text nodes
  const root = commonAncestor.nodeType === Node.TEXT_NODE ? commonAncestor.parentNode : commonAncestor;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (node.parentElement && node.parentElement.closest('.katex')) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }
  });

  const nodesToWrap = [];
  let started = false;

  let currentNode = walker.nextNode();
  while (currentNode) {
    if (currentNode === startContainer) {
      started = true;
      nodesToWrap.push({ node: currentNode, isStart: true });
    } else if (currentNode === endContainer) {
      nodesToWrap.push({ node: currentNode, isEnd: true });
      break;
    } else if (started) {
      nodesToWrap.push({ node: currentNode });
    }
    currentNode = walker.nextNode();
  }

  nodesToWrap.forEach(item => {
    let node = item.node;
    if (item.isStart) {
      if (startOffset > 0 && startOffset < node.length) {
        node = node.splitText(startOffset);
      }
    }
    if (item.isEnd) {
      if (endOffset > 0 && endOffset < node.length) {
        node.splitText(endOffset);
      }
    }
    const mark = document.createElement('mark');
    mark.className = `highlight highlight-${color}`;
    mark.setAttribute('data-highlight-id', highlightId);
    node.parentNode.replaceChild(mark, node);
    mark.appendChild(node);
  });
}

function updateExistingHighlightColor(mark, color) {
  const id = mark.getAttribute('data-highlight-id');
  const card = mark.closest('.question-card');
  const qId = card ? card.getAttribute('data-qid') : null;

  mark.className = `highlight highlight-${color}`;

  if (qId && questionHighlights[qId]) {
    const hl = questionHighlights[qId].find(h => h.id === id);
    if (hl) {
      hl.color = color;
      saveUserData();
    }
  }
}

function removeHighlightRecord(mark) {
  const id = mark.getAttribute('data-highlight-id');
  const card = mark.closest('.question-card');
  const qId = card ? card.getAttribute('data-qid') : null;

  // Unwrap mark element
  const parent = mark.parentNode;
  while (mark.firstChild) {
    parent.insertBefore(mark.firstChild, mark);
  }
  parent.removeChild(mark);
  parent.normalize();

  if (qId && questionHighlights[qId]) {
    questionHighlights[qId] = questionHighlights[qId].filter(h => h.id !== id);
    saveUserData();
    if (card) updateCardHighlightBadge(card, qId);
  }
}

window.clearQuestionHighlights = function(qId) {
  if (!confirm(`Clear all highlights for Question ${qId}?`)) return;

  delete questionHighlights[qId];
  saveUserData();

  const card = document.getElementById('q-' + qId.replace(/\./g, '-'));
  if (card) {
    const marks = card.querySelectorAll('mark.highlight');
    marks.forEach(mark => {
      const parent = mark.parentNode;
      while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
      parent.removeChild(mark);
      parent.normalize();
    });
    updateCardHighlightBadge(card, qId);
  }
};

function updateCardHighlightBadge(card, qId) {
  const count = (questionHighlights[qId] || []).length;
  const meta = card.querySelector('.question-meta');
  if (!meta) return;

  let badge = meta.querySelector('.badge-highlight-count');
  if (count > 0) {
    if (!badge) {
      badge = document.createElement('span');
      badge.className = 'badge badge-highlight-count';
      meta.prepend(badge);
    }
    badge.textContent = `🖍 ${count}`;
    badge.title = `${count} highlights`;
  } else if (badge) {
    badge.remove();
  }
}

function applyHighlightsToContainer(container) {
  container.querySelectorAll('.question-card').forEach(card => {
    const qId = card.getAttribute('data-qid');
    const answerBody = card.querySelector('.answer-body');
    if (qId && answerBody) {
      applyHighlightsToAnswer(qId, answerBody);
    }
  });
}

function applyHighlightsToAnswer(qId, answerBody) {
  const list = questionHighlights[qId];
  if (!list || list.length === 0) return;

  // Don't re-apply if already applied
  if (answerBody.querySelector('mark.highlight')) return;

  // Apply in reverse offset order (bottom-to-top) so earlier offsets are never affected
  const sortedList = [...list].sort((a, b) => (b.offsetHint || 0) - (a.offsetHint || 0));

  sortedList.forEach(hl => {
    if (!hl.text) return;

    const walker = document.createTreeWalker(answerBody, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (node.parentElement && node.parentElement.closest('.katex')) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });

    // Build character map of text nodes
    const textNodes = [];
    let fullText = '';
    let currentNode = walker.nextNode();
    while (currentNode) {
      textNodes.push({ node: currentNode, start: fullText.length, end: fullText.length + currentNode.length });
      fullText += currentNode.nodeValue;
      currentNode = walker.nextNode();
    }

    // Find matching position using context and offset hint
    let matchIdx = -1;
    if (hl.prefix && fullText.includes(hl.prefix + hl.text)) {
      matchIdx = findBestMatchIndex(fullText, hl.prefix + hl.text, (hl.offsetHint || 0) - hl.prefix.length);
      if (matchIdx !== -1) matchIdx += hl.prefix.length;
    } else if (fullText.includes(hl.text)) {
      matchIdx = findBestMatchIndex(fullText, hl.text, hl.offsetHint);
    }

    if (matchIdx === -1) return; // skip silently if quote cannot be located

    const matchEnd = matchIdx + hl.text.length;

    // Find starting and ending text nodes
    const startNodeItem = textNodes.find(item => matchIdx >= item.start && matchIdx < item.end);
    const endNodeItem = textNodes.find(item => matchEnd > item.start && matchEnd <= item.end);

    if (startNodeItem && endNodeItem) {
      const range = document.createRange();
      range.setStart(startNodeItem.node, matchIdx - startNodeItem.start);
      range.setEnd(endNodeItem.node, matchEnd - endNodeItem.start);
      wrapRangeInHighlight(range, hl.color, hl.id);
    }
  });
}

function findBestMatchIndex(fullText, query, offsetHint) {
  if (!query || !fullText) return -1;
  let bestIdx = -1;
  let minDiff = Infinity;
  let pos = fullText.indexOf(query);
  while (pos !== -1) {
    const diff = offsetHint !== undefined ? Math.abs(pos - offsetHint) : pos;
    if (diff < minDiff) {
      minDiff = diff;
      bestIdx = pos;
    }
    pos = fullText.indexOf(query, pos + 1);
  }
  return bestIdx;
}

function getCharacterOffsetWithin(targetNode, offsetInNode, container) {
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
  let total = 0;
  let currentNode = walker.nextNode();
  while (currentNode) {
    if (currentNode === targetNode) {
      return total + offsetInNode;
    }
    total += currentNode.length;
    currentNode = walker.nextNode();
  }
  return total;
}

// ==========================================================================
// 2. Offline KaTeX Math Rendering with Fallback
// ==========================================================================
function applyMathInContainer(container) {
  if (!container) return;

  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(container, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ],
        throwOnError: false,
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
      });
      return;
    } catch (e) {
      console.warn("KaTeX error, using fallback math parser:", e);
    }
  }

  // Graceful Offline Fallback Parser
  renderMathFallback(container);
}

function renderMathFallback(container) {
  const answerBodies = container.querySelectorAll('.answer-body, .formula-block, .definition-box');
  answerBodies.forEach(body => {
    body.innerHTML = parseMathText(body.innerHTML);
  });
}

function parseMathText(html) {
  if (!html) return '';

  html = html.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
    return `<div class="math-display">${cleanLatexFormula(formula)}</div>`;
  });

  html = html.replace(/\$([^\$\n\r<]+?)\$/g, (match, formula) => {
    if (/^0x[0-9a-fA-F_]+$/.test(formula.trim())) {
      return `<code>${formula.trim()}</code>`;
    }
    return `<span class="math-inline">${cleanLatexFormula(formula)}</span>`;
  });

  return html;
}

function cleanLatexFormula(tex) {
  let s = tex.trim();

  // Greek letters
  s = s.replace(/\\alpha\b/g, '&alpha;');
  s = s.replace(/\\beta\b/g, '&beta;');
  s = s.replace(/\\gamma\b/g, '&gamma;');
  s = s.replace(/\\delta\b/g, '&delta;');
  s = s.replace(/\\Delta\b/g, '&Delta;');
  s = s.replace(/\\epsilon\b/g, '&epsilon;');
  s = s.replace(/\\theta\b/g, '&theta;');
  s = s.replace(/\\lambda\b/g, '&lambda;');
  s = s.replace(/\\mu\b/g, '&mu;');
  s = s.replace(/\\pi\b/g, '&pi;');
  s = s.replace(/\\tau\b/g, '&tau;');
  s = s.replace(/\\omega\b/g, '&omega;');
  s = s.replace(/\\Omega\b/g, '&Omega;');

  // Math operators
  s = s.replace(/\\cdot\b/g, '&sdot;');
  s = s.replace(/\\times\b/g, '&times;');
  s = s.replace(/\\approx\b/g, '&asymp;');
  s = s.replace(/\\pm\b/g, '&plusmn;');
  s = s.replace(/\\le\b|\\leq\b/g, '&le;');
  s = s.replace(/\\ge\b|\\geq\b/g, '&ge;');
  s = s.replace(/\\neq\b/g, '&ne;');
  s = s.replace(/\\infty\b/g, '&infin;');
  s = s.replace(/\\sum\b/g, '&sum;');
  s = s.replace(/\\dots\b/g, '&hellip;');
  s = s.replace(/\\circ\b/g, '&deg;');

  // Brackets
  s = s.replace(/\\left\\lfloor\s*([\s\S]*?)\s*\\right\\rfloor/g, '&lfloor;$1&rfloor;');
  s = s.replace(/\\left\\lceil\s*([\s\S]*?)\s*\\right\\rceil/g, '&lceil;$1&rceil;');
  s = s.replace(/\\left\(\s*([\s\S]*?)\s*\\right\)/g, '($1)');
  s = s.replace(/\\left\[\s*([\s\S]*?)\s*\\right\]/g, '[$1]');
  s = s.replace(/\\left|\/right/g, '');

  // Text and bold
  s = s.replace(/\\mathbf\{([^{}]+)\}/g, '<strong>$1</strong>');
  s = s.replace(/\\text\{([^{}]+)\}/g, '<span class="math-text">$1</span>');

  // Superscripts and subscripts
  s = s.replace(/\^\{([^{}]+)\}/g, '<sup>$1</sup>');
  s = s.replace(/\^([0-9a-zA-Z\+\-]+)/g, '<sup>$1</sup>');
  s = s.replace(/_\{([^{}]+)\}/g, '<sub>$1</sub>');
  s = s.replace(/_([0-9a-zA-Z\+\-]+)/g, '<sub>$1</sub>');

  // Fractions: balanced parser
  while (s.includes('\\frac{')) {
    const startIdx = s.indexOf('\\frac{');
    let i = startIdx + 6;
    let depth = 1;
    let numStart = i;
    while (i < s.length && depth > 0) {
      if (s[i] === '{') depth++;
      else if (s[i] === '}') depth--;
      i++;
    }
    if (depth !== 0) break;
    const num = s.substring(numStart, i - 1);
    if (s[i] !== '{') break;
    i++;
    let denStart = i;
    depth = 1;
    while (i < s.length && depth > 0) {
      if (s[i] === '{') depth++;
      else if (s[i] === '}') depth--;
      i++;
    }
    if (depth !== 0) break;
    const den = s.substring(denStart, i - 1);
    const replacement = `<span class="math-frac"><span class="numerator">${cleanLatexFormula(num)}</span><span class="denominator">${cleanLatexFormula(den)}</span></span>`;
    s = s.substring(0, startIdx) + replacement + s.substring(i);
  }

  s = s.replace(/\\sqrt\{([^{}]+)\}/g, '&radic;($1)');
  s = s.replace(/\\quad\b/g, '&emsp;');
  s = s.replace(/\\,|\\ /g, '&thinsp;');

  // Standalone single letters as italic variables
  s = s.replace(/(^|[^a-zA-Z0-9_>])([a-zA-Z])(?=[^a-zA-Z0-9_<]|$)/g, '$1<i>$2</i>');
  s = s.replace(/\\/g, '');

  return s;
}

// ==========================================================================
// 6. Search Engine with Hotkeys & Keyboard Navigation
// ==========================================================================
function handleSearch(e) {
  const query = e.target.value.trim().toLowerCase();
  searchQuery = query;
  selectedSearchIndex = -1;

  if (query.length < 2) {
    if (searchDropdown) searchDropdown.classList.remove('active');
    searchResultsList = [];
    return;
  }

  const results = [];
  studyData.forEach(mod => {
    (mod.topics || []).forEach(t => {
      (t.questions || []).forEach(q => {
        const inQuestion = q.question.toLowerCase().includes(query);
        const inTags = (q.tags || []).some(tag => tag.toLowerCase().includes(query));
        const inAnswer = (q.answer_html || '').toLowerCase().includes(query);

        if (inQuestion || inTags || inAnswer) {
          results.push({
            modId: mod.module,
            modTitle: mod.title,
            qId: q.id,
            question: q.question,
            matchType: inQuestion ? 'Question match' : (inTags ? 'Tag match' : 'Answer content match')
          });
        }
      });
    });
  });

  searchResultsList = results;
  renderSearchResults(results, query);
}

function renderSearchResults(results, query) {
  if (!searchDropdown) return;

  if (results.length === 0) {
    searchDropdown.innerHTML = `
      <div style="padding: 14px; text-align:center; color:var(--text-muted); font-size:12.5px;">
        No questions matched "${escapeHtml(query)}"
      </div>
    `;
    searchDropdown.classList.add('active');
    return;
  }

  let html = '';
  results.slice(0, 12).forEach((res, index) => {
    // Highlight matched query in question text
    const highlightedQ = highlightMatch(res.question, query);
    html += `
      <div class="search-result-item" role="option" data-index="${index}" onclick="navigateToQuestion(${res.modId}, '${res.qId}')">
        <div class="search-result-mod">Module ${res.modId} &bull; ${escapeHtml(res.matchType)}</div>
        <div class="search-result-q"><strong>Q${res.qId}:</strong> ${highlightedQ}</div>
      </div>
    `;
  });

  searchDropdown.innerHTML = html;
  searchDropdown.classList.add('active');
}

function highlightMatch(text, query) {
  if (!query) return escapeHtml(text);
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  return escapeHtml(text).replace(regex, '<mark class="search-match">$1</mark>');
}

window.navigateToQuestion = function(modId, qId) {
  if (searchDropdown) searchDropdown.classList.remove('active');
  if (searchInput) searchInput.blur();

  // Reset filter to 'all' so searched card is always visible
  const filterChanged = currentFilter !== 'all';
  if (filterChanged) {
    currentFilter = 'all';
    filterChips.forEach(c => {
      const isAll = c.dataset.filter === 'all';
      c.classList.toggle('active', isAll);
      c.setAttribute('aria-pressed', String(isAll));
    });
  }

  if (currentModuleId !== modId) {
    switchModule(modId);
  } else if (filterChanged) {
    renderCurrentModule();
  }

  setTimeout(() => {
    const cardId = 'q-' + qId.replace(/\./g, '-');
    const card = document.getElementById(cardId);
    if (card) {
      if (!card.classList.contains('open')) {
        toggleQuestion(cardId);
      }
      // Scroll into view below sticky header
      const topOffset = card.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });

      // Flash highlight
      card.classList.add('flash-highlight');
      setTimeout(() => card.classList.remove('flash-highlight'), 1200);
    }
  }, 120);
};

// ==========================================================================
// Export / Import (Backup & Restore)
// ==========================================================================
function setupBackupHandlers() {
  if (btnExportImport) {
    btnExportImport.addEventListener('click', () => {
      if (backupModal) backupModal.classList.add('active');
    });
  }

  if (btnCloseModal) {
    btnCloseModal.addEventListener('click', () => {
      if (backupModal) backupModal.classList.remove('active');
    });
  }

  if (btnDoExport) {
    btnDoExport.addEventListener('click', () => {
      const exportData = {
        version: 1,
        exportedAt: new Date().toISOString(),
        starredQuestions: Array.from(starredQuestions),
        completedQuestions: Array.from(completedQuestions),
        starredModules: Array.from(starredModules),
        highlights: questionHighlights
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `embedded-systems-study-backup-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  if (importFileInput) {
    importFileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const imported = JSON.parse(event.target.result);
          if (Array.isArray(imported.starredQuestions)) {
            starredQuestions = new Set(imported.starredQuestions);
          }
          if (Array.isArray(imported.completedQuestions)) {
            completedQuestions = new Set(imported.completedQuestions);
          }
          if (Array.isArray(imported.starredModules)) {
            starredModules = new Set(imported.starredModules);
          }
          if (imported.highlights && typeof imported.highlights === 'object') {
            questionHighlights = imported.highlights;
          }
          saveUserData();
          computeGlobalStats();
          renderSidebar();
          renderCurrentModule();
          if (backupModal) backupModal.classList.remove('active');
          alert('Study progress and highlights imported successfully!');
        } catch (err) {
          alert('Invalid backup file. Please select a valid JSON backup.');
        }
      };
      reader.readAsText(file);
    });
  }
}

// ==========================================================================
// Code Copy Button
// ==========================================================================
function setupCodeCopyButtons() {
  document.querySelectorAll('pre').forEach(pre => {
    if (pre.querySelector('.code-copy-btn')) return;

    pre.style.position = 'relative';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'code-copy-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code snippet');
    btn.style.cssText = `
      position: absolute;
      top: 6px;
      right: 6px;
      padding: 2px 7px;
      font-size: 11px;
      font-family: var(--font-mono);
      color: var(--text-code);
      background: rgba(255,255,255,0.12);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 3px;
      cursor: pointer;
    `;

    btn.addEventListener('click', () => {
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      navigator.clipboard.writeText(code).then(() => {
        btn.textContent = 'Copied!';
        btn.style.color = '#34D399';
        setTimeout(() => {
          btn.textContent = 'Copy';
          btn.style.color = 'var(--text-code)';
        }, 1800);
      });
    });

    pre.appendChild(btn);
  });
}

// ==========================================================================
// Global Event Listeners (Hotkeys, Drawer, Controls)
// ==========================================================================
function setupEventListeners() {
  initHighlightListeners();
  setupBackupHandlers();

  // Theme toggle
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', toggleTheme);
  }

  // Expand / Collapse all
  if (expandAllBtn) expandAllBtn.addEventListener('click', expandAllCurrent);
  if (collapseAllBtn) collapseAllBtn.addEventListener('click', collapseAllCurrent);

  // Filter chips
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => {
        c.classList.remove('active');
        c.setAttribute('aria-pressed', 'false');
      });
      chip.classList.add('active');
      chip.setAttribute('aria-pressed', 'true');
      currentFilter = chip.dataset.filter;
      renderCurrentModule();
    });
  });

  // Search input listeners & keyboard navigation
  if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
    searchInput.addEventListener('focus', () => {
      if (searchInput.value.trim().length >= 2 && searchDropdown) {
        searchDropdown.classList.add('active');
      }
    });

    searchInput.addEventListener('keydown', (e) => {
      if (!searchDropdown || !searchDropdown.classList.contains('active')) return;
      const items = searchDropdown.querySelectorAll('.search-result-item');
      if (items.length === 0) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedSearchIndex = (selectedSearchIndex + 1) % items.length;
        updateSelectedSearchItem(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedSearchIndex = (selectedSearchIndex - 1 + items.length) % items.length;
        updateSelectedSearchItem(items);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedSearchIndex >= 0 && selectedSearchIndex < items.length) {
          items[selectedSearchIndex].click();
        } else if (items.length > 0) {
          items[0].click();
        }
      }
    });

    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.classList.remove('active');
      }
    });
  }

  function updateSelectedSearchItem(items) {
    items.forEach((item, idx) => {
      item.classList.toggle('selected', idx === selectedSearchIndex);
      if (idx === selectedSearchIndex) {
        item.scrollIntoView({ block: 'nearest' });
      }
    });
  }

  // Global Keyboard Shortcuts ('/', Ctrl+K, Esc)
  document.addEventListener('keydown', (e) => {
    const isTyping = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) || document.activeElement.isContentEditable;

    if (!isTyping) {
      if (e.key === '/' || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) {
        e.preventDefault();
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      }
    }

    if (e.key === 'Escape') {
      if (searchDropdown && searchDropdown.classList.contains('active')) {
        searchDropdown.classList.remove('active');
      }
      if (searchInput && document.activeElement === searchInput) {
        searchInput.value = '';
        searchInput.blur();
      }
      if (sidebar && sidebar.classList.contains('open')) {
        closeMobileSidebar();
      }
    }
  });

  // Mobile Drawer Toggle with focus management
  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = sidebar.classList.toggle('open');
      sidebarOverlay.classList.toggle('open');
      mobileMenuBtn.setAttribute('aria-expanded', String(isOpen));
      if (isOpen) {
        const firstLink = sidebar.querySelector('.nav-item');
        if (firstLink) firstLink.focus();
      }
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeMobileSidebar);
  }

  // Back to Top Button
  window.addEventListener('scroll', () => {
    if (window.scrollY > 280) {
      backToTopBtn.classList.add('visible');
    } else {
      backToTopBtn.classList.remove('visible');
    }
  });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}

function closeMobileSidebar() {
  if (sidebar) sidebar.classList.remove('open');
  if (sidebarOverlay) sidebarOverlay.classList.remove('open');
  if (mobileMenuBtn) {
    mobileMenuBtn.setAttribute('aria-expanded', 'false');
    mobileMenuBtn.focus();
  }
}

function escapeHtml(text) {
  if (!text) return '';
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.toString().replace(/[&<>"']/g, m => map[m]);
}
