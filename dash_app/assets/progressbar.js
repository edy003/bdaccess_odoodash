var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.ProgressBar = function (props) {
    const value = props.value || 0;
    const color = value < 30 ? '#e74c3c' : value < 70 ? '#f39c12' : '#2ecc71'; // Rouge / Orange / Vert

    return React.createElement(
        'div',
        {
            style: {
                width: '100%',
                backgroundColor: 'White',
                borderRadius: '4px',
                overflow: 'hidden',
            }
        },
        React.createElement(
            'div',
            {
                style: {
                    width: `${value}%`,
                    backgroundColor: color,
                    textAlign: 'center',
                    color: 'white',
                    padding: '2px 0',
                    fontSize: '12px',
                    transition: 'width 0.5s ease',
                }
            },
            `${value}%`
        )
    );
};



dagcomponentfuncs.StatusBadge = function (props) {
    const value = props.value || '';
     

    if (value === 'À Faire') {
        color = '#e67e22'; // orange
    } else if (value === 'En Cours') {
        color = '#3498db'; // bleu
    } else if (value === 'Terminée') {
        color = '#2ecc71'; // vert
    }


    return React.createElement(
        'div',
        {
            style: {
                backgroundColor: color,
                color: 'white',
                borderRadius: '12px',
                display: 'flex',
                textAlign: 'center',
                alignItems: 'center',
                justifyContent: 'center',
                width:'100%',
                height:'100%',
                marginTop:'2px',
                height: 'calc(100% - 2px)',
                marginBottom:'4px',
                // paddingBottom: 4,          
                // paddingTop: 4,
                // fontSize: '12px',
                fontWeight: 'bold',
                // minWidth: '80px',
                // transition: 'background-color 0.3s ease',
            }
        },
        value
    );
};


dagcomponentfuncs.NoteColor = function (props) {
    const value = props.value;

    // Si la valeur est nulle ou vide, on ne retourne rien (la cellule reste vide)
    if (value === null || value === undefined || value === '') {
        return null;
    }


    if (value < 5) {
        color = '#e74c3c'; // rouge
    } else if (value >= 5 && value < 8) {
        color = '#f1c40f'; // jaune
    } else if (value >= 8) {
        color = '#2ecc71'; // vert
    }

    return React.createElement(
        'div',  // on utilise un <div> pour centrer correctement
        {
            style: {
                color: color,
                fontWeight: 'bold',
                fontSize: '18px',
                textAlign: 'center',
                width: '100%',
            }
        },
        value
    );
};



dagcomponentfuncs.StatusBadgesuivi = function (props) {
    const value = props.value || '';
     

    if (value === 'À Faire') {
        color = '#e67e22'; // orange
    } else if (value === 'En Cours') {
        color = '#3498db'; // bleu
    } else if (value === 'Terminée') {
        color = '#2ecc71'; // vert
    }
    else{
        color = '#e74c3c'
    }
    

    return React.createElement(
        'div',
        {
            style: {
                backgroundColor: color,
                color: 'white',
                borderRadius: '12px',
                display: 'flex',
                textAlign: 'center',
                alignItems: 'center',
                justifyContent: 'center',
                width:'100%',
                height:'100%',
                marginTop:'2px',
                height: 'calc(100% - 2px)',
                marginBottom:'4px',
                // paddingBottom: 4,          
                // paddingTop: 4,
                // fontSize: '12px',
                fontWeight: 'bold',
                // minWidth: '80px',
                // transition: 'background-color 0.3s ease',
            }
        },
        value
    );
};
