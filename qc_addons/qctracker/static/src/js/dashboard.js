odoo.define('qctracker.dashboard', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    
    var QCTrackerDashboard = AbstractAction.extend({
        start: function () {
            var self = this;
            
            // Créer l'iframe avec un conteneur approprié
            this.$el.empty().addClass('qctracker_dashboard_container').css({
                'width': '100%',
                'height': '100%',
                'padding': '0',
                'margin': '0',
                'overflow': 'hidden',
                'position': 'relative'
            });
            
            var iframe = $('<iframe>', {
                id: 'dashboard_iframe',
                src: 'http://127.0.0.1:8050/dash/',
                frameborder: '0',
                css: {
                    'width': '100%',
                    'height': '100%',
                    'border': 'none',
                    'display': 'block',
                    'margin': '0',
                    'padding': '0',
                    'background-color': '#ffffff'
                }
            });
            
            this.$el.append(iframe);
            
            // CSS moins agressif qui préserve les menus
            $('<style>')
                .text(`
                    /* Maximiser la zone de contenu tout en préservant le menu principal */
                    .o_content {
                        padding: 0 !important;
                        margin: 0 !important;
                        border: 0 !important;
                        height: calc(100vh - 46px) !important;
                        width: 100% !important;
                        overflow: hidden !important;
                        background-color: #ffffff !important;
                    }
                    
                    /* Supprimer seulement les contrôles spécifiques, pas le menu principal */
                    .o_control_panel, .o_cp_buttons, .o_cp_left, .o_cp_right,
                    .o_form_buttons_view, .o_form_buttons_edit, .breadcrumb {
                        display: none !important;
                    }
                    
                    /* Assurer l'iframe prend tout l'espace */
                    #dashboard_iframe {
                        width: 100% !important;
                        height: 100% !important;
                        border: none !important;
                        margin: 0 !important;
                        padding: 0 !important;
                        background-color: #ffffff !important;
                    }
                    
                    /* Container de l'iframe */
                    .qctracker_dashboard_container {
                        width: 100% !important;
                        height: 100% !important;
                        position: relative !important;
                        overflow: hidden !important;
                    }
                `)
                .appendTo('head');
            
            // Ajustement des dimensions sans position fixed
            function adjustDimensions() {
                var headerHeight = $('.o_main_navbar').outerHeight(true) || 46;
                
                // Ajuster la hauteur du contenu en fonction de la hauteur du menu
                self.$el.parents('.o_content').css({
                    'height': 'calc(100vh - ' + headerHeight + 'px)',
                    'width': '100%'
                });
                
                // S'assurer que l'iframe occupe tout l'espace
                $('#dashboard_iframe').css({
                    'width': '100%',
                    'height': '100%'
                });
            }
            
            // Appliquer les ajustements
            adjustDimensions();
            setTimeout(adjustDimensions, 250);
            
            // Réajuster lors du redimensionnement
            $(window).on('resize', adjustDimensions);
            
            return this._super.apply(this, arguments);
        },
        
        destroy: function () {
            $(window).off('resize');
            this._super.apply(this, arguments);
        },
    });
    
    core.action_registry.add('qctracker.dashboard', QCTrackerDashboard);
    
    return QCTrackerDashboard;
});