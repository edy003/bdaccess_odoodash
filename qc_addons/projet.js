/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;
const { useState, onMounted, onWillUnmount, useRef } = owl.hooks;

export class ProjectManagementDashboard extends Component {
    setup() {
        console.log("Initialisation du composant ProjectManagementDashboard");

        // ===== ÉTAT PRINCIPAL =====
        this.state = useState({
            loading: false,
            error: null,

            // Filtres
            selectedProjectType: "",
            selectedPartnerId: "",
            selectedProjectManagerId: "",
            selectedDepartmentId: "",

            // Listes déroulantes
            projectTypes: [],
            availablePartners: [],
            availableProjectManagers: [],
            availableDepartments: [],

            // KPI
            totalProjects: '--',
            totalDueProjects: '--',
            totalLateProjects: '--',
            totalDepartments: '--',

            // Graphiques
            chartData: {
                projectTypeDistribution: { labels: [], values: [] },
                projectsByDepartment: { labels: [], values: [] },
                projectsByManager: { labels: [], values: [] },
                // projectsByDepartment: { labels: [], values: [] },
            },

            // Tableau
            tableData: [],
        });

        // ===== SERVICES =====
        this.rpc = useService("rpc");
        this.orm = useService("orm");
        this.action = useService("action");
        this.user = useService("user");

        // ===== REFS POUR GRAPHIQUES =====
        this.projectTypeDistributionChartRef = useRef("project-type-distribution-chart");
        this.projectsByDepartmentChartRef = useRef("projects-by-department-chart");
        this.projectsByManagerChartRef = useRef("projects-by-manager-chart");
         this.datatableContainerRef = useRef("datatable-container");
        this.dataTable = null;
        // this.projectStatusChartRef = useRef("project-status-chart");
        // this.projectDepartmentChartRef = useRef("project-department-chart");
        // this.gridRef = useRef("projects-grid");
        
        // ===== GRID VARIABLES =====
        // this.gridApi = null;
        // this.gridColumnApi = null;
        // this.gridInitialized = false;
        // this.gridInstance = null;

        // ===== HOOKS =====
        onMounted(async () => {
            await this.loadInitialData();
            // setTimeout(() => {
            //     this.initializeGrid();
            // }, 100);
        });

    onWillUnmount(() => {
            console.log("🧹 Nettoyage DataTable");
            this.destroyDataTable();
        });

        // onWillUnmount(() => {
        //     this.destroyGrid();
        // });
    }

    // ===== CHARGEMENT INITIAL =====
    async loadInitialData() {
        this.state.loading = true;
        try {
            // Charger les listes de filtres en parallèle
            await Promise.all([
                this.loadProjectTypes(),
                this.loadPartners(),
                this.loadProjectManagers(),
                this.loadDepartments(),
            ]);

            // Charger toutes les données (KPI + graphiques + tableau)
            await this.loadAllData();

        } catch (error) {
            console.error("Erreur lors du chargement initial:", error);
            this.state.error = error.message;
        } finally {
            this.state.loading = false;
        }
    }

    // ===== CHARGEMENT DE TOUTES LES DONNÉES =====
    async loadAllData() {
        const params = this.getFilterParams();
        
        try {
            await Promise.all([
                this.loadKPIData(params), 
                this.loadChartData(params),
                this.loadTableData(params),
                // this.loadTableData(params)
            ]);
            this.renderCharts();
            // this.updateGridData();
        } catch (error) {
            console.error("Erreur lors du chargement des données:", error);
            throw error;
        }
    }

    // ===== HELPER : Récupérer les paramètres de filtres =====
    getFilterParams() {
        let departmentIds = null;
        if (this.state.selectedDepartmentId && this.state.selectedDepartmentId !== "") {
            departmentIds = [parseInt(this.state.selectedDepartmentId)];
        }

        return {
            project_type: this.state.selectedProjectType || null,
            partner_id: this.state.selectedPartnerId || null,
            project_manager_id: this.state.selectedProjectManagerId || null,
            department_ids: departmentIds,
        };
    }

    // ===== CHARGEMENT DES KPI =====
    async loadKPIData(params) {
        try {
            const [
                projectCountResponse,
                projectsDueResponse,
                projectsLateResponse,
                departmentsCountResponse
            ] = await Promise.all([
                this.rpc('/dashboard/project_count', params),
                this.rpc('/dashboard/projects_due', params),
                this.rpc('/dashboard/projects_late', params),
                this.rpc('/dashboard/departments_count', params),
            ]);

            // Mise à jour des KPI
            this.state.totalProjects = projectCountResponse.error ? '--' : projectCountResponse.total_projects;
            this.state.totalDueProjects = projectsDueResponse.error ? '--' : projectsDueResponse.total_projects;
            this.state.totalLateProjects = projectsLateResponse.error ? '--' : projectsLateResponse.total_projects;
            this.state.totalDepartments = departmentsCountResponse.error ? '--' : departmentsCountResponse.total_departments;

            console.log("✅ KPI chargés avec succès");
        } catch (error) {
            console.error("Erreur lors du chargement des KPI:", error);
            this.state.totalProjects = '--';
            this.state.totalDueProjects = '--';
            this.state.totalLateProjects = '--';
            this.state.totalDepartments = '--';
        }
    }

    // ===== CHARGEMENT DES GRAPHIQUES =====
    async loadChartData(params) {
        try {
            await Promise.all([
                this.loadProjectTypeDistributionChart(params),
                this.loadProjectsByDepartmentChart(params),
                this.loadProjectsByManagerChart(params),
                // this.loadProjectStatusChart(params),
                // this.loadProjectDepartmentChart(params),
            ]);
        } catch (error) {
            console.error("Erreur lors du chargement des données graphiques:", error);
            this.state.chartData = {
                projectTypeDistribution: { labels: [], values: [] },
                // projectsByStatus: { labels: [], values: [] },
                // projectsByDepartment: { labels: [], values: [] },
            };
        }
    }

   async loadProjectTypeDistributionChart(params) {
    try {
        console.log("Appel RPC vers /dashboard/project_type_distribution avec params:", params);
        
        const result = await this.rpc("/dashboard/project_type_distribution", params);

        // CETTE LIGNE EST LA PLUS IMPORTANTE DE TA VIE ACTUELLEMENT
        console.log("RÉPONSE COMPLÈTE DE L'ENDPOINT :", result);

        if (result.error) {
            console.error("Erreur endpoint :", result.message);
            this.state.chartData.projectTypeDistribution = { labels: [], values: [] };
            return;
        }

        // Si tu vois "undefined" ici → ton Python ne renvoie pas chart_data
        console.log("chart_data reçu :", result.chart_data);

        if (!result.chart_data) {
            console.warn("chart_data est manquant ! L'endpoint ne renvoie pas le bon format");
            this.state.chartData.projectTypeDistribution = { labels: [], values: [] };
            return;
        }

        this.state.chartData.projectTypeDistribution = result.chart_data;
        console.log("Données bien chargées →", this.state.chartData.projectTypeDistribution);

    } catch (error) {
        console.error("Exception RPC :", error);
        this.state.chartData.projectTypeDistribution = { labels: [], values: [] };
    }
}

async loadProjectsByDepartmentChart(params) {
    try {
        const result = await this.rpc("/dashboard/projects_by_department", params);
        if (result.error || !result.chart_data) {
            this.state.chartData.projectsByDepartment = { labels: [], values: [] };
            return;
        }
        this.state.chartData.projectsByDepartment = result.chart_data;
        console.log("Données projets par département chargées :", result.chart_data);
    } catch (error) {
        console.error("Erreur chargement projets par département :", error);
        this.state.chartData.projectsByDepartment = { labels: [], values: [] };
    }
}

async loadProjectsByManagerChart(params) {
    try {
        const result = await this.rpc("/dashboard/projects_by_manager", params);
        if (result.error || !result.chart_data) {
            this.state.chartData.projectsByManager = { labels: [], values: [] };
            return;
        }
        this.state.chartData.projectsByManager = result.chart_data;
        console.log("Données projets par manager chargées :", result.chart_data);
    } catch (error) {
        console.error("Erreur chargement projets par manager :", error);
        this.state.chartData.projectsByManager = { labels: [], values: [] };
    }
}
// async loadTableData(params) {
//     this.state.loading = true;

//     // DONNÉES DE TEST 100% IDENTIQUES À TON FORMAT RÉEL
//     this.state.tableData = [
//         {
//             id: 101,
//             name: "Construction Hôpital Casablanca",
//             project_type: "Externe",
//             partner_name: "Hôpital Central Casablanca",
//             user_name: "Ahmed Benali",
//             project_assistant_name: "Fatima Zahra",
//             practice_name: "Santé",
//             subcategories: "Chirurgie, Urgences, Pédiatrie"
//         },
//         {
//             id: 102,
//             name: "Refonte SI Interne QC",
//             project_type: "Interne",
//             partner_name: "N/A",
//             user_name: "Sophie Martin",
//             project_assistant_name: "N/A",
//             practice_name: "IT & Digital",
//             subcategories: "ERP, CRM"
//         },
//         {
//             id: 103,
//             name: "Audit Banque Al Maghrib",
//             project_type: "Externe",
//             partner_name: "Banque Al Maghrib",
//             user_name: "Karim El Amrani",
//             project_assistant_name: "Amina Khalil",
//             practice_name: "Finance",
//             subcategories: "Risque, Conformité"
//         },
//         {
//             id: 104,
//             name: "Formation continue 2025",
//             project_type: "Interne",
//             partner_name: "N/A",
//             user_name: "Nadia Slimani",
//             project_assistant_name: "Youssef Rami",
//             practice_name: "Ressources Humaines",
//             subcategories: "Leadership, Soft Skills"
//         }
//     ];

//     console.log("Données mockées chargées :", this.state.tableData);

//     // Petit délai pour simuler le RPC
//     await new Promise(r => setTimeout(r, 600));

//     // ON EST SÛR QUE LE DOM EST PRÊT
//     await this.env.isReady;
//     await new Promise(r => requestAnimationFrame(r));

//     this.initializeDataTable();

//     this.state.loading = false;
// }
async loadTableData(params) {
        try {
            console.log("📥 Chargement tableau...");

            const response = await this.rpc("/dashboard/projects_table", params || {});
            const result = response?.result ?? response;

            if (result?.error) {
                console.error("❌ Erreur backend:", result.message);
                this.state.tableData = [];
            } else if (result?.data && Array.isArray(result.data)) {
                this.state.tableData = result.data;
                console.log(`✅ ${result.data.length} projets chargés`);
            } else {
                console.warn("⚠️ Format invalide:", result);
                this.state.tableData = [];
            }

            // ✅ Attendre que le DOM soit stable
            await new Promise(resolve => setTimeout(resolve, 200));

            // ✅ Initialiser DataTable
            this.initializeDataTable();

        } catch (err) {
            console.error("❌ Erreur RPC:", err);
            this.state.tableData = [];
        }
    }


    // ===== CHARGEMENT DES DONNÉES DU TABLEAU =====
    // async loadTableData(params) {
    //     try {
    //         console.log("Chargement des données du tableau...");
    //         const result = await this.rpc("/dashboard/projects_grid", params);
    //         if (result.error) {
    //             console.error("Erreur lors du chargement du tableau:", result.message);
    //             this.state.tableData = [];
    //         } else {
    //             this.state.tableData = result.data || [];
    //             console.log("Données du tableau chargées:", result.data.length, "lignes");
    //         }
    //     } catch (error) {
    //         console.error("Erreur lors du chargement du tableau:", error);
    //         this.state.tableData = [];
    //     }
    // }

    // ===== CHARGEMENT DES LISTES DE FILTRES =====
    async loadProjectTypes() {
        try {
            const response = await this.rpc('/dashboard/project_types', {});
            if (!response.error) {
                this.state.projectTypes = response.project_types || [];
                console.log("Types de projets chargés:", this.state.projectTypes);
            }
        } catch (error) {
            console.error("Erreur types de projets:", error);
        }
    }

    async loadPartners() {
        try {
            const response = await this.rpc('/dashboard/partners', {});
            if (!response.error) {
                this.state.availablePartners = response.partners || [];
                console.log("Partenaires chargés:", this.state.availablePartners);
            }
        } catch (error) {
            console.error("Erreur partenaires:", error);
        }
    }

    async loadProjectManagers() {
        try {
            const response = await this.rpc('/dashboard/project_managers', {});
            if (!response.error) {
                this.state.availableProjectManagers = response.managers || [];
                console.log("Chefs de projet chargés:", this.state.availableProjectManagers);
            }
        } catch (error) {
            console.error("Erreur chefs de projet:", error);
        }
    }

    async loadDepartments() {
        try {
            const departments = await this.orm.searchRead(
                "hr.department",
                [],
                ["id", "name"]
            );
            this.state.availableDepartments = departments;
            console.log("Départements chargés:", this.state.availableDepartments);
        } catch (error) {
            console.error("Erreur départements:", error);
        }
    }

    // ===== RENDU DES GRAPHIQUES =====
    renderCharts() {
        console.log("📊 Rendu des graphiques");
        this.renderProjectTypeDistributionChart();
        this.renderProjectsByDepartmentChart();
        this.renderProjectsByManagerChart();
        // this.renderProjectStatusChart();
        // this.renderProjectDepartmentChart();
    }


    renderProjectTypeDistributionChart() {
        console.log("Tentative de rendu du pie chart types de projets...", {
            chartRef: this.projectTypeDistributionChartRef.el,
            hasData: this.state.chartData.projectTypeDistribution.labels?.length > 0,
            data: this.state.chartData.projectTypeDistribution
        });

        if (!this.projectTypeDistributionChartRef.el) {
            console.warn("Élément DOM du pie chart types de projets introuvable");
            return;
        }

        if (!this.state.chartData.projectTypeDistribution.labels?.length) {
            console.warn("Aucune donnée pour le pie chart types de projets");
            this.projectTypeDistributionChartRef.el.innerHTML = 
                '<div class="text-center p-4 text-gray-500">Aucune donnée à afficher pour les filtres sélectionnés</div>';
            return;
        }

        // Nettoyage propre de l'ancien graphique
        if (typeof Plotly !== 'undefined') {
            try {
                Plotly.purge(this.projectTypeDistributionChartRef.el);
            } catch (e) {
                console.warn("Erreur lors du nettoyage Plotly:", e);
            }
        }
        this.projectTypeDistributionChartRef.el.innerHTML = '';

        if (typeof Plotly === 'undefined') {
            console.warn("Plotly non disponible");
            return;
        }

        try {
            // ✅ Mapping des labels techniques vers labels français
            const labelMap = {
                'internal': 'Projets Internes',
                'external': 'Projets Externes',
                'Non défini': 'Non défini'
            };

            // ✅ Traduire les labels
            const translatedLabels = this.state.chartData.projectTypeDistribution.labels.map(
                label => labelMap[label] || label
            );

            // Mapping des couleurs par type de projet
            const colorMap = {
                'internal': '#3B82F6',        // Bleu vif (projets internes)
                'external': '#10B981',        // Vert émeraude (projets externes)
                'Non défini': '#9CA3AF',      // Gris
            };

            // Génère les couleurs dans le bon ordre (basé sur les labels ORIGINAUX)
            const colors = this.state.chartData.projectTypeDistribution.labels.map(
                label => colorMap[label.trim()] || '#9CA3AF'
            );

            const data = [{
                values: this.state.chartData.projectTypeDistribution.values,
                labels: translatedLabels,  // ✅ Utiliser les labels traduits
                type: 'pie',
                hole: 0.4,
                marker: {
                    colors: colors
                },
                textinfo: 'label+percent',
                textposition: 'none',
                hovertemplate: '<b>%{label}</b><br>' +
                              'Nombre de projets: %{value}<br>' +
                              'Pourcentage: %{percent}<br>' +
                              '<extra></extra>'
            }];

            const layout = {
                paper_bgcolor: '#FFFFFF',
                plot_bgcolor: '#FFFFFF',
                margin: { t: 0, r: 0, b: 0, l: 0 },
                showlegend: true,
                legend: {
                    orientation: "v",
                    yanchor: "middle",
                    y: 0.5,
                    xanchor: "left",
                    x: 1.05,
                    font: { size: 12 }
                },
                font: { family: 'Inter, sans-serif' }
            };

            const config = {
                displayModeBar: false,
                displaylogo: false,
                responsive: true
            };

            Plotly.newPlot(this.projectTypeDistributionChartRef.el, data, layout, config);

            console.log("✅ Pie chart types de projets rendu avec succès");

        } catch (error) {
            console.error("❌ Erreur lors du rendu du pie chart types de projets:", error);
        }
    }

renderProjectsByDepartmentChart() {
    console.log("Rendu du bar chart horizontal (barh) départements...");

    if (!this.projectsByDepartmentChartRef.el) {
        console.warn("Élément DOM du bar chart départements introuvable");
        return;
    }

    // Nettoyage
    if (typeof Plotly !== 'undefined') {
        try { Plotly.purge(this.projectsByDepartmentChartRef.el); } catch (e) {}
    }
    this.projectsByDepartmentChartRef.el.innerHTML = '';

    if (!this.state.chartData.projectsByDepartment.labels?.length) {
        this.projectsByDepartmentChartRef.el.innerHTML = 
            '<div class="text-center p-4 text-gray-500">Aucune donnée à afficher pour les filtres sélectionnés</div>';
        return;
    }

    if (typeof Plotly === 'undefined') return;

    try {
        // Tri décroissant (département avec le + de projets en haut)
        const sorted = this.state.chartData.projectsByDepartment.labels
            .map((label, i) => ({ label, value: this.state.chartData.projectsByDepartment.values[i] }))
            .sort((a, b) => b.value - a.value);

        const sortedLabels = sorted.map(item => item.label);
        const sortedValues = sorted.map(item => item.value);

        const data = [{
            y: sortedLabels,           // ← les noms sur l'axe Y (vertical)
            x: sortedValues,           // ← les valeurs sur l'axe X (horizontal)
            type: 'bar',
            orientation: 'h',          // ← BAR HORIZONTAL
            marker: { 
                color: '#3B82F6',
                line: { width: 1, color: '#2563eb' }
            },
            text: sortedValues.map(String),
            textposition: 'outside',
            hovertemplate: '<b>%{y}</b><br>Nombre de projets: <b>%{x}</b><extra></extra>',
            textfont: { size: 12 }
        }];

        const layout = {
            paper_bgcolor: '#FFFFFF',
            plot_bgcolor: '#FFFFFF',
            margin: { t: 0, r: 0, b: 0, l: 0 },  // ← beaucoup de place à gauche pour les longs noms
            xaxis: { 
                title: 'Nombre de projets',
                gridcolor: '#f0f0f0',
                zeroline: false
            },
            yaxis: { 
                automargin: true,
                tickfont: { size: 11.5 },
                title: null
            },
            font: { family: 'Inter, sans-serif' },
            hovermode: 'closest',
            bargap: 0.35
        };

        const config = {
            displayModeBar: false,
            displaylogo: false,
            responsive: true
        };

        Plotly.newPlot(this.projectsByDepartmentChartRef.el, data, layout, config);


        console.log("Bar chart HORIZONTAL (barh) projets par département → RENDU PARFAIT");
    } catch (error) {
        console.error("Erreur rendu barh départements:", error);
    }
}

renderProjectsByManagerChart() {
    console.log("Rendu du bar chart vertical (croissant) project managers...");

    if (!this.projectsByManagerChartRef.el) {
        console.warn("Élément DOM du bar chart managers introuvable");
        return;
    }

    // Nettoyage
    if (typeof Plotly !== 'undefined') {
        try { Plotly.purge(this.projectsByManagerChartRef.el); } catch (e) {}
    }
    this.projectsByManagerChartRef.el.innerHTML = '';

    if (!this.state.chartData.projectsByManager.labels?.length) {
        this.projectsByManagerChartRef.el.innerHTML = 
            '<div class="text-center p-4 text-gray-500">Aucune donnée à afficher pour les filtres sélectionnés</div>';
        return;
    }

    if (typeof Plotly === 'undefined') return;

    try {
        // Tri CROISSANT (manager avec le moins de projets à gauche)
        const sorted = this.state.chartData.projectsByManager.labels
            .map((label, i) => ({ label, value: this.state.chartData.projectsByManager.values[i] }))
            .sort((a, b) => a.value - b.value);  // ← CROISSANT

        const sortedLabels = sorted.map(item => item.label);
        const sortedValues = sorted.map(item => item.value);

        const data = [{
            x: sortedLabels,           // ← Noms des managers sur l'axe X
            y: sortedValues,           // ← Valeurs sur l'axe Y
            type: 'bar',
            orientation: 'v',          // ← BAR VERTICAL
            marker: { 
                color: '#10B981',      // Vert émeraude
                line: { width: 1, color: '#059669' }
            },
            text: sortedValues.map(String),
            textposition: 'outside',
            hovertemplate: '<b>%{x}</b><br>Nombre de projets: <b>%{y}</b><extra></extra>',
            textfont: { size: 12 }
        }];

        const layout = {
            paper_bgcolor: '#FFFFFF',
            plot_bgcolor: '#FFFFFF',
            margin: { t: 0, r: 0, b: 0, l: 0 },  // ← Plus d'espace en bas pour les labels
            xaxis: { 
                title: null,
            // ← Rotation des noms pour lisibilité
                tickfont: { size: 11 },
                automargin: true
            },
            yaxis: { 
                title: 'Nombre de projets',
                gridcolor: '#f0f0f0',
                zeroline: false
            },
            font: { family: 'Inter, sans-serif' },
            hovermode: 'closest',
            bargap: 0.2
        };

        const config = {
            displayModeBar: false,
            displaylogo: false,
            responsive: true
        };

        Plotly.newPlot(this.projectsByManagerChartRef.el, data, layout, config);

        console.log("✅ Bar chart VERTICAL CROISSANT project managers rendu avec succès");
    } catch (error) {
        console.error("❌ Erreur rendu bar chart managers:", error);
    }
}
    // ===== GESTION DU TABLEAU (AG-GRID) =====
// 
initializeDataTable() {
        console.log("🔧 Initialisation DataTable");

        // ✅ 1. Récupérer le conteneur
        const container = this.datatableContainerRef.el;
        
        if (!container) {
            console.error("❌ Conteneur introuvable !");
            return;
        }

        // ✅ 2. Détruire l'ancienne instance
        this.destroyDataTable();

        // ✅ 3. Injecter le HTML du tableau
        container.innerHTML = `
            <table id="projects_datatable" class="table table-striped table-hover table-bordered nowrap" style="width:100%">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Projet</th>
                        <th>Type</th>
                        <th>Client</th>
                        <th>Manager</th>
                        <th>Assistant</th>
                        <th>Practice</th>
                        <th>Sous-catégories</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        `;

        // ✅ 4. Attendre la stabilisation du DOM
        setTimeout(() => {
            const $table = $('#projects_datatable');

            if (!$table.length) {
                console.error("❌ Table non trouvée après injection");
                return;
            }

            // ✅ 5. Créer DataTable
            try {
                this.dataTable = $table.DataTable({
                    data: this.state.tableData,
                    pageLength: 25,
                    lengthChange: true,
                    lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
                    responsive: true,
                    // language: {
                    //     url: "//cdn.datatables.net/plug-ins/2.0.0/i18n/fr-FR.json"
                    // },
                    order: [[0, "asc"]],
                    columns: [
                        { 
                            data: "id", 
                            className: "text-center fw-bold", 
                            width: "60px" 
                        },
                        { 
                            data: "name", 
                            render: d => `<strong>${d || ''}</strong>` 
                        },
                        {
                            data: "project_type",
                            width: "120px",
                            render: d => {
                                if (!d || d === "Non défini") {
                                    return `<span class="badge bg-secondary">Non défini</span>`;
                                }
                                const lower = d.toString().toLowerCase();
                                return lower.includes("externe") || lower.includes("external")
                                    ? `<span class="badge bg-success">${d}</span>`
                                    : `<span class="badge bg-primary">${d}</span>`;
                            }
                        },
                        { data: "partner_name", defaultContent: "N/A" },
                        { data: "user_name", defaultContent: "Non assigné" },
                        { data: "project_assistant_name", defaultContent: "N/A" },
                        { data: "practice_name", defaultContent: "N/A" },
                        { data: "subcategories", defaultContent: "N/A" },
                    ]
                });

                console.log("✅✅✅ DataTable créée avec succès !");

            } catch (error) {
                console.error("❌ Erreur création DataTable:", error);
            }
        }, 100);
    }


    updateGridData() {
  
    }

    reinitializeGrid() {
    }

    destroyDataTable() {
        if (this.dataTable) {
            try {
                this.dataTable.destroy();
                this.dataTable = null;
                console.log("♻️ DataTable détruite");
            } catch (e) {
                console.warn("⚠️ Erreur destruction:", e);
            }
        }
    }

    // ===== GESTIONNAIRES DE FILTRES =====
    onProjectTypeChange(ev) {
        this.state.selectedProjectType = ev.target.value || "";
    }

    onPartnerChange(ev) {
        this.state.selectedPartnerId = ev.target.value || "";
    }

    onProjectManagerChange(ev) {
        this.state.selectedProjectManagerId = ev.target.value || "";
    }

    onDepartmentChange(ev) {
        this.state.selectedDepartmentId = ev.target.value || "";
    }

    // ===== ACTIONS SUR LES FILTRES =====
     async onApplyFilters() {
        console.log("🔄 Application filtres");
        
        try {
            // ✅ On ne met PAS state.loading = true pour ne pas cacher le conteneur
            const params = this.getFilterParams();
            
            await Promise.all([
                this.loadKPIData(params),
                this.loadChartData(params),
                this.loadTableData(params)
            ]);
            
            this.renderCharts();
            
        } catch (error) {
            console.error("❌ Erreur filtres:", error);
        }
    }

    async onResetFilters() {
        console.log("🔄 Réinitialisation des filtres");
        this.state.selectedProjectType = "";
        this.state.selectedPartnerId = "";
        this.state.selectedProjectManagerId = "";
        this.state.selectedDepartmentId = "";
        await this.onApplyFilters();
    }

    // ===== HELPERS =====
    formatValue(value) {
        if (value === '--' || value === null || value === undefined) return '--';
        return value.toString();
    }
}

ProjectManagementDashboard.template = "qc_dashboard.ProjectManagementDashboard";
registry.category('actions').add('qc_dashboard.action_project_management_dashboard', ProjectManagementDashboard);