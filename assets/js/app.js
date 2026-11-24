/**
 * Embedded Systems & RTOS Study Guide - Interactive Dashboard App
 */

// Global State
let studyData = [];
let currentModuleId = 1;
let currentFilter = 'all'; // 'all', 'high-pyq', 'musa', 'syllabus'
let searchQuery = '';

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
  setupEventListeners();
  await loadAllModuleData();
  renderSidebar();
  renderCurrentModule();
  setupCodeCopyButtons();
});

// Load data for all modules
async function loadAllModuleData() {
  const modulesToLoad = [1, 2, 3, 4, 5, 6];
  studyData = [];

  for (const modNum of modulesToLoad) {
    try {
      // Check if data is already provided via window.embeddedStudyData
      if (window.embeddedStudyData && window.embeddedStudyData[modNum]) {
        studyData.push(window.embeddedStudyData[modNum]);
        continue;
      }
      
      const response = await fetch(`data/mod${modNum}_answers.json`);
      if (response.ok) {
        const json = await response.json();
        studyData.push(json);
      } else {
        console.warn(`Could not load mod${modNum}_answers.json`);
      }
    } catch (e) {
      // If running directly from file:// and fetch is blocked, check window variable
      if (window.embeddedStudyData && window.embeddedStudyData[modNum]) {
        studyData.push(window.embeddedStudyData[modNum]);
      } else {
        console.warn(`Error loading module ${modNum}:`, e);
      }
    }
  }

  // Sort modules in numerical order
  studyData.sort((a, b) => a.module - b.module);
  updateGlobalStats();
}

// Update total questions count in sidebar footer
function updateGlobalStats() {
  let totalQuestions = 0;
  let pyqHighCount = 0;

  studyData.forEach(mod => {
    (mod.topics || []).forEach(t => {
      (t.questions || []).forEach(q => {
        totalQuestions++;
        const isHigh = (q.tags || []).some(tag => {
          const m = tag.match(/x(\d+)/i);
          return m && parseInt(m[1]) >= 3;
        });
        if (isHigh) pyqHighCount++;
      });
    });
  });

  const totalElem = document.getElementById('total-questions-count');
  if (totalElem) totalElem.textContent = `${totalQuestions} Questions`;
  
  const highElem = document.getElementById('high-freq-count');
  if (highElem) highElem.textContent = `${pyqHighCount} High-Yield`;
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
    (mod.topics || []).forEach(t => qCount += (t.questions || []).length);

    const a = document.createElement('a');
    a.className = `nav-item ${mod.module === currentModuleId ? 'active' : ''}`;
    a.dataset.modId = mod.module;
    a.href = `#module-${mod.module}`;

    a.innerHTML = `
      <span class="nav-item-title">Mod ${mod.module}: ${escapeHtml(mod.title.split('&')[0].trim())}</span>
      <span class="nav-item-meta">
        <span class="nav-badge">${qCount} Qs</span>
      </span>
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

  // Update active state in sidebar
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
  let pyqSum = 0;
  let musaCount = 0;

  (mod.topics || []).forEach(t => {
    (t.questions || []).forEach(q => {
      totalModQuestions++;
      (q.tags || []).forEach(tag => {
        const m = tag.match(/x(\d+)/i);
        if (m) pyqSum += parseInt(m[1]);
        if (tag.toLowerCase().includes('musa')) musaCount++;
      });
    });
  });

  let html = `
    <div class="module-section active" id="module-${mod.module}">
      <div class="module-hero">
        <div>
          <div class="module-number">Module ${mod.module} &bull; University Exam Guide</div>
          <h1 class="module-title">${escapeHtml(mod.title)}</h1>
        </div>
        <div class="module-stats">
          <div class="stat-pill">
            <div class="stat-value">${totalModQuestions}</div>
            <div class="stat-label">Total Questions</div>
          </div>
          <div class="stat-pill">
            <div class="stat-value">${musaCount}</div>
            <div class="stat-label">Musa Reference</div>
          </div>
        </div>
      </div>
  `;

  // Render Topics and Questions
  (mod.topics || []).forEach(topic => {
    const filteredQuestions = (topic.questions || []).filter(q => matchesFilter(q));
    if (filteredQuestions.length === 0 && currentFilter !== 'all') {
      return; // Skip empty topic when filtering
    }

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
  setupAccordionClicks();
  setupCodeCopyButtons();
}

// Render individual question card
function renderQuestionCard(q, topicId) {
  const tagsHtml = renderTags(q.tags || []);
  const safeId = `q-${q.id.replace(/\./g, '-')}`;

  return `
    <div class="question-card" id="${safeId}" data-qid="${q.id}">
      <div class="question-header" onclick="toggleQuestion('${safeId}')">
        <div class="question-title-area">
          <div class="question-num">Question ${q.id}</div>
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

// Helper: Wrap tables in horizontally scrollable container if not already wrapped
function wrapTablesInContainer(html) {
  return html.replace(/<table class="comparison-table">([\s\S]*?)<\/table>/gi, (match) => {
    return `<div class="table-wrapper">${match}</div>`;
  });
}

// Render colored tags
function renderTags(tags) {
  return tags.map(tag => {
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
}

// Filter matching logic
function matchesFilter(q) {
  if (currentFilter === 'all') return true;
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
  // Expand / Collapse All
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
    // Close dropdown on outside click
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

  // Allow DOM to render
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
