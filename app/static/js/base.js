const filter_all_toggle = document.getElementById('toggle-all-filters');
const filters = document.getElementById('filters').querySelectorAll('input');

if (filter_all_toggle) filter_all_toggle.onclick = () => {
	let current = true;
	filters.forEach(e => {
		current = current && e.checked;
	});
	filters.forEach(e => {
		e.checked = !current;
	});
};
