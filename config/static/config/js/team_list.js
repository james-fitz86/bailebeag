console.log("team list JS loaded");

document.addEventListener('DOMContentLoaded', () => {
  const table = document.querySelector('#teams_table');
  if (!table) return;

  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));

  const genderFilter  = document.querySelector('#gender_filter');
  const sportFilter = document.querySelector('#sport_filter');
  const ageGroupFilter = document.querySelector('#age_group_filter');
  const resetBtn = document.querySelector('#reset_filters');

  function applyFilters() {
    const genderVal  = (genderFilter?.value || 'all').toLowerCase();
    const sportVal = (sportFilter?.value || 'all').toLowerCase();
    const ageGroupVal = (ageGroupFilter?.value || 'all').toLowerCase();

    rows.forEach(row => {
        const gender  = (row.dataset.gender  || '').toLowerCase();
        const sport = (row.dataset.sport || '').toLowerCase();
        const ageGroup = (row.dataset.age_group || '').toLowerCase();

        const matchesGender =
          genderVal === 'all' || gender === genderVal;

        const matchesSport =
          sportVal === 'all' || sport === sportVal;

        const matchesAgeGroup =
          ageGroupVal === 'all' || ageGroup === ageGroupVal;

        row.style.display = (matchesGender && matchesSport && matchesAgeGroup) ? '' : 'none';
    });

  }


  applyFilters(); 

  genderFilter?.addEventListener('change', applyFilters);
  sportFilter?.addEventListener('change', applyFilters);
  ageGroupFilter?.addEventListener('change', applyFilters);
  
  resetBtn?.addEventListener('click', () => {
    genderFilter.value = 'all';
    sportFilter.value = 'all';
    ageGroupFilter.value = 'all';
    applyFilters();
  });
});