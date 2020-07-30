var express = require('express');
var db = require("../db");
const { wifiScan } = require('../db');
var router = express.Router();

/* Update data from RaspberryPi. */
router.post('/update/:hostname', function(req, res, next) {
  let currentTime = Date.now();

  let newUpdate = new db.wifiScan({
    scanner: req.params.hostname,
    time: currentTime,
    result: req.body
  });

  newUpdate.save(()=>{
    let timeString = new Date(currentTime).toISOString().
                     replace(/T/, ' ').
                     replace(/\..+/, '') 
    console.log(`[${timeString}] New update saved form ${req.params.hostname}`)
  });

  res.send();
});

router.get('/', function(req,res,next){
  wifiScan.find({}, (err, scans)=>{
    res.render('index', {scans});
  });
})
module.exports = router;
