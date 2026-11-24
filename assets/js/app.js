/**
 * Embedded Systems & RTOS Study Guide - Interactive Dashboard App
 * Features:
 * - Direct-open zero-CORS file:// support
 * - LaTeX math rendering with KaTeX and built-in offline mathematical typography fallback
 * - Star (Bookmark) and Tick (Completed / Studied) options for all questions & modules
 * - LocalStorage persistence
 * - Real-time full-text search & quick filters
 * - Accordion controls, code copying, and mobile drawer
 */

// Global State
let studyData = [];
let currentModuleId = 1;
let currentFilter = 'all'; // 'all', 'starred', 'completed', 'uncompleted', 'high-pyq', 'musa', 'syllabus'
let searchQuery = '';

// User Progress & Bookmarks (with LocalStorage persistence)
let starredQuestions = new Set();
let completedQuestions = new Set();
let starredModules = new Set();

// DOM Elements
const sidebarNav = document.getElementById('sidebar-nav');
const contentContainer = document.getElementById('content-container');
const searchInput = document.getElementById('search-input');
const searchCount = document.getElementById('search-count');
const searchDropdown = document.getElementById('search-dropdown');
const filterChips = document.querySelectorAll('.filter-chip');
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');
const backToTopBtn = document.getElementById('back-to-top');
const expandAllBtn = document.getElementById('btn-expand-all');
const collapseAllBtn = document.getElementById('btn-collapse-all');

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  loadSavedUserData();
  setupEventListeners();
  await loadAllModuleData();
  renderSidebar();
  renderCurrentModule();
  setupCodeCopyButtons();
  updateGlobalStats();
});

// Load user bookmarks & completion state from localStorage
function loadSavedUserData() {
  try {
    const savedStars = localStorage.getItem('es_starred_questions');
    if (savedStars) starredQuestions = new Set(JSON.parse(savedStars));

    const savedCompleted = localStorage.getItem('es_completed_questions');
    if (savedCompleted) completedQuestions = new Set(JSON.parse(savedCompleted));

    const savedModStars = localStorage.getItem('es_starred_modules');
    if (savedModStars) starredModules = new Set(JSON.parse(savedModStars));
  } catch (e) {
    console.warn('LocalStorage not available, falling back to session memory.', e);
  }
}

function saveUserData() {
  try {
    localStorage.setItem('es_starred_questions', JSON.stringify(Array.from(starredQuestions)));
    localStorage.setItem('es_completed_questions', JSON.stringify(Array.from(completedQuestions)));
    localStorage.setItem('es_starred_modules', JSON.stringify(Array.from(starredModules)));
  } catch (e) {
    // Session fallback
  }
}

// Load data for all modules
async function loadAllModuleData() {
  const modulesToLoad = [1, 2, 3, 4, 5, 6];
  studyData = [];

  for (const modNum of modulesToLoad) {
    try {
      if (window.embeddedStudyData && window.embeddedStudyData[modNum]) {
        studyData.push(window.embeddedStudyData[modNum]);
        continue;
      }
      
      const response = await fetch(`data/mod${modNum}_answers.json`);
      if (response.ok) {
        const json = await response.json();
        studyData.push(json);
      }
    } catch (e) {
      if (window.embeddedStudyData && window.embeddedStudyData[modNum]) {
        studyData.push(window.embeddedStudyData[modNum]);
      }
    }
  }

  studyData.sort((a, b) => a.module - b.module);
}

// Update sidebar stats & overall progress bar
function updateGlobalStats() {
  let totalQuestions = 0;
  let completedCount = 0;
  let starredCount = 0;
  let pyqHighCount = 0;

  studyData.forEach(mod => {
    (mod.topics || []).forEach(t => {
      (t.questions || []).forEach(q => {
        totalQuestions++;
        if (completedQuestions.has(q.id)) completedCount++;
        if (starredQuestions.has(q.id)) starredCount++;

        const isHigh = (q.tags || []).some(tag => {
          const m = tag.match(/x(\d+)/i);
          return m && parseInt(m[1]) >= 3;
        });
        if (isHigh) pyqHighCount++;
      });
    });
  });

  // Sidebar header stats
  const totalElem = document.getElementById('total-questions-count');
  if (totalElem) totalElem.textContent = `${totalQuestions} Questions`;
  
  const highElem = document.getElementById('high-freq-count');
  if (highElem) highElem.textContent = `${pyqHighCount} High-Yield`;

  // Syllabus progress widget
  const pct = totalQuestions > 0 ? Math.round((completedCount / totalQuestions) * 100) : 0;
  const pctElem = document.getElementById('syllabus-progress-pct');
  if (pctElem) pctElem.textContent = `${pct}%`;

  const compElem = document.getElementById('syllabus-completed-count');
  if (compElem) compElem.textContent = completedCount;

  const starElem = document.getElementById('syllabus-starred-count');
  if (starElem) starElem.textContent = starredCount;

  const barElem = document.getElementById('syllabus-progress-bar');
  if (barElem) barElem.style.width = `${pct}%`;

  // Filter chips count
  const filterStarCount = document.getElementById('filter-starred-count');
  if (filterStarCount) filterStarCount.textContent = starredCount;

  const filterCompCount = document.getElementById('filter-completed-count');
  if (filterCompCount) filterCompCount.textContent = completedCount;
}

// Render Left Sidebar Navigation
function renderSidebar() {
  if (!sidebarNav) return;
  sidebarNav.innerHTML = '';

  const navSection = document.createElement('div');
  navSection.className = 'nav-section-title';
  navSection.textContent = 'Curriculum Modules';
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

    const isAllCompleted = qCount > 0 && completedInMod === qCount;

    const a = document.createElement('a');
    a.className = `nav-item ${mod.module === currentModuleId ? 'active' : ''}`;
    a.dataset.modId = mod.module;
    a.href = `#module-${mod.module}`;

    a.innerHTML = `
      <div class="nav-item-title-wrapper">
        ${hasStarInMod ? `<span class="nav-star-indicator" title="Contains starred questions">&#11088;</span>` : ''}
        <span>Mod ${mod.module}: ${escapeHtml(mod.title.split('&')[0].trim())}</span>
      </div>
      <div class="nav-item-meta">
        ${isAllCompleted ? `<span class="nav-completed-badge" title="All completed">&#10003; Done</span>` : `<span class="nav-badge">${completedInMod}/${qCount}</span>`}
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

// Switch active module
function switchModule(modId) {
  currentModuleId = parseInt(modId);

  document.querySelectorAll('.nav-item').forEach(el => {
    if (parseInt(el.dataset.modId) === currentModuleId) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  });

  renderCurrentModule();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Render the active module's content
function renderCurrentModule() {
  if (!contentContainer) return;
  const mod = studyData.find(m => m.module === currentModuleId);
  if (!mod) {
    contentContainer.innerHTML = `
      <div style="text-align:center; padding: 60px 20px;">
        <h2>Loading module data...</h2>
        <p style="color:var(--text-muted); margin-top:8px;">Compiling verified answers from teacher PDFs.</p>
      </div>
    `;
    return;
  }

  // Calculate module statistics
  let totalModQuestions = 0;
  let completedModQuestions = 0;
  let starredModQuestions = 0;
  let musaCount = 0;

  (mod.topics || []).forEach(t => {
    (t.questions || []).forEach(q => {
      totalModQuestions++;
      if (completedQuestions.has(q.id)) completedModQuestions++;
      if (starredQuestions.has(q.id)) starredModQuestions++;
      (q.tags || []).forEach(tag => {
        if (tag.toLowerCase().includes('musa')) musaCount++;
      });
    });
  });

  const modProgressPct = totalModQuestions > 0 ? Math.round((completedModQuestions / totalModQuestions) * 100) : 0;
  const isModStarred = starredModules.has(mod.module);
  const isModAllCompleted = totalModQuestions > 0 && completedModQuestions === totalModQuestions;

  let html = `
    <div class="module-section active" id="module-${mod.module}">
      <!-- Module Hero Header -->
      <div class="module-hero">
        <div class="module-hero-top">
          <div>
            <div class="module-number">Module ${mod.module} &bull; University Exam Guide</div>
            <h1 class="module-title">${escapeHtml(mod.title)}</h1>
          </div>
          
          <!-- Module Level Quick Actions -->
          <div class="module-actions">
            <button class="btn-module-action ${isModStarred ? 'starred' : ''}" onclick="toggleStarModule(${mod.module}, event)" title="Star entire module">
              <span>${isModStarred ? '&#11088; Starred' : '&#9734; Star Module'}</span>
            </button>
            <button class="btn-module-action ${isModAllCompleted ? 'completed' : ''}" onclick="toggleCompleteAllModule(${mod.module}, event)" title="${isModAllCompleted ? 'Mark all uncompleted' : 'Mark all completed'}">
              <span>${isModAllCompleted ? '&#10003; All Completed' : '&#9744; Mark All Done'}</span>
            </button>
          </div>
        </div>

        <!-- Module Progress Bar -->
        <div class="module-progress-wrapper">
          <div class="progress-info">
            <span>Module Completion Progress</span>
            <span><strong>${completedModQuestions}</strong> of ${totalModQuestions} completed (${modProgressPct}%)</span>
          </div>
          <div class="progress-track">
            <div class="progress-bar-fill" style="width: ${modProgressPct}%;"></div>
          </div>
        </div>
      </div>
  `;

  // Render Topics and Questions
  let totalRenderedInMod = 0;

  (mod.topics || []).forEach(topic => {
    const filteredQuestions = (topic.questions || []).filter(q => matchesFilter(q));
    if (filteredQuestions.length === 0 && currentFilter !== 'all') {
      return;
    }

    totalRenderedInMod += filteredQuestions.length;

    html += `
      <div class="topic-group" id="topic-${topic.id.replace('.', '-')}">
        <div class="topic-header">
          <h2 class="topic-title">
            <span class="topic-id-badge">${topic.id}</span>
            <span>${escapeHtml(topic.title)}</span>
          </h2>
          <span style="font-size:12px; color:var(--text-muted);">${filteredQuestions.length} questions</span>
        </div>
        <div class="question-list">
    `;

    filteredQuestions.forEach(q => {
      html += renderQuestionCard(q, topic.id);
    });

    html += `
        </div>
      </div>
    `;
  });

  if (totalRenderedInMod === 0) {
    html += `
      <div style="text-align:center; padding: 48px 20px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:var(--radius-lg); margin: 20px 0;">
        <h3 style="font-size:16px; color:var(--text-main); margin-bottom:6px;">No questions match filter: "${escapeHtml(currentFilter)}"</h3>
        <p style="font-size:13px; color:var(--text-muted);">Try selecting "All Questions" from the filter bar above.</p>
      </div>
    `;
  }

  // Module Navigation Footer (Prev / Next)
  const prevMod = studyData.find(m => m.module === currentModuleId - 1);
  const nextMod = studyData.find(m => m.module === currentModuleId + 1);

  html += `
    <div class="module-nav-footer">
      ${prevMod ? `
        <button class="nav-page-btn" onclick="switchModule(${prevMod.module})">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
          Previous: Mod ${prevMod.module}
        </button>
      ` : `<div></div>`}
      ${nextMod ? `
        <button class="nav-page-btn" onclick="switchModule(${nextMod.module})">
          Next: Mod ${nextMod.module}
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      ` : `<div></div>`}
    </div>
  </div>`;

  contentContainer.innerHTML = html;
  
  // Format math and setup interactions
  applyMathFormatting(contentContainer);
  setupAccordionClicks();
  setupCodeCopyButtons();
}

// Render individual question card
function renderQuestionCard(q, topicId) {
  const isStarred = starredQuestions.has(q.id);
  const isCompleted = completedQuestions.has(q.id);
  const tagsHtml = renderTags(q.tags || [], isCompleted);
  const safeId = `q-${q.id.replace(/\./g, '-')}`;

  return `
    <div class="question-card ${isStarred ? 'is-starred' : ''} ${isCompleted ? 'is-completed' : ''}" id="${safeId}" data-qid="${q.id}">
      <div class="question-header" onclick="toggleQuestion('${safeId}')">
        <div class="question-title-area">
          <div class="question-actions-row">
            <!-- Star Button -->
            <button class="btn-q-action btn-q-star ${isStarred ? 'active' : ''}" onclick="toggleStarQuestion('${q.id}', event)" title="Star/Bookmark this question for quick revision">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="${isStarred ? '#F59E0B' : 'none'}" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
              <span>${isStarred ? 'Starred' : 'Star'}</span>
            </button>

            <!-- Tick / Completed Button -->
            <button class="btn-q-action btn-q-tick ${isCompleted ? 'active' : ''}" onclick="toggleCompleteQuestion('${q.id}', event)" title="Mark as studied/completed">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>${isCompleted ? 'Completed' : 'Mark Done'}</span>
            </button>

            <span class="question-num">Question ${q.id}</span>
          </div>

          <div class="question-text">${escapeHtml(q.question)}</div>
        </div>
        
        <div class="question-meta">
          ${tagsHtml}
          <svg class="accordion-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </div>
      </div>
      <div class="answer-body">
        ${wrapTablesInContainer(q.answer_html || '<p class="not-found">Answer coming soon.</p>')}
      </div>
    </div>
  `;
}

// User Action Handlers (Star & Tick)
window.toggleStarQuestion = function(qId, event) {
  if (event) event.stopPropagation();

  if (starredQuestions.has(qId)) {
    starredQuestions.delete(qId);
  } else {
    starredQuestions.add(qId);
  }

  saveUserData();
  updateGlobalStats();
  renderSidebar();
  renderCurrentModule();
};

window.toggleCompleteQuestion = function(qId, event) {
  if (event) event.stopPropagation();

  if (completedQuestions.has(qId)) {
    completedQuestions.delete(qId);
  } else {
    completedQuestions.add(qId);
  }

  saveUserData();
  updateGlobalStats();
  renderSidebar();
  renderCurrentModule();
};

window.toggleStarModule = function(modId, event) {
  if (event) event.stopPropagation();
  modId = parseInt(modId);

  if (starredModules.has(modId)) {
    starredModules.delete(modId);
  } else {
    starredModules.add(modId);
  }

  saveUserData();
  renderSidebar();
  renderCurrentModule();
};

window.toggleCompleteAllModule = function(modId, event) {
  if (event) event.stopPropagation();
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
  });

  saveUserData();
  updateGlobalStats();
  renderSidebar();
  renderCurrentModule();
};

// ============================================================================
// MATHEMATICAL TYPESETTING ENGINE (KaTeX with Full Offline Fallback)
// ============================================================================

function applyMathFormatting(container) {
  if (!container) return;

  // 1. If KaTeX is available in window, use KaTeX's official auto-render
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
      console.warn("KaTeX render failed, using fallback:", e);
    }
  }

  // 2. Offline Fallback: Parse and format LaTeX math into clean HTML
  formatMathFallback(container);
}

function formatMathFallback(container) {
  const answerBodies = container.querySelectorAll('.answer-body, .formula-block, .definition-box');
  answerBodies.forEach(body => {
    body.innerHTML = parseMathText(body.innerHTML);
  });
}

function parseMathText(html) {
  if (!html) return '';

  // Process Display Math ($$ ... $$)
  html = html.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
    return `<div class="math-display">${cleanLatexFormula(formula)}</div>`;
  });

  // Process Inline Math ($ ... $) - Avoid currency like &#36;100
  html = html.replace(/\$([^\$\n\r<]+?)\$/g, (match, formula) => {
    // If it looks like a hex address, render as code
    if (/^0x[0-9a-fA-F_]+$/.test(formula.trim())) {
      return `<code>${formula.trim()}</code>`;
    }
    return `<span class="math-inline">${cleanLatexFormula(formula)}</span>`;
  });

  return html;
}

function cleanLatexFormula(tex) {
  let s = tex.trim();

  // Fix known corruptions
  s = s.replace(/\\?u0007lpha/g, '\\alpha');
  s = s.replace(/\blpha\b/g, '\\alpha');
  s = s.replace(/\\?u0007pprox/g, '\\approx');
  s = s.replace(/\\?u0007/g, '');

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

  // Math operators & relations
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

  // Balanced fraction parser for nested expressions
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

  // Square root: \sqrt{x}
  s = s.replace(/\\sqrt\{([^{}]+)\}/g, '&radic;($1)');

  // Spacing
  s = s.replace(/\\quad\b/g, '&emsp;');
  s = s.replace(/\\,|\\ /g, '&thinsp;');

  // Standalone single letters as italic variables (only outside HTML tags)
  s = s.replace(/(^|[^a-zA-Z0-9_>])([a-zA-Z])(?=[^a-zA-Z0-9_<]|$)/g, '$1<i>$2</i>');

  // Strip residual backslashes
  s = s.replace(/\\/g, '');

  return s;
}

// When KaTeX CDN finishes loading, re-run math rendering
window.addEventListener('load', () => {
  if (window.renderMathInElement && contentContainer) {
    try {
      window.renderMathInElement(contentContainer, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ],
        throwOnError: false,
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
      });
    } catch (e) {}
  }
});

// Helper: Wrap tables in horizontally scrollable container if not already wrapped
function wrapTablesInContainer(html) {
  return html.replace(/<table class="comparison-table">([\s\S]*?)<\/table>/gi, (match) => {
    return `<div class="table-wrapper">${match}</div>`;
  });
}

// Render colored tags
function renderTags(tags, isCompleted) {
  let html = '';
  if (isCompleted) {
    html += `<span class="badge badge-completed" title="Completed">&#10003; Completed</span> `;
  }

  html += tags.map(tag => {
    const lower = tag.toLowerCase().trim();
    if (lower.startsWith('x')) {
      const freq = parseInt(lower.slice(1)) || 1;
      let badgeClass = 'badge-pyq-low';
      if (freq >= 5) badgeClass = 'badge-pyq-high';
      else if (freq >= 2) badgeClass = 'badge-pyq-med';
      return `<span class="badge ${badgeClass}" title="Appeared ${freq} times in past papers">&#128293; ${escapeHtml(tag)}</span>`;
    } else if (lower.includes('musa')) {
      return `<span class="badge badge-musa" title="Musa Question Bank Reference">&#128214; ${escapeHtml(tag)}</span>`;
    } else if (lower.includes('syllabus')) {
      return `<span class="badge badge-syllabus" title="Syllabus Only Topic">&#128203; Syllabus</span>`;
    } else {
      return `<span class="badge badge-pyq-low">${escapeHtml(tag)}</span>`;
    }
  }).join(' ');

  return html;
}

// Filter matching logic
function matchesFilter(q) {
  if (currentFilter === 'all') return true;

  if (currentFilter === 'starred') {
    return starredQuestions.has(q.id);
  }
  if (currentFilter === 'completed') {
    return completedQuestions.has(q.id);
  }
  if (currentFilter === 'uncompleted') {
    return !completedQuestions.has(q.id);
  }

  const tags = (q.tags || []).map(t => t.toLowerCase());

  if (currentFilter === 'high-pyq') {
    return tags.some(t => {
      const m = t.match(/x(\d+)/i);
      return m && parseInt(m[1]) >= 3;
    });
  }
  if (currentFilter === 'musa') {
    return tags.some(t => t.includes('musa'));
  }
  if (currentFilter === 'syllabus') {
    return tags.some(t => t.includes('syllabus'));
  }
  return true;
}

// Accordion toggle
window.toggleQuestion = function(cardId) {
  const card = document.getElementById(cardId);
  if (!card) return;
  card.classList.toggle('open');
};

function setupAccordionClicks() {
  // Accordions are handled directly via onclick for instant response
}

// Expand all questions in current view
function expandAllCurrent() {
  document.querySelectorAll('.question-card').forEach(card => {
    card.classList.add('open');
  });
}

// Collapse all questions in current view
function collapseAllCurrent() {
  document.querySelectorAll('.question-card').forEach(card => {
    card.classList.remove('open');
  });
}

// Setup Event Listeners
function setupEventListeners() {
  if (expandAllBtn) expandAllBtn.addEventListener('click', expandAllCurrent);
  if (collapseAllBtn) collapseAllBtn.addEventListener('click', collapseAllCurrent);

  // Filter Chips
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFilter = chip.dataset.filter;
      renderCurrentModule();
    });
  });

  // Search Input
  if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
    searchInput.addEventListener('focus', () => {
      if (searchInput.value.trim().length >= 2) {
        if (searchDropdown) searchDropdown.classList.add('active');
      }
    });
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        if (searchDropdown) searchDropdown.classList.remove('active');
      }
    });
  }

  // Mobile Menu
  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      sidebarOverlay.classList.toggle('open');
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeMobileSidebar);
  }

  // Back to Top Button
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
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
}

// Real-Time Search Handler
function handleSearch(e) {
  const query = e.target.value.trim().toLowerCase();
  searchQuery = query;

  if (query.length < 2) {
    if (searchDropdown) searchDropdown.classList.remove('active');
    if (searchCount) searchCount.textContent = '';
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

  if (searchCount) {
    searchCount.textContent = `${results.length} found`;
  }

  renderSearchResults(results);
}

// Render Search Results Dropdown
function renderSearchResults(results) {
  if (!searchDropdown) return;

  if (results.length === 0) {
    searchDropdown.innerHTML = `
      <div style="padding: 16px; text-align:center; color:var(--text-muted); font-size:13px;">
        No questions matched your search query.
      </div>
    `;
    searchDropdown.classList.add('active');
    return;
  }

  let html = '';
  results.slice(0, 15).forEach(res => {
    html += `
      <div class="search-result-item" onclick="navigateToQuestion(${res.modId}, '${res.qId}')">
        <div class="search-result-mod">Module ${res.modId} &bull; ${escapeHtml(res.matchType)}</div>
        <div class="search-result-q"><strong>Q${res.qId}:</strong> ${escapeHtml(res.question)}</div>
      </div>
    `;
  });

  if (results.length > 15) {
    html += `
      <div style="padding: 8px 16px; font-size: 11.5px; text-align: center; color: var(--text-muted); background: var(--bg-primary);">
        Showing 15 of ${results.length} results. Refine search for more.
      </div>
    `;
  }

  searchDropdown.innerHTML = html;
  searchDropdown.classList.add('active');
}

// Navigate directly to question from search result
window.navigateToQuestion = function(modId, qId) {
  if (searchDropdown) searchDropdown.classList.remove('active');
  if (currentModuleId !== modId) {
    switchModule(modId);
  }

  setTimeout(() => {
    const safeId = `q-${qId.replace(/\./g, '-')}`;
    const card = document.getElementById(safeId);
    if (card) {
      card.classList.add('open');
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      card.style.outline = '2px solid var(--primary-accent)';
      setTimeout(() => card.style.outline = 'none', 2000);
    }
  }, 100);
};

// Copy code button helper
function setupCodeCopyButtons() {
  document.querySelectorAll('pre').forEach(pre => {
    if (pre.querySelector('.code-copy-btn')) return;

    pre.style.position = 'relative';
    const btn = document.createElement('button');
    btn.className = 'code-copy-btn';
    btn.textContent = 'Copy';
    btn.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 3px 8px;
      font-size: 11px;
      font-weight: 600;
      color: #94A3B8;
      background: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
    `;

    btn.addEventListener('click', () => {
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      navigator.clipboard.writeText(code).then(() => {
        btn.textContent = 'Copied!';
        btn.style.color = '#34D399';
        setTimeout(() => {
          btn.textContent = 'Copy';
          btn.style.color = '#94A3B8';
        }, 2000);
      });
    });

    pre.appendChild(btn);
  });
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
