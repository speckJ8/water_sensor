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
        for (var i = 0; i < window.reservoirs.length; i++)
            addReservoirToMap(window.reservoirs[i]);
    }

    /**
     * Add a marker to a reservoir location in the map
     * @param {object} reservoirData should contain the location and address name of the reservoir
     */
    window.addReservoirToMap = (reservoirData) => {
        console.log('adding ' + reservoirData.address + ' to map');
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
     * Removes all current reservoir locations from the map
     */
    window.removeReservoirLocations = () => {
        var i = window.revervoirLocations.length;
        while (i-- >= 0) {
            // remove from map and from array
            window.reservoirLocations[i].setMap(null);
            window.reservoirLocations.splice(i, 1);
        }
    }
    
})();