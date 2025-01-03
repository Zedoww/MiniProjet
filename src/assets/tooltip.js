window.dccFunctions = window.dccFunctions || {};
window.dccFunctions.ordinalToDate = function(value) {
    const epoch = new Date(1970, 0, 1); // 1er janv 1970
    const days = value - 719163;        // Décalage Python <-> JS
    epoch.setDate(epoch.getDate() + days);


    const options = { year: 'numeric', month: 'short', day: '2-digit' };
    return epoch.toLocaleDateString('fr-FR', options);
}