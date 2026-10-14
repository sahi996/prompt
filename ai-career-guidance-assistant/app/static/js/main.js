/* AI Career Guidance Assistant — main.js */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss flash messages ─────────────────────────────────────────
  const flashContainer = document.getElementById('flash-container');
  if (flashContainer) {
    setTimeout(() => {
      flashContainer.querySelectorAll('.alert').forEach(alert => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 300);
      });
    }, 5000);
  }

  // ── Navbar scroll effect ────────────────────────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        nav.style.background = 'rgba(10,14,35,0.98)';
      } else {
        nav.style.background = 'rgba(15,21,53,0.95)';
      }
    }, { passive: true });
  }

  // ── Skill gap checkboxes: toggle known/gap class ─────────────────────────
  document.querySelectorAll('.skill-check').forEach(cb => {
    cb.addEventListener('change', function () {
      const tag = this.closest('.skill-item')?.querySelector('.skill-tag');
      if (!tag) return;
      if (this.checked) {
        tag.classList.remove('gap');
        tag.classList.add('known');
      } else {
        tag.classList.remove('known');
        tag.classList.add('gap');
      }
    });
  });

  // ── Progress bar animated fill ───────────────────────────────────────────
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        bar.style.width = bar.dataset.width || '0%';
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.progress-bar[data-width]').forEach(bar => {
    bar.style.width = '0%';
    observer.observe(bar);
  });

  // ── Career search live filter ────────────────────────────────────────────
  const searchInput = document.getElementById('careerSearch');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const q = this.value.toLowerCase().trim();
      document.querySelectorAll('[data-career-card]').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.closest('.col').style.display = text.includes(q) ? '' : 'none';
      });
    });
  }

  // ── Roadmap stage toggle ─────────────────────────────────────────────────
  document.querySelectorAll('.stage-checkbox').forEach(cb => {
    cb.addEventListener('change', function () {
      const stageId = this.dataset.stageId;
      const completed = this.checked;
      const roadmapId = this.dataset.roadmapId;

      fetch(`/roadmaps/${roadmapId}/progress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ stage_id: stageId, completed: completed }),
      })
      .then(r => r.json())
      .then(data => {
        const pct = document.getElementById('roadmapProgress');
        if (pct && data.percent !== undefined) {
          pct.style.width = data.percent + '%';
          pct.setAttribute('aria-valuenow', data.percent);
          const label = document.getElementById('roadmapProgressLabel');
          if (label) label.textContent = data.percent + '%';
        }
        const step = this.closest('.roadmap-step');
        if (step) step.classList.toggle('completed', completed);
      })
      .catch(() => {/* silently fail — user sees no broken UI */});
    });
  });

  // ── Interview practice feedback ──────────────────────────────────────────
  const feedbackForm = document.getElementById('interviewFeedbackForm');
  if (feedbackForm) {
    feedbackForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = feedbackForm.querySelector('[type=submit]');
      const original = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analysing…';

      const data = Object.fromEntries(new FormData(feedbackForm));
      fetch('/assessment/interview-feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
        body: JSON.stringify(data),
      })
      .then(r => r.json())
      .then(resp => {
        const box = document.getElementById('feedbackResult');
        if (box) {
          box.innerHTML = `<div class="alert alert-info">${escapeHtml(resp.feedback)}</div>`;
          box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      })
      .finally(() => {
        btn.disabled = false;
        btn.innerHTML = original;
      });
    });
  }

  // ── Helpers ──────────────────────────────────────────────────────────────
  function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    const inp = document.querySelector('input[name="csrf_token"]');
    return inp ? inp.value : '';
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

});
