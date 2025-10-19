exports.getAvailability = (req, res, next) => {
    var features = {
        colours: req.place.colours,
        flags: req.place.config.pixelFlags || []
    }
    if(req.user) features.user = req.user.getFeatureAvailability();
    res.json({
        success: true,
        availability: features
    });
}