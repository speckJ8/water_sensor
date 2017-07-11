(() => {

    var locationSantiagoIsland = {lat: 15.082677, lng: -23.6210796}

    /**
     * will load the map into the html page and show
     * the reservoir locations
     */
    window.loadMap = () => {
        window.myMap = new google.maps.Map(document.getElementById('map'), {
            zoom: 11,
            center: locationSantiagoIsland
        });
        window.reservoirLocations = [];
        window.pumpLocations      = [];
        for (var i = 0; i < window.reservoirs.length; i++)
            addReservoirToMap(window.reservoirs[i]);
        for (var i = 0; i < window.pumps.length; i++)
            addPumpToMap(window.pumps[i]);
    }

    /**
     * Add a marker of a reservoir location in the map
     * @param {object} reservoirData should contain the location and address name of the reservoir
     */
    window.addReservoirToMap = (reservoirData) => {
        var marker = new google.maps.Marker({
            position: reservoirData.position,
            title: reservoirData.address,
            map: window.myMap,
            icon: {
                url: window.RESERVOIR_ICON,
                scaledSize: new google.maps.Size(20, 20)
            }
        });
        window.reservoirLocations.push(marker);
    }

    /**
     * Add a marker of a pump location in the map
     * @param {object} pumpData should contain the location and address name of the pump
     */
    window.addPumpToMap = (pumpData) => {
        var marker = new google.maps.Marker({
            position: pumpData.position,
            title: pumpData.address,
            map: window.myMap,
            icon: {
                url: window.PUMP_ICON,
                scaledSize: new google.maps.Size(20, 20)
            }
        });
        window.pumpLocations.push(marker);
    }

    /**
     * Removes all current markers from the map
     */
    window.removeMarkers = () => {
        var i = window.revervoirLocations.length;
        while (i-- >= 0) {
            // remove from map and from array
            window.reservoirLocations[i].setMap(null);
            window.reservoirLocations.splice(i, 1);
        }
        
        i = window.pumpLocations.length;
        while (i-- > 0) {
            // remove from map and from array
            window.pumpLocations[i].setMap(null);
            window.pumpLocations.splice(i, 1);
        }
    }
    
})();