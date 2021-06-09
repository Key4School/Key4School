const filters_slide = (direction) => {
	const filtersContainer = document.getElementById('filters-container');
	const pos = parseInt(filtersContainer.style.left.replace(/px/, ''));
	const filtersContainer_size = parseInt(window.getComputedStyle(filtersContainer, null).getPropertyValue('width').replace(/px/, ''));
	const filtersContainerParent_size = parseInt(window.getComputedStyle(filtersContainer.parentElement, null).getPropertyValue('width').replace(/px/, ''));

	if(filtersContainerParent_size > filtersContainer_size)
		return filtersContainer.style.left = '0px';

	if(direction === 'left') {
		if(pos + 80 > 0)
			return filtersContainer.style.left = '0px';
		return filtersContainer.style.left = `${pos+80}px`;
	}

	else {
		if(pos - 80 < -filtersContainer_size + filtersContainerParent_size)
			return filtersContainer.style.left = `${-filtersContainer_size + filtersContainerParent_size}px`;
		return filtersContainer.style.left = `${pos-80}px`;
	}
};

const filter = (f) => {
	const subject = f.parentElement.dataset.subject;
	const selected = !f.classList.contains('is-light');

	f.classList.toggle('is-light');

	if(subject === 'everything') {
		if(selected) {
			Array.from(document.getElementsByClassName('demande')).forEach(demande => {
				demande.style.display = 'none';
			});
			document.querySelectorAll('.filter button').forEach(filter => {
				filter.classList.add('is-light');
			});
		}
		else {
			Array.from(document.getElementsByClassName('demande')).forEach(demande => {
				demande.style.display = 'block';
			});
			document.querySelectorAll('.filter > button').forEach(filter => {
				filter.classList.remove('is-light');
			});
		}
	}

	else {
		if(document.querySelectorAll('.filter.subject button.is-light').length)
			document.querySelector('.filter[data-subject="everything"] > button').classList.add('is-light');
		else
			document.querySelector('.filter[data-subject="everything"] > button').classList.remove('is-light');

		if(selected) {
			document.querySelectorAll(`.demande[data-subject=${subject}]`).forEach(demande => {
				demande.style.display = 'none';
			});
		}
		else {
			document.querySelectorAll(`.demande[data-subject=${subject}]`).forEach(demande => {
				demande.style.display = 'block';
			});
		}
	}
};

const user_filter = (v) => {
	const value = v.trim().toLowerCase();
	if(v === '') {
		Array.from(document.getElementsByClassName('listedUser')).forEach(user => {
			user.style.display = 'block';
		});
	}

	else {
		Array.from(document.getElementsByClassName('listedUser')).forEach(user => {
			const id = (user.dataset.id || '').toLowerCase();
			const pseudo = (user.dataset.pseudo || '').toLowerCase();
			const nom = (user.dataset.nom || '').toLowerCase();
			const prenom = (user.dataset || '').prenom.toLowerCase();
			const lycee = (user.dataset.lycee || '').replace(/LGT-/, '').toLowerCase();
			const email = (user.dataset.email || '').toLowerCase();
			const telephone = (user.dataset.telephone || '').toLowerCase();

			if(id.startsWith(value) || pseudo.startsWith(value) || nom.startsWith(value) || prenom.startsWith(value) || lycee.startsWith(value) || email.startsWith(value) || telephone.startsWith(value))
				user.style.display = 'block';
			else
				user.style.display = 'none';
		});
	}
}