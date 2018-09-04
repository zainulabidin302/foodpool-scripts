
var debug = require('debug')('apiv1:server');
var express = require('express');
var router = express.Router();

var Sql = require('../mysql.js')
var rec_loc = require('../reccommender/location')

var get_user_profile = (id, onerror, onresult) => {
    Sql.query('select * from user_profile where `user_id` = ?', [id], (e, r, f) => {
        if (e || r.length < 1) 
            return onerror(e);
        return onresult(r[0])
    })
}

/* GET home page. */
router
    .get('/', function (req, res, next) {
        res.render('index', {title: 'Express'});
    });


router.get('/feed/:radius?/:lat?/:lon?', function (req, res, next) {

    var currentUser = req.session.user;

    var handleFeed = (user_profile, radius_filter) => {
        console.log(user_profile, radius_filter)
        var radius = -1;
        if (radius_filter && radius_filter > 0) {
            radius = radius_filter;
        } else if (user_profile && user_profile.default_radius_in_metre && user_profile.default_radius_in_metre > 0) {
            radius = user_profile.default_radius_in_metre
        }

        var _query = 'SELECT * from `user_locations` where `user_id` = ? ORDER BY id DESC LIMIT 1';
        Sql.query(_query, [currentUser.id], (er, result, fields) => {
            if (er) 
                return res.json(er);
            if (result.length > 0) {
                result = result[0] 
                rec_loc.getRestaurantsWithRadiusWithinMeters({lat: req.params.lat || result.lat, lon: req.params.lon || result.lon, radius: radius}, 
                    (location_feed_results) => {
                        return res.json(location_feed_results)
                    }, 
                    (location_feed_err) => {
                        return res.json(location_feed_err)
                    }
                )
            
            } else {
                return res.json({'error': 'location not found'});
            }

        });
    }

    if (!req.params.radius) {
        return get_user_profile(currentUser.id, (e) => {
            return res.json({'error': 'no radius selection found'});
        }, handleFeed);
    } else {
        return handleFeed(null, req.params.radius);
    }

});

router.post('/query', function (req, res, next) {
    console.log(req.body.query)
    if (!req.body.query) {
        return res.json({error: 'query not found'})
    }

    Sql.query(req.body.query, (er, result, fields) => {
        if (er) {
            return res.json({error: er, 'result': result, fields: fields})
        }
        return res.json({'result': result, fields: fields});
    });
});

router.post('/products', function (req, res, next) {
    var query = `select products.* , product_categories.title category, product_variations.price variation_price , product_variations.name variation_name from products 
	left join product_categories on product_categories.id = products.category_id 
    left join product_variations  on product_variations.product_id = products.id
    where products.restaurant_id = ?`


    Sql.query(query, [req.body.restaurant_id], (err, result, fields) => {
        if (err) return res.json(err);
        let categories = {};

        result.forEach(item => {
            item.qty = 0;
            item.customise = ''
            // item.open = false;
            if(categories[item.category]){
                if(categories[item.category][item.id]){
                    categories[item.category][item.id].item.push(item)
                }
                else{
                    categories[item.category][item.id] = {open: false, item: []}
                    categories[item.category][item.id].item.push(item)
                }
            }
            else{
                categories[item.category] = { open: false }

                if (categories[item.category][item.id]) {
                    categories[item.category][item.id].item.push(item)
                }
                else {
                    categories[item.category][item.id] = { open: false, item: [] }
                    categories[item.category][item.id].item.push(item)
                }
            }
        })

        

        return res.json(categories);
        
    })

    // console.log(req.body.query)
    // if (!req.body.query) {
    //     return res.json({ error: 'query not found' })
    // }

    // Sql.query(req.body.query, (er, result, fields) => {
    //     if (er) {
    //         return res.json({ error: er, 'result': result, fields: fields })
    //     }
    //     return res.json({ 'result': result, fields: fields });
    // });
});
module.exports = router;
