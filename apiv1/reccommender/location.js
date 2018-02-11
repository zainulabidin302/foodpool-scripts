var mysql = require('../mysql');

var getRestaurantsWithRadiusWithinMeters = (data, onResult, onError) => {

    if (!data.lat || !data.lat) 
        return onError({error: 'location is missing'})

    let radius = data.radius || 1;
    let lat = data.lat;
    let lon = data.lon;


    let query = 'SELECT * ,' + `( 6371 * acos( cos( radians(${lat}) ) * cos( radians( lat ) ) * cos( radians( lon ) -` + `radians(${lon}) ) + sin( radians(${lat}) ) * sin( radians(lat) ) ) ) AS distance` + ` FROM restaurants HAVING distance <= ${radius} ORDER BY distance ASC`

    mysql.query(query, (error, result, fields) => {
        if (!error) {
            onResult(result)
        } else {
            onError(error)
        }
    });

}


module.exports = {
    getRestaurantsWithRadiusWithinMeters: getRestaurantsWithRadiusWithinMeters
}