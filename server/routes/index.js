var express = require('express');
var db = require("../db");
const { wifiScan } = require('../db');
var router = express.Router();

/* Update data from RaspberryPi. */
router.post('/update', function(req, res, next) {
  let currentTime = req.body.time;

  let newUpdate = new db.wifiScan({
    scanner: req.body.hostname,
    time: currentTime,
    result: req.body.result
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
    scans.reverse();
    res.render('index', {scans});
  });
})
module.exports = router;
