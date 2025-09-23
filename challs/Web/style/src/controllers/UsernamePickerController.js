const fs = require("fs");

exports.postUsername = (req, res, next) => {
    function renderResponse(errorMsg) {
        return req.responseFactory.sendRenderedResponse("public/pick-username", { captcha: req.place.enableCaptcha, error: { message: errorMsg || "An unknown error occurred" }, username: req.body.username, user: {name: ""} });
    }
    if(req.user.usernameSet) res.redirect("/");
    
    // Check if we can actually do this
    const config = req.place.config;
    if (config.maintenance && !config.maintenance.allowSignups) {
        req.logout();
        return res.redirect(403, "/");
    }
    
    let user = req.user;
    user.name = req.body.username;
    user.setUserName(user.name, function(err) {
        if(err) return renderResponse(err.message);
        req.login(user, function(err) {
            if (err) {
                req.place.reportError("Unknown user login error.");
                return renderResponse("An unknown error occurred.");
            }
            res.redirect("/?signedin=1");
        });
    });
};
