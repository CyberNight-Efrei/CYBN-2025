const DataModelManager = require("../util/DataModelManager");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

var ReportSchema = new Schema({
    offenderID: {
        type: String,
        required: true
    },
    reporterID: {
        type: String,
        required: true
    },
    reason: {
        type: String,
        required: true
    },
    xPos: {
        type: Number,
        required: false
    },
    yPos: {
        type: Number,
        required: false
    },
    handled: {
        type: Boolean,
        required: true,
        default: false
    }
});

ReportSchema.statics.reportUser = function(reportedUser, reporter, reason, app, callback)  {
    let report = this({
        offenderID: reportedUser,
        reporterID: reporter,
        reason: reason
    });

    report.save().then(() => {
        require("../util/ActionLogger").log(app, "report", report);
        return callback(report, null);
    }).catch((err) => {
        return callback(null, { message: "some error fuck off out of here.", code: "fuck_off" });
    });
}

module.exports = DataModelManager.registerModel("Report", ReportSchema);