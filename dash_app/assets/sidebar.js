// // Fichier à placer dans assets/sidebar.js
// document.addEventListener('DOMContentLoaded', function() {
//     // Intercepter les clics sur tous les liens de navigation
//     interceptNavLinks();
    
//     // Attendre que les composants Dash Mantine soient complètement chargés
//     setTimeout(function() {
//         // Sélectionner le bouton burger Mantine et les éléments à animer
//         const burgerButton = document.querySelector('[id="burger-button"]');
//         const sidebar = document.getElementById('sidebar');
//         const spacerCol = document.getElementById('spacer-col');
//         const contentCol = document.getElementById('content-col');
        
//         if (!burgerButton || !sidebar || !spacerCol || !contentCol) {
//             console.error('Un ou plusieurs éléments nécessaires sont manquants');
//             return;
//         }
        
//         // Capture des propriétés de style initiales précises et complètes
//         const initialLayout = {
//             sidebar: {
//                 transform: 'translateX(0)',
//                 width: getComputedStyle(sidebar).width,
//                 position: getComputedStyle(sidebar).position,
//                 left: getComputedStyle(sidebar).left,
//                 top: getComputedStyle(sidebar).top,
//                 zIndex: getComputedStyle(sidebar).zIndex,
//                 backgroundColor: getComputedStyle(sidebar).backgroundColor,
//                 height: getComputedStyle(sidebar).height
//             },
//             spacer: {
//                 width: getComputedStyle(spacerCol).width,
//                 backgroundColor: getComputedStyle(spacerCol).backgroundColor,
//                 marginTop: getComputedStyle(spacerCol).marginTop
//             },
//             content: {
//                 width: getComputedStyle(contentCol).width,
//                 marginLeft: getComputedStyle(contentCol).marginLeft,
//                 marginRight: getComputedStyle(contentCol).marginRight,
//                 className: contentCol.className
//             }
//         };
        
//         // Stocker les mesures Bootstrap importantes
//         const mainRow = sidebar.closest('.row');
//         if (mainRow) {
//             const allCols = mainRow.querySelectorAll('.col, [class*="col-"]');
//             initialLayout.cols = {};
            
//             allCols.forEach((col, index) => {
//                 initialLayout.cols[index] = {
//                     element: col,
//                     width: getComputedStyle(col).width,
//                     flexBasis: getComputedStyle(col).flexBasis,
//                     maxWidth: getComputedStyle(col).maxWidth,
//                     className: col.className
//                 };
//             });
//         }
        
//         // Capturer l'état des graphiques
//         const graphs = document.querySelectorAll('.js-plotly-plot');
//         initialLayout.graphs = {};
//         graphs.forEach((graph, index) => {
//             initialLayout.graphs[index] = {
//                 width: getComputedStyle(graph).width,
//                 height: getComputedStyle(graph).height
//             };
            
//             // Capture le conteneur parent qui pourrait aussi avoir besoin d'être restauré
//             const graphContainer = graph.closest('.dash-graph');
//             if (graphContainer) {
//                 initialLayout.graphs[index].container = {
//                     width: getComputedStyle(graphContainer).width,
//                     height: getComputedStyle(graphContainer).height
//                 };
//             }
//         });
        
//         // Récupérer l'état de la sidebar depuis localStorage
//         let isOpen = localStorage.getItem('sidebarState') !== 'closed';
        
//         // Si un état existe, synchroniser l'affichage
//         if (localStorage.getItem('sidebarState')) {
//             if (!isOpen) {
//                 // Appliquer l'état fermé immédiatement
//                 sidebar.style.transform = 'translateX(-100%)';
//                 spacerCol.style.width = '0';
//                 spacerCol.style.minWidth = '0';
//                 spacerCol.style.maxWidth = '0';
//                 spacerCol.style.flex = '0 0 0';
                
//                 // Ajuster la colonne du spacer
//                 const spacerBootstrapCol = spacerCol.closest('.col, [class*="col-"]');
//                 if (spacerBootstrapCol) {
//                     spacerBootstrapCol.style.width = '0';
//                     spacerBootstrapCol.style.minWidth = '0';
//                     spacerBootstrapCol.style.maxWidth = '0';
//                     spacerBootstrapCol.style.flex = '0 0 0';
//                 }
                
//                 // Préserver et ajuster le contenu
//                 if (!contentCol.hasAttribute('data-original-class')) {
//                     contentCol.setAttribute('data-original-class', contentCol.className);
//                 }
//                 contentCol.style.width = '100%';
//                 contentCol.style.maxWidth = '100%';
//             }
//         }
        
//         // Fonction optimisée pour réinitialiser précisément la disposition
//         const resetLayout = () => {
//             // Réinitialiser la sidebar
//             sidebar.style.transform = 'translateX(0)';
//             sidebar.style.width = initialLayout.sidebar.width;
//             sidebar.style.position = initialLayout.sidebar.position;
//             sidebar.style.left = initialLayout.sidebar.left;
//             sidebar.style.top = initialLayout.sidebar.top;
//             sidebar.style.zIndex = initialLayout.sidebar.zIndex;
//             sidebar.style.backgroundColor = initialLayout.sidebar.backgroundColor;
//             sidebar.style.height = initialLayout.sidebar.height;
            
//             // Réinitialiser le spacer
//             spacerCol.style.width = initialLayout.spacer.width;
//             spacerCol.style.backgroundColor = initialLayout.spacer.backgroundColor;
//             spacerCol.style.marginTop = initialLayout.spacer.marginTop;
//             spacerCol.style.minWidth = '';
//             spacerCol.style.maxWidth = '';
//             spacerCol.style.flex = '';
            
//             // Restaurer la classe d'origine si elle a été sauvegardée
//             if (contentCol.hasAttribute('data-original-class')) {
//                 contentCol.className = contentCol.getAttribute('data-original-class');
//             } else {
//                 contentCol.className = initialLayout.content.className;
//             }
            
//             // Réinitialiser le contenu
//             contentCol.style.width = initialLayout.content.width;
//             contentCol.style.marginLeft = initialLayout.content.marginLeft;
//             contentCol.style.marginRight = initialLayout.content.marginRight;
//             contentCol.style.maxWidth = ''; // Réinitialiser maxWidth
            
//             // Réinitialiser toutes les colonnes Bootstrap capturées
//             if (initialLayout.cols) {
//                 Object.keys(initialLayout.cols).forEach(index => {
//                     const colData = initialLayout.cols[index];
//                     const col = colData.element;
                    
//                     col.style.width = colData.width;
//                     col.style.flexBasis = colData.flexBasis;
//                     col.style.maxWidth = colData.maxWidth;
//                     col.className = colData.className;
//                 });
//             }
            
//             // Forcer le rafraîchissement des graphiques
//             setTimeout(() => {
//                 window.dispatchEvent(new Event('resize'));
                
//                 // Réappliquer les dimensions des graphiques après le redimensionnement
//                 graphs.forEach((graph, index) => {
//                     if (initialLayout.graphs[index]) {
//                         graph.style.width = initialLayout.graphs[index].width;
//                         graph.style.height = initialLayout.graphs[index].height;
                        
//                         // Restaurer également le conteneur du graphique si capturé
//                         const graphContainer = graph.closest('.dash-graph');
//                         if (graphContainer && initialLayout.graphs[index].container) {
//                             graphContainer.style.width = initialLayout.graphs[index].container.width;
//                             graphContainer.style.height = initialLayout.graphs[index].container.height;
//                         }
//                     }
//                 });
//             }, 350);
//         };
        
//         // Fonction pour basculer l'état de la sidebar
//         const toggleSidebar = () => {
//             isOpen = !isOpen;
            
//             if (isOpen) {
//                 // Restaurer l'état initial
//                 resetLayout();
//             } else {
//                 // Fermer la sidebar avec précision
//                 sidebar.style.transform = 'translateX(-100%)';
                
//                 // Ajuster le spacer
//                 spacerCol.style.width = '0';
//                 spacerCol.style.minWidth = '0';
//                 spacerCol.style.maxWidth = '0';
//                 spacerCol.style.flex = '0 0 0';
                
//                 // Trouver la colonne Bootstrap du spacer et l'ajuster également
//                 const spacerBootstrapCol = spacerCol.closest('.col, [class*="col-"]');
//                 if (spacerBootstrapCol) {
//                     spacerBootstrapCol.style.width = '0';
//                     spacerBootstrapCol.style.minWidth = '0';
//                     spacerBootstrapCol.style.maxWidth = '0';
//                     spacerBootstrapCol.style.flex = '0 0 0';
//                 }
                
//                 // Préserver la classe d'origine tout en ajustant la largeur
//                 if (!contentCol.hasAttribute('data-original-class')) {
//                     contentCol.setAttribute('data-original-class', contentCol.className);
//                 }
                
//                 // Ajuster le contenu pour prendre toute la largeur
//                 contentCol.style.width = '100%';
//                 contentCol.style.maxWidth = '100%';
//             }
            
//             // Sauvegarder l'état dans localStorage
//             localStorage.setItem('sidebarState', isOpen ? 'open' : 'closed');
            
//             // Forcer un redimensionnement des graphiques
//             setTimeout(() => {
//                 window.dispatchEvent(new Event('resize'));
//             }, 350);
//         };
        
//         // Nettoyer tout ancien écouteur d'événement
//         burgerButton.removeEventListener('click', toggleSidebar);
        
//         // Ajouter l'événement de clic au bouton burger Mantine
//         burgerButton.addEventListener('click', function(e) {
//             // Empêcher le comportement par défaut du bouton Mantine
//             e.stopPropagation();
            
//             // Basculer la sidebar
//             toggleSidebar();
//         });
        
//         // Redimensionnement de la fenêtre
//         window.addEventListener('resize', () => {
//             // Si la sidebar est ouverte, s'assurer que tout est bien positionné
//             if (isOpen) {
//                 setTimeout(() => {
//                     // Redimensionner les graphiques
//                     graphs.forEach((graph, index) => {
//                         if (initialLayout.graphs[index]) {
//                             // Vérifier si les dimensions sont différentes avant de les réappliquer
//                             if (graph.style.width !== initialLayout.graphs[index].width) {
//                                 graph.style.width = initialLayout.graphs[index].width;
//                             }
//                             if (graph.style.height !== initialLayout.graphs[index].height) {
//                                 graph.style.height = initialLayout.graphs[index].height;
//                             }
//                         }
//                     });
                    
//                     window.dispatchEvent(new Event('resize'));
//                 }, 350);
//             }
//         });
        
//     }, 1000);
// });

// // Fonction pour intercepter tous les liens de navigation
// function interceptNavLinks() {
//     // Attendre un moment pour s'assurer que tous les liens sont chargés
//     setTimeout(() => {
//         // Ciblage spécifique des liens de navigation dans votre app
//         const navLinks = document.querySelectorAll('a[href^="/"], a[href^="./"], a[href^="../"], a[href*="analyse"], a[href*="performance"]');
        
//         navLinks.forEach(link => {
//             link.addEventListener('click', function(e) {
//                 // Ne pas interférer avec les liens externes ou comportant des modificateurs
//                 if (e.ctrlKey || e.metaKey || this.target === '_blank' || this.getAttribute('data-no-reload') === 'true') {
//                     return;
//                 }
                
//                 e.preventDefault();
                
//                 // Sauvegarder l'URL vers laquelle on souhaite naviguer
//                 const targetUrl = this.href;
                
//                 // Ajouter un paramètre de timestamp pour forcer le rechargement
//                 const separator = targetUrl.includes('?') ? '&' : '?';
//                 const reloadUrl = `${targetUrl}${separator}_reload=${Date.now()}`;
                
//                 // Navigation avec rechargement forcé
//                 window.location.href = reloadUrl;
//             });
//         });
//     }, 1500);
    
//     // Observer les changements dans le DOM pour intercepter également les liens ajoutés dynamiquement
//     const observer = new MutationObserver((mutations) => {
//         mutations.forEach((mutation) => {
//             if (mutation.addedNodes && mutation.addedNodes.length > 0) {
//                 for (let i = 0; i < mutation.addedNodes.length; i++) {
//                     const node = mutation.addedNodes[i];
//                     if (node.nodeType === 1) { // ELEMENT_NODE
//                         const links = node.querySelectorAll('a[href^="/"], a[href^="./"], a[href^="../"], a[href*="analyse"], a[href*="performance"]');
//                         links.forEach(link => {
//                             if (!link.hasAttribute('data-intercepted')) {
//                                 link.setAttribute('data-intercepted', 'true');
//                                 link.addEventListener('click', function(e) {
//                                     if (e.ctrlKey || e.metaKey || this.target === '_blank' || this.getAttribute('data-no-reload') === 'true') {
//                                         return;
//                                     }
                                    
//                                     e.preventDefault();
//                                     const targetUrl = this.href;
//                                     const separator = targetUrl.includes('?') ? '&' : '?';
//                                     const reloadUrl = `${targetUrl}${separator}_reload=${Date.now()}`;
//                                     window.location.href = reloadUrl;
//                                 });
//                             }
//                         });
//                     }
//                 }
//             }
//         });
//     });
    
//     observer.observe(document.body, {
//         childList: true,
//         subtree: true
//     });
// }

// // Détecter si nous avons été rechargés via un paramètre _reload et le retirer de l'URL pour la propreté
// document.addEventListener('DOMContentLoaded', function() {
//     const url = new URL(window.location.href);
//     if (url.searchParams.has('_reload')) {
//         url.searchParams.delete('_reload');
//         window.history.replaceState({}, document.title, url.toString());
//     }
// });