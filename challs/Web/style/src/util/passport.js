const JwtStrategy = require("passport-jwt").Strategy,
    LocalStrategy = require("passport-local").Strategy,
    ExtractJwt = require("passport-jwt").ExtractJwt;

// Get user model
const User = require("../models/user");
const config = require("../config/config");
const ActionLogger = require("../util/ActionLogger");

module.exports = function(passport, app) {
    var opts = {};
    opts.jwtFromRequest = ExtractJwt.fromAuthHeader();
    opts.secretOrKey = config.secret;
    passport.use(new JwtStrategy(opts, function(jwt_payload, done) {
        User.findOne({ _id: jwt_payload._id }, function(err, user) {
            if (err) return done(err, false);
            if (user) {
                if (user.loginError()) return done(null, false, { error: user.loginError() });                
                return done(null, user);
            }
            done(null, false, { error: { message: "Invalid token.", code: "invalid_token" } });
        });
    }));

    passport.use(new LocalStrategy(function(username, password, done) {
        function rejectCredentials() {
            done(null, false, { error: { message: "Incorrect username or password provided.", code: "invalid_credentials" } });
        }
        User.findByUsername(username, function(err, user) {
            if (err) return done(err, false);
            if (user) {
                if (user.loginError()) return done(null, false, { error: user.loginError() });
              
                if(user.passwordResetKey) {
                    if(user.passwordResetKey == password) return done(null, user);
                } else {
                    return user.comparePassword(password, function(err, match) {
                        if (match && !err) {
                            ActionLogger.log(app, "signIn", user, null, {method: "normal"});
                            return done(null, user);
                        }
                        rejectCredentials();
                    });
                }
            }
            rejectCredentials();
        });
    }));

    passport.serializeUser(function(user, done) {
        done(null, user.id);
    });

    passport.deserializeUser(function(user, done) {
        User.findById(user, (err, user) => done(err, user));
    });
}
