const state = {
  papers: [],
  filters: { query: '', year: 'all', category: 'all', status: 'all' }
};

const statusLabels = {
  planned: '待读',
  reading: '阅读中',
  read: '已阅读',
  discussed: '已讨论'
};

const elements = {};

document.addEventListener('DOMContentLoaded', async () => {
  Object.assign(elements, {
    search: document.querySelector('#search-input'),
    year: document.querySelector('#year-filter'),
    category: document.querySelector('#category-filter'),
    status: document.querySelector('#status-filter'),
    clear: document.querySelector('#clear-filters'),
    tbody: document.querySelector('#paper-table-body'),
    cards: document.querySelector('#paper-card-list'),
    empty: document.querySelector('#empty-state'),
    resultCount: document.querySelector('#result-count')
  });

  setupTheme();
  bindFilters();

  try {
    const response = await fetch('data/papers.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.papers = await response.json();
    populateFilters();
    updateStats();
    render();
  } catch (error) {
    elements.resultCount.textContent = '论文数据载入失败';
    elements.empty.hidden = false;
    elements.empty.querySelector('h3').textContent = '无法载入论文数据';
    elements.empty.querySelector('p').textContent = '请通过本地服务器或 GitHub Pages 打开页面。';
    console.error(error);
  }
});

function setupTheme() {
  const toggle = document.querySelector('.theme-toggle');
  toggle.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('paper-library-theme', next);
  });
}

function bindFilters() {
  elements.search.addEventListener('input', (event) => {
    state.filters.query = event.target.value.trim().toLowerCase();
    render();
  });
  [['year', elements.year], ['category', elements.category], ['status', elements.status]].forEach(([key, element]) => {
    element.addEventListener('change', (event) => {
      state.filters[key] = event.target.value;
      render();
    });
  });
  elements.clear.addEventListener('click', () => {
    state.filters = { query: '', year: 'all', category: 'all', status: 'all' };
    elements.search.value = '';
    elements.year.value = 'all';
    elements.category.value = 'all';
    elements.status.value = 'all';
    render();
  });
}

function populateFilters() {
  const years = [...new Set(state.papers.map((paper) => paper.year))].sort((a, b) => b - a);
  const categories = [...new Set(state.papers.map((paper) => paper.category))].sort();
  years.forEach((year) => elements.year.append(new Option(String(year), String(year))));
  categories.forEach((category) => elements.category.append(new Option(category, category)));
}

function updateStats() {
  const categories = new Set(state.papers.map((paper) => paper.category));
  document.querySelector('#paper-count').textContent = state.papers.length;
  document.querySelector('#note-count').textContent = state.papers.filter((paper) => paper.status === 'read' && paper.notes_url).length;
  document.querySelector('#discussion-count').textContent = state.papers.filter((paper) => paper.discussed === true).length;
  document.querySelector('#topic-count').textContent = categories.size;
}

function getFilteredPapers() {
  return state.papers.filter((paper) => {
    const haystack = [paper.title, paper.authors.join(' '), paper.venue, paper.category, paper.method, paper.summary, ...(paper.tags || [])].join(' ').toLowerCase();
    const matchesStatus = state.filters.status === 'all'
      || (state.filters.status === 'discussed' ? paper.discussed === true : paper.status === state.filters.status);
    return (!state.filters.query || haystack.includes(state.filters.query))
      && (state.filters.year === 'all' || String(paper.year) === state.filters.year)
      && (state.filters.category === 'all' || paper.category === state.filters.category)
      && matchesStatus;
  });
}

function render() {
  const papers = getFilteredPapers();
  elements.tbody.replaceChildren(...papers.map(createTableRow));
  elements.cards.replaceChildren(...papers.map(createCard));
  elements.empty.hidden = papers.length !== 0;
  elements.resultCount.textContent = `显示 ${papers.length} / ${state.papers.length} 篇论文`;
}

function createTableRow(paper) {
  const row = document.createElement('tr');
  row.append(
    cell(createPaperHeading(paper)),
    cell(fragment(`<span class="venue">${escapeHtml(paper.year)} / ${escapeHtml(paper.venue)}</span>`, createStatusGroup(paper))),
    cell(fragment(escapeHtml(paper.category), createTags(paper.tags))),
    cell(text(paper.method)),
    cell(text(paper.summary)),
    cell(createResources(paper)),
    cell(createNotesLink(paper))
  );
  return row;
}

function createCard(paper) {
  const article = document.createElement('article');
  article.className = 'paper-card';
  const heading = createPaperHeading(paper);
  const meta = document.createElement('div');
  meta.className = 'paper-card__meta';
  meta.append(text(`${paper.year} / ${paper.venue}`), text(paper.category), text(paper.method), createStatusGroup(paper));
  const summary = document.createElement('p');
  summary.className = 'paper-card__summary';
  summary.textContent = paper.summary;
  const footer = document.createElement('div');
  footer.className = 'paper-card__footer';
  footer.append(createResources(paper), createNotesLink(paper));
  article.append(heading, meta, summary, createTags(paper.tags), footer);
  return article;
}

function createPaperHeading(paper) {
  const wrapper = document.createElement('div');
  const link = document.createElement('a');
  link.className = 'paper-title';
  link.href = paper.paper_url;
  link.target = '_blank';
  link.rel = 'noreferrer';
  link.textContent = paper.title;
  const authors = document.createElement('span');
  authors.className = 'paper-authors';
  authors.textContent = paper.authors.join(', ');
  wrapper.append(link, authors);
  return wrapper;
}

function createStatus(status) {
  const badge = document.createElement('span');
  badge.className = `status status--${status}`;
  badge.textContent = statusLabels[status] || status;
  return badge;
}

function createStatusGroup(paper) {
  const group = document.createElement('span');
  group.className = 'status-group';
  group.append(createStatus(paper.status));
  if (paper.discussed === true) group.append(createStatus('discussed'));
  return group;
}

function createTags(tags = []) {
  const list = document.createElement('div');
  list.className = 'tag-list';
  tags.forEach((tag) => {
    const item = document.createElement('span');
    item.className = 'tag';
    item.textContent = tag;
    list.append(item);
  });
  return list;
}

function createResources(paper) {
  const wrapper = document.createElement('div');
  wrapper.className = 'resource-links';
  [['Paper', paper.paper_url], ['Code', paper.code_url], ['Data', paper.data_url]].forEach(([label, url]) => {
    if (!url) return;
    const link = document.createElement('a');
    link.className = 'resource-link';
    link.href = url;
    link.target = '_blank';
    link.rel = 'noreferrer';
    link.textContent = label;
    wrapper.append(link);
  });
  return wrapper;
}

function createNotesLink(paper) {
  if (!paper.notes_url) return text('—');
  const link = document.createElement('a');
  link.className = 'notes-link';
  link.href = paper.notes_url;
  link.textContent = paper.status === 'planned' ? '笔记框架 →' : '阅读笔记 →';
  return link;
}

function cell(content) {
  const td = document.createElement('td');
  td.append(content);
  return td;
}

function text(value) { return document.createTextNode(value ?? ''); }

function fragment(html, ...nodes) {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = html;
  wrapper.append(...nodes);
  return wrapper;
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  })[character]);
}

