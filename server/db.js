//Import the mongoose module
var mongoose = require('mongoose');
const { builtinModules } = require('module');

//Connect to mongoDB
var mongoDbURL = 'mongodb://127.0.0.1/5gva_mmtc_app';
mongoose.connect(mongoDbURL,{
    useNewUrlParser: true,
    useUnifiedTopology: true
});
// Get Mongoose to use the global promise library
mongoose.Promise = global.Promise;
//Get the default connection
var db = mongoose.connection;

//Bind connection to error event (to get notification of connection errors)
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// ============== Define the schemas ====================
var Schema = mongoose.Schema;

var wifiProfile = new Schema({
    ssid: String,
    bssid: String,
    akm: [String],
    freq: Number,
    rssi: Number
})

var wifiScanSchema = new Schema({
    scanner: String,
    time: Date,
    result: [wifiProfile]
});

var wifiScan = mongoose.model('wifiScan', wifiScanSchema);
// ========== End definition of schemas ==================

module.exports ={
    db,
    wifiScan
}