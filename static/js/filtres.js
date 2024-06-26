const centerFilters = () => {
	const filtersContainer = document.getElementById('filters-container');
	const filtersContainer_size = parseInt(window.getComputedStyle(filtersContainer, null).getPropertyValue('width').replace(/px/, ''));
	const filtersContainerParent_size = parseInt(window.getComputedStyle(filtersContainer.parentElement, null).getPropertyValue('width').replace(/px/, ''));

	if(filtersContainer_size < filtersContainerParent_size) {
		const diff = filtersContainerParent_size - filtersContainer_size;
		const pos = diff / 2;

		filtersContainer.style.left = `${pos}px`;
	}

	return filtersContainer.style.transition = 'left .5s';
};

try {
	centerFilters();
} catch(e) {}


const filters_slide = (direction) => {
	const filtersContainer = document.getElementById('filters-container');
	const pos = parseInt(filtersContainer.style.left.replace(/px/, ''));
	const filtersContainer_size = parseInt(window.getComputedStyle(filtersContainer, null).getPropertyValue('width').replace(/px/, ''));
	const filtersContainerParent_size = parseInt(window.getComputedStyle(filtersContainer.parentElement, null).getPropertyValue('width').replace(/px/, ''));

	if(filtersContainerParent_size > filtersContainer_size) {
		const diff = filtersContainerParent_size - filtersContainer_size;
		const pos = diff / 2;

		return filtersContainer.style.left = `${pos}px`;
	}

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

let userColor2 = '#fff';
if(!document.location.pathname.match(/^\/messages/))
	userColor2 = document.getElementById('filters').dataset.usercolor2;

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
				filter.style.backgroundColor = '#fff';
				filter.style.opacity = '.6';
				filter.style.textDecoration = 'line-through';
			});
		}
		else {
			Array.from(document.getElementsByClassName('demande')).forEach(demande => {
				demande.style.display = 'block';
			});
			document.querySelectorAll('.filter > button').forEach(filter => {
				filter.classList.remove('is-light');
				filter.style.backgroundColor = userColor2;
				filter.style.opacity = '1';
				filter.style.textDecoration = 'none';
			});
		}
	}

	else {
		if(document.querySelectorAll('.filter.subject button.is-light').length) {
			document.querySelector('.filter[data-subject="everything"] > button').classList.add('is-light');
			document.querySelector('.filter[data-subject="everything"] > button').style.backgroundColor = '#fff';
			document.querySelector('.filter[data-subject="everything"] > button').style.opacity = '.6';
			document.querySelector('.filter[data-subject="everything"] > button').style.textDecoration = 'line-through';
		}
		else {
			document.querySelector('.filter[data-subject="everything"] > button').classList.remove('is-light');
			document.querySelector('.filter[data-subject="everything"] > button').style.backgroundColor = userColor2;
			document.querySelector('.filter[data-subject="everything"] > button').style.opacity = '1';
			document.querySelector('.filter[data-subject="everything"] > button').style.textDecoration = 'none';
		}

		if(selected) {
			document.querySelectorAll(`.demande[data-subject=${subject}]`).forEach(demande => {
				demande.style.display = 'none';
			});
			f.style.backgroundColor = '#fff';
			f.style.opacity = '.6';
			f.style.textDecoration = 'line-through';
		}
		else {
			document.querySelectorAll(`.demande[data-subject=${subject}]`).forEach(demande => {
				demande.style.display = 'block';
			});
			f.style.backgroundColor = userColor2;
			f.style.opacity = '1';
			f.style.textDecoration = 'none';
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

const grp_filter = (v) => {
	const value = v.trim().toLowerCase();
	if(v === '') {
		Array.from(document.getElementsByClassName('listedGrp')).forEach(grp => {
			grp.style.display = 'table-row';
		});
	}

	else {
		Array.from(document.getElementsByClassName('listedGrp')).forEach(grp => {
			const grpName = (grp.dataset.grpname || '').toLowerCase();
			const grpUsers = JSON.parse(grp.dataset.grpusers);

			grp.style.display = 'none';

			if(grpName.startsWith(value))
				return grp.style.display = 'table-row';
			else {
				grpUsers.forEach(user => {
					if(user.pseudo.toLowerCase().startsWith(value) || user.prenom.toLowerCase().startsWith(value) || user.nom.toLowerCase().startsWith(value))
						return grp.style.display = 'table-row';
				});
			}
		});
	}
};

var lastScrollTop = 0;
$(window).scroll(function(event){
   var st = $(this).scrollTop();
   if (st > lastScrollTop){
		 document.getElementById('filters').style.position = "";
       document.getElementById('filters').style.display = "none";
   } else {
       document.getElementById('filters').style.display = "flex";
			 document.getElementById('filters').style.position = "fixed";
   }
   lastScrollTop = st;
});
