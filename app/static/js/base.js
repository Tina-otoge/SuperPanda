// https://stackoverflow.com/a/5448595
function findGetParameter(parameterName) {
	var result = null,
		tmp = [];
	location.search
		.substr(1)
		.split("&")
		.forEach(function (item) {
  			tmp = item.split("=");
  			if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
		});
	return result;
}

function toggleFullscreen(elem = document.documentElement) {
	if (document.fullscreenElement)
		return document.exitFullscreen();
	elem.requestFullscreen();
}
document.addEventListener('keydown', e => {
	if (document.activeElement != document.body)
		return;
	if (['s', 'j'].includes(e.key))
		window.scrollBy(0, 50);
	if (['z', 'w', 'k'].includes(e.key))
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
	document.addEventListener('keydown', e => {
		if (document.activeElement != document.body)
			return;
		if (e.key == 'e') {
			let current_search = findGetParameter('search');
			if (current_search)
				current_search += ' '
			location.href = (
				location.origin + location.pathname +
				'?search=' + encodeURIComponent(current_search + ' language:english')
			);
		}
	});
}

const gallery = document.getElementById('gallery');
if (gallery) {
	const artist = gallery.querySelector('.tags-group.artist a')
	const group = gallery.querySelector('.tags-group.group a')
	const parody = gallery.querySelector('.tags-group.parody a')
	const character = gallery.querySelector('.tags-group.character a')

	document.addEventListener('keydown', e => {
		if (e.key == 'a' && artist)
			location.href = artist.href;
		else if (e.key == 'g' && group)
			location.href = group.href;
		else if (e.key == 'p' && parody)
			location.href = parody.href;
		else if (e.key == 'c' && character)
			location.href = character.href;
	});
}

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
