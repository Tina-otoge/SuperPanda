function toggleFullscreen(elem = document.documentElement) {
	if (document.fullscreenElement)
		return document.exitFullscreen();
	elem.requestFullscreen();
}
document.addEventListener('keydown', e => {
	if (document.activeElement != document.body)
		return;
	if (e.key == 's')
		window.scrollBy(0, 50);
	if (['z', 'w'].includes(e.key))
		window.scrollBy(0, -50);
	if (['f'].includes(e.key))
		toggleFullscreen();
});

const galleries = document.getElementById('galleries');
if (galleries) {
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
}

const gallery = document.getElementById('gallery');

const reader = document.getElementById('reader');
if (reader) {
	const next_page = reader.querySelector('a.next');
	const prev_page = reader.querySelector('a.previous');
	const back_gallery = document.getElementById('back-to-gallery');

	document.addEventListener('keydown', e => {
		if (['q', 'a', 'h', 'ArrowLeft'].includes(e.key) && prev_page)
			location.href = prev_page.href;
		else if (['d', 'l', 'ArrowRight'].includes(e.key) && next_page)
			location.href = next_page.href;
		else if (['Backspace', 'g'].includes(e.key))
			location.href = back_gallery.href;
	});
}

if (reader || gallery) {
	const back_home = document.getElementById('back-to-home');

	document.addEventListener('keydown', e => {
		if (['e', 't'].includes(e.key))
			location.href = back_home.href;
	});
}
