document.addEventListener('DOMContentLoaded', () => {
  const table = document.querySelector('#bookings_table');
  if (!table) return;

  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));

  const pitchFilter  = document.querySelector('#pitch_filter');
  const statusFilter = document.querySelector('#status_filter');
  const resetBtn = document.querySelector('#reset_filters');

  rows.sort((a, b) => {
    const da = new Date(a.dataset.start || 0);
    const db = new Date(b.dataset.start || 0);
    return da - db;
  });
  rows.forEach(r => tbody.appendChild(r));

  function applyFilters() {
    const pitchVal  = (pitchFilter?.value || 'all').toLowerCase();
    const statusVal = (statusFilter?.value || 'all').toLowerCase();

    rows.forEach(row => {
      const pitch  = (row.dataset.pitch  || '').toLowerCase();
      const status = (row.dataset.status || '').toLowerCase();

      const matchesPitch =
        pitchVal === 'all' ||
        (pitchVal === 'astro' && pitch.includes('astro')) ||
        (pitchVal === 'main'  && pitch.includes('main'));

      const matchesStatus =
        statusVal === 'all' || status === statusVal;

      row.style.display = (matchesPitch && matchesStatus) ? '' : 'none';
    });
  }

  applyFilters();

  pitchFilter?.addEventListener('change', applyFilters);
  statusFilter?.addEventListener('change', applyFilters);

  resetBtn?.addEventListener('click', () => {
    pitchFilter.value = 'all';
    statusFilter.value = 'all';
    applyFilters();
  });
});

