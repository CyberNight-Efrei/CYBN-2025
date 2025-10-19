const mongoose = require("mongoose");
mongoose.promise = global.Promise;
const recaptcha = require("express-recaptcha");
const readline = require("readline").createInterface({input: process.stdin, output: process.stdout});
const util = require("util");
const PaintingManager = require("./util/PaintingManager");
const HTTPServer = require("./util/HTTPServer");
const WebsocketServer = require("./util/WebsocketServer");
const ResponseFactory = require("./util/ResponseFactory");
const TemporaryUserInfo = require("./util/TemporaryUserInfo");
const LeaderboardManager = require("./util/LeaderboardManager");
const UserActivityManager = require("./util/UserActivityManager");
const ModuleManager = require("./util/ModuleManager");
const PixelNotificationManager = require("./util/PixelNotificationManager");
const JavaScriptProcessor = require("./util/JavaScriptProcessor");
const User = require("./models/user");
const Pixel = require("./models/pixel");
const font = require("./alphabet.json");
const fs = require("fs");
const path = require("path");

var app = {};

app.logger = require('./util/logger');

app.loadConfig = (path = "./config/config") => {
    delete require.cache[require.resolve(path)];
    var oldConfig = app.config;
    app.config = require(path);
    app.colours = [... new Set((app.config.colours || ["#FFFFFF", "#E4E4E4", "#888888", "#222222", "#FFA7D1", "#E50000", "#E59500", "#A06A42", "#E5D900", "#94E044", "#02BE01", "#00D3DD", "#0083C7", "#0000EA", "#CF6EE4", "#820080"]).map((c) => c.toUpperCase()))];
    if(!app.config.siteName) app.config.siteName = "Place";
    if(!app.config.boardSize) app.config.boardSize = 1600; // default to 1600 if not specified in config
    if(oldConfig && (oldConfig.secret != app.config.secret || oldConfig.database != app.config.database || oldConfig.boardSize != app.config.boardSize)) {
        app.logger.log("Configuration", "We are stopping the Place server because the database URL, secret, and/or board image size has been changed, which will require restarting the entire server.");
        process.exit(0);
    }
    if(oldConfig && (oldConfig.port != app.config.port || oldConfig.onlyListenLocal != app.config.onlyListenLocal)) app.restartServer();
}
app.loadConfig();

app.temporaryUserInfo = TemporaryUserInfo;
app.responseFactory = (req, res) => new ResponseFactory(app, req, res);

app.pixelNotificationManager = new PixelNotificationManager(app);

app.reportError = app.logger.capture;

app.moduleManager = new ModuleManager(app);
app.moduleManager.loadAll();

// Create .place-data folder
app.dataFolder = path.resolve(__dirname, ".place-data");
if (!fs.existsSync(app.dataFolder)) fs.mkdirSync(app.dataFolder);

app.leaderboardManager = LeaderboardManager(app);
app.userActivityController = UserActivityManager(app);

app.enableCaptcha = false;
if(typeof app.config.recaptcha !== "undefined") {
    if(typeof app.config.recaptcha.siteKey !== "undefined" && typeof app.config.recaptcha.secretKey !== "undefined") {
        app.enableCaptcha = app.config.recaptcha.siteKey != "" && app.config.recaptcha.secretKey != "";
    }
}
if(app.enableCaptcha) {
    // Set up reCaptcha
    recaptcha.init(app.config.recaptcha.siteKey, app.config.recaptcha.secretKey);
    app.recaptcha = recaptcha;
}

app.adminMiddleware = (req, res, next) => {
    if(!req.user || !req.user.admin) return res.status(403).redirect("/?admindenied=1");
    next();
};

app.modMiddleware = (req, res, next) => {
    if(!req.user || !(req.user.admin || req.user.moderator)) return res.status(403).redirect("/?moddenied=1");
    next();
};

app.recreateServer = () => {
    app.httpServer = new HTTPServer(app);
    app.server = app.httpServer.httpServer;
    app.websocketServer = new WebsocketServer(app, app.server);
}
app.recreateServer();

mongoose.connect(process.env.DATABASE || app.config.database);

const handlePendingDeletions = () => {
    setInterval(() => {
        const now = new Date();
        User.remove({ deletionDate: { $lte: now } }, function(err, result) {
            if (err) { console.error(err); return }
            if (result.n) app.logger.log('Deleter', `Deleted ${result.n} users.`);
        });
    }, 30 * Math.pow(10, 3));
}

const flag = "CYBN{P1X3LS_4R3_FUN}";
const bait = "CYBN{YOU_WISH}";
const startX = 10;
const startY = 10;
const glyphWidth = 5;
const glyphHeight = 7;
const charSpacing = 1;

const initData = async () => {
    // clear db in case shit was done
    await User.deleteMany({})
    await Pixel.deleteMany({})
    // init default user
    var user = new User();
    user.name = "admin";
    user.password = "lsbgziuhgziudgjoedihgioedhgiuzhgfdzhfidzuyfbgiudzvbgfziubgfziuygfziuygfz";
    user.admin = true;
    user.email = "";
    user.creationDate = new Date();
    user.save().then(() => {
        app.logger.log("Startup", "Default user created successfully.");
        app.logger.log("Startup", "Initializing pixel board with default colour #888888 …");
        const size = app.config.boardSize;
        const batchSize = 10000;
        const editorId = user._id;
        const now = new Date();
        let batch = [];
        let inserted = 0;
        const tasks = [];

        function flush() {
            if (!batch.length) return;
            const toInsert = batch;
            batch = [];
            tasks.push(
                Pixel.insertMany(toInsert, { ordered: false })
                    .then(() => { inserted += toInsert.length; })
                    .catch(err => app.logger.capture("Pixel batch insert error: " + err))
            );
        }

        function buildText(text, ox, oy) {
            const track = new Set();
            for (const ch of text) {
                const g = font[ch] || [
                    ".....",
                    ".....",
                    ".....",
                    ".....",
                    ".....",
                    ".....",
                    "....."
                ];
                for (let gy = 0; gy < glyphHeight; gy++) {
                    const row = g[gy];
                    for (let gx = 0; gx < glyphWidth; gx++) {
                        if (row[gx] === "#") {
                            const px = ox + gx;
                            const py = oy + gy;
                            if (px < size && py < size) {
                                track.add(px + "," + py);
                            }
                        }
                    }
                }
                ox += glyphWidth + charSpacing;
                if (ox >= size) break;
            }
            return track;
        }
        
        const flagged = buildText(flag, startX, startY);
        for (let y = 0; y < size; y++) {
            for (let x = 0; x < size; x++) {
                const bump = flagged.has(x + "," + y);
                batch.push({
                    xPos: x,
                    yPos: y,
                    colourR: bump ? 137 : 136,
                    colourG: 136,
                    colourB: 136,
                    editorID: editorId,
                    lastModified: now
                });
                if (batch.length === batchSize) flush();
            }
            flush();
        }

        Promise.all(tasks).then(() => {
            app.logger.log("Startup", `Initialized ${inserted} pixels.`);
            app.paintingManager = PaintingManager(app);
            
            app.logger.info('Startup', "Loading image from the database…");
            app.paintingManager.loadImageFromDatabase().then((image) => {
                app.paintingManager.startTimer();
                
                app.logger.info('Startup', "Successfully loaded image from database, now building bait pixels…");
                let baitPixels = buildText(bait, startX, startY + (glyphHeight * 2));
                baitPixels = Array.from(baitPixels);
                let baitIndex = 0;
                let color = { r: 255, g: 0, b: 0 };
                setInterval(async () => {
                    if (baitIndex >= baitPixels.length) {
                        baitIndex = 0;
                        // Generate random color that's not close to board bg
                        do {
                            color = {
                                r: Math.floor(Math.random() * 256),
                                g: Math.floor(Math.random() * 256),
                                b: Math.floor(Math.random() * 256)
                            };
                        } while (
                            Math.abs(color.r - 136) < 20 &&
                            Math.abs(color.g - 136) < 20 &&
                            Math.abs(color.b - 136) < 20
                        );
                    }
                    const px = baitPixels[baitIndex];
                    try {
                        const [x, y] = px.split(",").map(Number);
                        app.paintingManager.doPaint(color, x, y, user);
                    } catch (err) {
                        app.logger.capture("Error while placing bait pixel: " + err);
                    }
                    baitIndex++;
                }, 10 * 1000); // every 10 seconds
            }).catch((err) => {
                app.logger.capture("Error while loading the image from database: " + err);
            });
        });
    }).catch((err) => {
        app.logger.capture("Error while creating default admin user: " + err);
    });
}

mongoose.connection.once('connected', () => {
    handlePendingDeletions();
    initData();
});

// Process JS
app.javascriptProcessor = new JavaScriptProcessor(app);
app.javascriptProcessor.processJavaScript();

app.stopServer = () => {
    if(app.server.listening) {
        app.logger.log('Shutdown', "Closing server…")
        app.server.close();
        setImmediate(function() { app.server.emit("close"); });
    }
}

app.restartServer = () => {
    app.stopServer();
    app.server.listen(process.env.PORT || app.config.port, (process.env.ONLY_LISTEN_LOCAL ? process.env.ONLY_LISTEN_LOCAL === true : app.config.onlyListenLocal) ? "127.0.0.1" : null, null, () => {
        app.logger.log('Startup', `Started Place server on port ${app.config.port}${app.config.onlyListenLocal ? " (only listening locally)" : ""}.`);
    });
}
app.restartServer();
app.recreateRoutes = () => {
    app.moduleManager.fireWhenLoaded((manager) => {
        function initializeServer(directories, routes = []) {
            app.httpServer.setupRoutes(directories, routes);
        }
        function continueWithServer(directories = []) {
            manager.getRoutesToRegister().then((routes) => initializeServer(directories, routes)).catch((err) => app.logger.capture(err))//initializeServer(directories));
        }
        manager.getAllPublicDirectoriesToRegister().then((directories) => continueWithServer(directories)).catch((err) => continueWithServer());
    });
}
app.recreateRoutes();
readline.on('line', i => {
    try {
        var output = eval(i)
        output instanceof Promise ? output.then(a => {
            console.log('Promise Resolved')
            console.log(util.inspect(a, {depth: 0}))
        }).catch(e => {
            console.log('Promise Rejected')
            console.log(e.stack)
        }) : output instanceof Object
            ? console.log(util.inspect(output, {depth: 0}))
            : console.log(output)
    } catch (err) {
        console.log(err.stack)
    }
})
