const express = require("express");

const UsernamePickerController = require("../controllers/UsernamePickerController");
const PasswordChangeController = require("../controllers/PasswordChangeController");
const AccountPageController = require("../controllers/AccountPageController");
const AuthController = require("../controllers/AuthController");

function PublicRouter(app) {
    let router = express.Router();

    const requireUser = (req, res, next) => {
        if (!req.user) return res.status(401).redirect("/#signin");
        next();
    }

    router.use(function(req, res, next) {
        if (req.path == "/signout") return next(); // Allow the user to sign out
        if (req.user && req.user.passwordResetKey) {
            if (req.path == "/force-pw-reset" && req.method == "POST") return next(); // Allow the user to POST their new password
            return req.responseFactory.sendRenderedResponse("public/force-pw-reset");
        }
        next();
    });

    router.post("/pick-username", [requireUser, UsernamePickerController.postUsername]);
    router.post("/force-pw-reset", [requireUser, PasswordChangeController.postSelfServeForcedPassword]);

    router.get("/", function(req, res) {
        req.responseFactory.sendRenderedResponse("public/index", { captcha: req.place.enableCaptcha });
    });

    router.get("/deactivated", function(req, res) {
        if (req.user) return res.redirect("/");
        req.responseFactory.sendRenderedResponse("public/deactivated");
    });

    router.get("/deleted", function(req, res) {
        if (req.user) return res.redirect("/");
        req.responseFactory.sendRenderedResponse("public/deleted");
    });

    router.get("/sitemap.xml", function(req, res, next) {
        if (typeof app.config.host === undefined) return next();
        req.responseFactory.sendRenderedResponse("public/sitemap.xml.pug", null, "text/xml");
    });

    router.get("/signin", function(req, res, next) {
        res.redirect("/#signin");
    });

    router.get("/signup", function(req, res, next) {
        res.redirect("/#signup");
    });
    router.get("/signout", [requireUser, AuthController.getSignOut]);

    router.get("/account", [requireUser, AccountPageController.getOwnAccount]);
    router.get("/user/:userID", AccountPageController.getAccountByID);
    router.get("/@:username", AccountPageController.getAccount);

    return router;
}

PublicRouter.prototype = Object.create(PublicRouter.prototype);

module.exports = PublicRouter;
