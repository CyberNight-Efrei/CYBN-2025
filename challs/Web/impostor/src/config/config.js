module.exports = {
    "secret": "THISSHOULDBESECUREENOUGHNOW15486484654684864512321151512",
    "database": "mongodb://localhost/place",
    "port": 3000,
    "boardSize": 150, 
    "onlyListenLocal": true,
    "trustProxyDepth": 1, // How many levels of proxy to trust for IP
    "debug": false,
    "googleAnalyticsTrackingID": "", // UA-XXXXXXXX-XX
    "placeTimeout": 60,
    'siteName': 'Place',
    // "raven": "", 
    // "publicRaven": "", 
    // "bugsnag": "",
    'maintenance': {
        'allowSignups': true, 
        'allowLogins': true,
        'notice': undefined
    },
    "cachet": {
        // Setup reporting error count as a metric to Cachet
        "apiKey": "",
        "site": "",
        "metricID": 0
    },
    "recaptcha": { // Leave blank to disable
        "siteKey": "",
        "secretKey": ""
    },
    "pixelFlags": []
};
