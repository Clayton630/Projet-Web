// ========================== VARIABLES GLOBALES =============================

// Liste de tous les marqueurs affichés sur la carte (pour les retirer facilement)
var markers = [];
// Objet principal Leaflet représentant la carte
var map;
// Cercle représentant la position de l'utilisateur sur la carte
var userCircle = null;
// Coordonnées [lat, lon] de l'utilisateur si la géolocalisation est activée
var userCoords = null;

// ========================== GESTION DES COULEURS ============================

// Liste des couleurs utilisées pour distinguer les catégories d'établissements
const colorList = [
    "red", "blue", "orange", "green", "violet", "grey", "yellow"
];
// Dictionnaire pour mémoriser la couleur attribuée à chaque catégorie
const categoryColorMap = {};
let colorIndex = 0;

// Fonction qui attribue une couleur à une catégorie (toujours la même couleur pour la même catégorie)
function getCategoryColor(category) {
    if (!(category in categoryColorMap)) {
        // Si la catégorie n'a pas encore de couleur, on lui en attribue une
        categoryColorMap[category] = colorList[colorIndex % colorList.length];
        colorIndex++;
    }
    return categoryColorMap[category];
}

// ========================= ICONE PERSONNALISEE POUR MARQUEUR =================

// Fonction qui génère une icône SVG colorée pour un marker Leaflet
function createModernMarkerIcon(color) {
    const svg = `
    <svg width="30" height="40" viewBox="0 0 30 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="15" cy="15" r="10" fill="${color}" fill-opacity="0.85" stroke="#fff" stroke-width="2" />
        <path d="M15 40C15 40 30 23 30 15C30 6.71573 23.2843 0 15 0C6.71573 0 0 6.71573 0 15C0 23 15 40 15 40Z" fill="${color}" fill-opacity="0.35" />
        <circle cx="15" cy="15" r="5" fill="#fff" fill-opacity="0.7" />
    </svg>`.trim();

    // On retourne un divIcon Leaflet personnalisé
    return L.divIcon({
        className: 'modern-marker-icon',
        html: svg,
        iconSize: [30, 40],
        iconAnchor: [15, 40],
        popupAnchor: [0, -40]
    });
}

// ======================= AFFICHAGE DES ETOILES DE NOTE =======================

// Retourne le HTML pour afficher la note moyenne sous forme d'étoiles remplies
function getStarsHTML(moyenne) {
    // Calcule le pourcentage d'étoiles remplies (sur 5)
    const percentage = moyenne ? (Math.max(0, Math.min(5, moyenne)) / 5 * 100) : 0;
    return `<span class="stars-outer"><span class="stars-inner" style="width:${percentage}%"></span></span>`;
}

// ===================== AJOUT/RAFRAICHISSEMENT DES MARQUEURS ==================

// Place les marqueurs correspondant à la liste d'établissements filtrée
function addMarkers(filteredEtablissements) {
    // Supprime tous les marqueurs actuels de la carte
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Ajoute un marker pour chaque établissement filtré
    filteredEtablissements.forEach(function(etab) {
        // On ne crée un marker que si l'établissement a des coordonnées valides
        if (etab.latitude && etab.longitude) {
            let cat = etab.categorie || "Autre";
            let color = getCategoryColor(cat);
            let moyenne = etab.moyenne || 0;
            let icon = createModernMarkerIcon(color);

            // On crée le marker Leaflet
            var marker = L.marker([etab.latitude, etab.longitude], {icon: icon})
                .addTo(map)
                .bindPopup(
                    // Popup HTML : nom cliquable, adresse, catégorie, note
                    `<b><a href="#" class="etab-link" data-id="${etab.id_etab}">${etab.nom}</a></b><br>` +
                    `${etab.adresse}<br><small>Catégorie : ${cat}</small><br>` +
                    `<span title="${moyenne ? moyenne + '/5' : 'Aucune note'}">` +
                    `${moyenne ? getStarsHTML(moyenne) + ` (${moyenne}/5)` : 'Pas de note'}</span>`
                );
            // On garde la référence dans la liste globale
            markers.push(marker);
        }
    });
}

// ======================= FILTRAGE DES ETABLISSEMENTS =========================

// Filtre la liste des établissements selon le texte recherché et la catégorie sélectionnée
function filterEtablissements() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categorySelect').value;
    const filtered = etablissements.filter(etab => {
        return (etab.nom.toLowerCase().includes(query) || !query) &&
            (etab.categorie === category || !category);
    });
    addMarkers(filtered);
}

// ==================== GESTION DU POINT UTILISATEUR (GEOLOCALISATION) ==========

// Ajoute ou déplace un cercle sur la position de l'utilisateur
function setUserCircle(lat, lon) {
    if (userCircle) map.removeLayer(userCircle); // Enlève l'ancien cercle si déjà affiché
    userCircle = L.circle([lat, lon], {
        color: '#111',
        fillColor: '#222',
        fillOpacity: 0.33,
        radius: 22
    }).addTo(map).bindPopup("Vous êtes ici");
    userCircle.openPopup();
}

// =============== INITIALISATION DE LA CARTE (SANS GEOLOCALISATION) ============

// Place la carte à un centre par défaut (si géoloc non accordée)
function setDefaultMap() {
    map = L.map('map', {zoomControl: false, attributionControl: false}).setView([43.116669, 5.93333], 14);
    L.tileLayer('https://api.maptiler.com/maps/basic-v2/{z}/{x}/{y}@2x.png?key=1XPmmAxswHqtzHfGMCGh', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &amp; <a href="https://www.maptiler.com/copyright/">MapTiler</a>',
        maxZoom: 20
    }).addTo(map);
    addMarkers(etablissements);
    addCustomControls();
}

// ================== BOUTONS PERSONNALISES DE LA CARTE =========================

// Ajoute des boutons zoom +/-, recentrer, sur la carte Leaflet
function addCustomControls() {
    var controlsContainer = L.DomUtil.create('div', 'custom-control-container');

    // Bouton zoom +
    var zoomInBtn = L.DomUtil.create('button', 'custom-control-button');
    zoomInBtn.title = "Zoomer";
    zoomInBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="lucide lucide-plus-circle">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="16"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
        </svg>`;
    L.DomEvent.on(zoomInBtn, 'click', function(e) {
        e.preventDefault();
        zoomInBtn.classList.remove('clicked');
        void zoomInBtn.offsetWidth;
        zoomInBtn.classList.add('clicked');
        setTimeout(() => { map.zoomIn(); }, 50);
    });

    // Bouton zoom -
    var zoomOutBtn = L.DomUtil.create('button', 'custom-control-button');
    zoomOutBtn.title = "Dézoomer";
    zoomOutBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="lucide lucide-minus-circle">
            <circle cx="12" cy="12" r="10"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
        </svg>`;
    L.DomEvent.on(zoomOutBtn, 'click', function(e) {
        e.preventDefault();
        zoomOutBtn.classList.remove('clicked');
        void zoomOutBtn.offsetWidth;
        zoomOutBtn.classList.add('clicked');
        setTimeout(() => { map.zoomOut(); }, 50);
    });

    // Bouton recentrer
    var recenterBtn = L.DomUtil.create('button', 'custom-control-button');
    recenterBtn.title = "Recentrer sur ma position";
    recenterBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="lucide lucide-target">
            <circle cx="12" cy="12" r="10"/>
            <circle cx="12" cy="12" r="2"/>
            <line x1="12" y1="2" x2="12" y2="4"/>
            <line x1="12" y1="20" x2="12" y2="22"/>
            <line x1="20" y1="12" x2="22" y2="12"/>
            <line x1="2" y1="12" x2="4" y2="12"/>
        </svg>`;
    L.DomEvent.on(recenterBtn, 'click', function(e) {
        e.preventDefault();
        if (userCoords) {
            map.setView(userCoords, 14);
            setUserCircle(userCoords[0], userCoords[1]);
        } else if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                userCoords = [position.coords.latitude, position.coords.longitude];
                map.setView(userCoords, 14);
                setUserCircle(userCoords[0], userCoords[1]);
            }, function() {
                alert("Impossible d'accéder à votre position.");
            });
        }
        recenterBtn.classList.remove('clicked');
        void recenterBtn.offsetWidth;
        recenterBtn.classList.add('clicked');
    });

    controlsContainer.appendChild(zoomInBtn);
    controlsContainer.appendChild(zoomOutBtn);
    controlsContainer.appendChild(recenterBtn);

    controlsContainer.style.position = 'absolute';
    controlsContainer.style.top = '10px';
    controlsContainer.style.right = '10px';
    controlsContainer.style.zIndex = '1000';
    controlsContainer.style.display = 'flex';
    controlsContainer.style.gap = '8px';

    map.getContainer().appendChild(controlsContainer);
}

// ===================== INITIALISATION GEOLOCALISATION =========================

// Quand la page se charge, on tente d'obtenir la position de l'utilisateur
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        // Succès : centre la carte sur l'utilisateur
        userCoords = [position.coords.latitude, position.coords.longitude];
        map = L.map('map', {zoomControl: false, attributionControl: false}).setView(userCoords, 14);
        L.tileLayer('https://api.maptiler.com/maps/basic-v2/{z}/{x}/{y}@2x.png?key=1XPmmAxswHqtzHfGMCGh', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &amp; <a href="https://www.maptiler.com/copyright/">MapTiler</a>',
            maxZoom: 20
        }).addTo(map);
        setUserCircle(userCoords[0], userCoords[1]);
        addMarkers(etablissements);
        addCustomControls();
    }, function() {
        // Échec : carte par défaut
        setDefaultMap();
    });
} else {
    // Géoloc non disponible
    setDefaultMap();
}

// ===================== AUTOCOMPLETE BARRE DE RECHERCHE ========================

// Quand on tape dans la barre de recherche
document.getElementById('searchInput').addEventListener('input', function(e) {
    const val = this.value;
    const list = document.getElementById("autocomplete-list");
    list.innerHTML = '';
    const category = document.getElementById('categorySelect').value;
    if (!val) {
        filterEtablissements();
        return;
    }
    // Suggestions selon ce qui est tapé
    const suggestions = etablissements.filter(e =>
        e.nom.toLowerCase().includes(val.toLowerCase()) &&
        (e.categorie === category || !category)
    );
    // Affichage des suggestions
    suggestions.forEach(suggestion => {
        const div = document.createElement('div');
        div.innerHTML = suggestion.nom.replace(new RegExp(val, 'i'), match => `<strong>${match}</strong>`);
        div.addEventListener('click', () => {
            document.getElementById('searchInput').value = suggestion.nom;
            list.innerHTML = '';
            filterEtablissements();
            if (suggestion.latitude && suggestion.longitude) {
                map.setView([suggestion.latitude, suggestion.longitude], 17);
            }
        });
        list.appendChild(div);
    });
    filterEtablissements();
});

// Quand on appuie sur Entrée, ça sélectionne la première suggestion si il y en a une
document.getElementById('searchInput').addEventListener('keydown', function(e) {
    if (e.key === "Enter") {
        const list = document.getElementById("autocomplete-list");
        const firstSuggestion = list.querySelector('div');
        if (firstSuggestion) {
            e.preventDefault();
            firstSuggestion.click();
        }
    }
});

// Quand on clique en dehors de la barre, les suggestions disparaissent
document.addEventListener("click", function(e) {
    if (!e.target.closest("#searchInput")) {
        document.getElementById("autocomplete-list").innerHTML = '';
    }
});

// ========================= FILTRE PAR CATEGORIE ==============================

document.getElementById('categorySelect').addEventListener('change', filterEtablissements);

// ==================== PANEL LATERAL ETABLISSEMENT (AJAX) ======================

// Quand on clique sur un nom d'établissement dans la popup, affiche le panneau latéral AJAX
document.body.addEventListener('click', function(e){
    if(e.target.matches('.etab-link')) {
        e.preventDefault();
        let etabId = e.target.getAttribute('data-id');
        const panel = document.getElementById('side-panel');
        const content = document.getElementById('side-panel-content');
        fetch(`/fiche_etablissement_fragment/${etabId}`)
            .then(resp => resp.text())
            .then(html => {
                content.innerHTML = '<button id="close-panel" class="leaflet-popup-close-button" aria-label="Fermer">×</button>' + html;
                panel.style.display = 'block';
                panel.classList.remove('hide-panel');
                document.body.style.overflow = "hidden";
            });
    }
});

// ======================== FERMETURE DU PANEL LATERAL =========================

// Par bouton ✕
document.body.addEventListener('click', function(e){
    if(e.target.id === "close-panel") {
        closeSidePanel();
    }
});

// Par touche Échap
document.addEventListener('keydown', function(e) {
    if(e.key === "Escape") {
        closeSidePanel();
    }
});

// Fonction de fermeture (avec animation et reset)
function closeSidePanel() {
    const panel = document.getElementById('side-panel');
    const content = document.getElementById('side-panel-content');
    panel.classList.add('hide-panel');
    setTimeout(() => {
        panel.style.display = 'none';
        content.innerHTML = '<button id="close-panel" class="leaflet-popup-close-button" aria-label="Fermer">×</button>';
        panel.classList.remove('hide-panel');
        document.body.style.overflow = "";
    }, 300);
}

// ==================== ANIMATION / ICONE RECHERCHE / CLEAR =====================

// Animation de l'icône loupe selon contenu du champ
const searchInput = document.getElementById('searchInput');
const searchIcon = document.getElementById('searchIcon');

searchInput.addEventListener('input', () => {
    if (searchInput.value.trim() === "") {
        searchIcon.style.opacity = "1";
    } else {
        searchIcon.style.opacity = "0";
    }
});

// ==================== EDITION D'AVIS (OUVERTURE PANEL AJAX) ===================

document.body.addEventListener('click', function(e) {
    if (e.target.closest('.edit-avis-btn')) {
        e.preventDefault();
        const btn = e.target.closest('.edit-avis-btn');
        const url = btn.getAttribute('data-url');
        fetch(url)
            .then(resp => resp.text())
            .then(html => {
                const panel = document.getElementById('side-panel');
                const content = document.getElementById('side-panel-content');
                content.innerHTML = '<button id="close-panel" class="leaflet-popup-close-button" aria-label="Fermer">×</button>' + html;
                panel.style.display = 'block';
                panel.classList.remove('hide-panel');
                document.body.style.overflow = 'hidden';
            });
    }
});

// ==================== BOUTON X POUR VIDER LE CHAMP DE RECHERCHE ===============

(function() {
    const searchInput = document.getElementById('searchInput');
    const searchIcon = document.getElementById('searchIcon');
    const parent = searchInput.parentNode;

    // S'assure que le parent est en position relative
    if (getComputedStyle(parent).position === 'static') {
        parent.style.position = 'relative';
    }

    // Crée le bouton X s'il n'existe pas déjà
    let clearBtn = parent.querySelector('.clear-search-btn');
    if (!clearBtn) {
        clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.innerHTML = '×';
        clearBtn.className = 'clear-search-btn';
        clearBtn.setAttribute('aria-label', 'Effacer');
        clearBtn.style.position = 'absolute';
        clearBtn.style.right = '12px'; // Peut s'ajuster
        clearBtn.style.top = '50%';
        clearBtn.style.transform = 'translateY(-50%)';
        clearBtn.style.background = 'none';
        clearBtn.style.border = 'none';
        clearBtn.style.fontSize = '20px';
        clearBtn.style.cursor = 'pointer';
        clearBtn.style.opacity = '0';
        clearBtn.style.transition = 'opacity 0.15s';
        clearBtn.style.padding = '0';
        clearBtn.style.zIndex = '10';
        clearBtn.style.lineHeight = '1';
        clearBtn.style.pointerEvents = 'none';
        parent.appendChild(clearBtn);
    }

    // Fonction qui affiche le bouton X si champ non vide, sinon cache
    function toggleIcons() {
        if (searchInput.value.trim() !== "") {
            clearBtn.style.opacity = '1';
            clearBtn.style.pointerEvents = 'auto';
            if (searchIcon) searchIcon.style.opacity = '0';
        } else {
            clearBtn.style.opacity = '0';
            clearBtn.style.pointerEvents = 'none';
            if (searchIcon) searchIcon.style.opacity = '1';
        }
    }

    // Quand on clique sur X, on efface et on filtre à nouveau
    clearBtn.addEventListener('click', function(e) {
        e.preventDefault();
        searchInput.value = '';
        toggleIcons();
        filterEtablissements();
        document.getElementById("autocomplete-list").innerHTML = '';
        searchInput.focus();
    });

    // Quand on tape, on affiche/cache le bouton
    searchInput.addEventListener('input', toggleIcons);
    // Initialisation (si champ déjà rempli)
    toggleIcons();
})();