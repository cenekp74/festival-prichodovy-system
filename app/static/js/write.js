function restoreFocus(ele) { // funkce na restorovani focusu na input element aby cipovani fungovalo dal i kdyz kliknu jinam
    setTimeout(function() {
        ele.focus()
    }, 50) // musi byt delay aspon par ms jinak to nefunguje nevim proc
}

function downloadJSON(data, filename) {
    let jsonData = JSON.stringify(data, null, 2);
    let blob = new Blob([jsonData], { type: 'application/json' });
    let url = URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

document.addEventListener('DOMContentLoaded', (event) => {
    window.BACKUP = window.confirm("Chcete ukládat lokální zálohy?");
    if (window.BACKUP) {
        window.BACKUP_EACH_N_WRITES = 5; // zalohy se budou ukladat kazdych n prichodu
        window.prichody = [];
        window.inputCount = 0;
    }
});

function onInputChange(ele) { // tuhle funkce vola htmx (viz write.html)
    let inputText = ele.value;
    ele.value = '';
    if (!window.BACKUP) {return} // pokud client rekl ze nechce ukladat zalohy uz nic nedelam
    let timestamp = new Date().toISOString();
    if (inputText) {
        window.prichody.push({ timestamp: timestamp, rfid: inputText });
        window.inputCount++;

        if (window.inputCount >= window.BACKUP_EACH_N_WRITES) {
            downloadJSON(window.prichody, `backup-prichody-${timestamp}.json`);
            window.inputCount = 0;
        }
    }
}
