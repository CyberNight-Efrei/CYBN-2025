const MongooseStore = require("express-brute-mongoose");
const bruteForceSchema = require("express-brute-mongoose/dist/schema");
const mongoose = require("mongoose");

function RatelimitStore(name = null) {
    // Build a stable model name. Use a dash separator for named stores.
    const modelName = `bruteforce${name ? `-${name}` : ""}`;
    // Avoid OverwriteModelError by reusing an already-compiled model if present.
    let model;
    if (mongoose.models && mongoose.models[modelName]) {
        model = mongoose.model(modelName);
    } else {
        model = mongoose.model(modelName, bruteForceSchema);
    }
    return new MongooseStore(model);
}

RatelimitStore.prototype = Object.create(RatelimitStore.prototype);

module.exports = RatelimitStore;