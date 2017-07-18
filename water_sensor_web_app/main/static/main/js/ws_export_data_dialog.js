$(document).ready(() => {
    var exportDataDialog = document.getElementById('export-data-dialog');
    var reservoirsList = document.getElementById('export-data-reservoir-list');
    var fromField = document.getElementById('export-data-dateFrom');
    var untilField = document.getElementById('export-data-dateUntil');
    var dialogCancelBt = document.getElementById('export-data-bt-cancel');
    var dialogCSVBt = document.getElementById('export-data-bt-csv');
    var dialogXLSBt = document.getElementById('export-data-bt-xls');
    var cbCheckAll  = document.getElementById('export-data-reservoir-list-all');
    // reservoirs currently shown in the dialog
    var currentReservoirs = []; 

    /**
     * Called when the export data button is called.
     */
    openExportDataDialog = () => {
        $.get(RESERVOIR_DATA_PATH)
        .done((result) => {
            var jsonRes = JSON.parse(result);

            // remove current children from reservoir list
            reservoirsList.innerHTML = "";
            // clear currentReservoirs list
            for (var r in currentReservoirs)
                currentReservoirs.splice(r, 1);

            for (var r in jsonRes) {
                // create new list element and add to table
                var reservoir = jsonRes[r];
                // check if it is the reservoir that's currently being shown
                var checkedOrUnchecked = 
                    reservoir.res_id == window.reservoir.res_id ? 'checked' : 'unchecked';
                reservoirsList.innerHTML +=
                `<li class="mdl-list__item">
                    <span class="mdl-list__item-primary-content">
                    ${reservoir.town}, ${reservoir.county}, ${reservoir.island}, #${reservoir.res_id}
                    </span>
                    <span class="mdl-list__item-secondary-action">
                    <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" 
                           for="export-data-reservoir-list-${reservoir.res_id}">
                        <input type="checkbox" id="export-data-reservoir-list-${reservoir.res_id}" 
                               class="mdl-checkbox__input" ${checkedOrUnchecked} />
                    </label>
                    </span>
                </li>`;

                currentReservoirs.push(reservoir);
            }

            // show default date from yesterday to today
            var today = new Date();
            var yesterday = new Date(today.getTime() - 25*60*60*1000);
            fromField.value  = moment(yesterday).format('YYYY-MM-DD');
            untilField.value = moment(today).format('YYYY-MM-DD');

            exportDataDialog.showModal();
        })
    }

    /**
     * Downloads the reservoir measurement data
     */
    exportData = (format) => {
        var url = EXPORT_DATA_PATH + "?format=" + format;
        var reservoirsChosen = "";
        var dateFrom = fromField.value;
        var dateUntil = untilField.value;

        if (!moment(dateFrom).isValid() || !moment(dateUntil).isValid()) {
            Util.showMsgDialog('Datas', 'Formato de datas inválido. Utilize o formato mês/dia/ano');
            return;
        }

        url += `&dateFrom=${dateFrom}&dateUntil=${dateUntil}`;

        for (var r in currentReservoirs) {
            var resId = currentReservoirs[r].res_id;
            if (document.getElementById('export-data-reservoir-list-' + resId).checked)
                reservoirsChosen += resId + ",";
        }

        url += "&reservoirs=" + reservoirsChosen.substr(0, reservoirsChosen.length-1);
        var link = document.createElement('a');
        link.href = url;
        link.download = true;
        link.click();
        exportDataDialog.close();
    }

    /**
     * Set the choice to export data of all reservoirs
     */
    checkAll = () => {
        for (var r in currentReservoirs) {
            var resId = currentReservoirs[r].res_id;
            document.getElementById('export-data-reservoir-list-' + resId).checked = cbCheckAll.checked;
        }
        dialogCSVBt.disabled = dialogXLSBt.disabled = !cbCheckAll.checked;
    }

    /* set callbacks for buttons */
    document.getElementById('reservoir-link-export-data').onclick = openExportDataDialog;
    document.getElementById('export-data-bt-cancel').onclick = () => exportDataDialog.close();
    dialogXLSBt.onclick = () => exportData('xls');
    dialogCSVBt.onclick = () => exportData('csv');
    cbCheckAll.onchange = checkAll;
})