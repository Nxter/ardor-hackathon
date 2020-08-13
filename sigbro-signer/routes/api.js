var express = require('express');
var router = express.Router();
const ardorjs = require('ardorjs');

var https = require('https');
var querystring = require('querystring');
var bunyan = require('bunyan');
var log = bunyan.createLogger({name: "sigbro-signer"});


let secretPhrase = process.env.SECRET_PHRASE || '';
let network = process.env.NETWORK || 'testnet';
let access_token = process.env.ACCESS_TOKEN || '';


/* POST sign tx */
router.post('/sign/', function(req, res) {
  let tx = req.body;
  let request_token = req.get('X-Sigbro-Token');

  if ( access_token.length < 10 ) {
    res.json({result: false, 'msg': 'You are hacker! Do not do this, please!'});
    return;
  } else if ( access_token != request_token )  {
    res.json({result: false, 'msg': 'You are not allowed to sign this tx, sorry.'});
    return;
  }

  // check for custom header

  if ( 'transactionJSON' in tx && 'unsignedTransactionBytes' in tx ) {

    // check the transaction type
    if ( 'type' in tx['transactionJSON'] ) {
      let txType = tx['transactionJSON']['type']
      if ( txType != 10 ) {
        log.warn({msg: 'Not a property type'}, tx);
        res.json({result: false, 'msg': 'Incorrect transaction type.'})
        return
      }
    }

    log.info({ recipient: tx['transactionJSON']['recipientRS']});

    // sign unsigned tx bytes
    let signedTx = ardorjs.signTransactionBytes( tx['unsignedTransactionBytes'], secretPhrase );

    // prepare data for the POST request 
    var postData = querystring.stringify({
      transactionBytes: signedTx
    });

    // prepare request
    let network_path = '/ardor';
    if ( network == 'testnet' ) {
      network_path = '/tstardor'
    }

    var options = {
      host: 'random.api.nxter.org',
      port: 443,
      method: 'POST',
      path: network_path + '?requestType=broadcastTransaction',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': postData.length
      }
    };

    // Send broadcast request 
    var broadcast = https.request(options, function (broadcast_res) {
      var result = '';

      broadcast_res.on('data', function (chunk) {
        result += chunk;
      });
      
      broadcast_res.on('end', function () {
        try { 
          let result_json = JSON.parse(result);
          if ( 'errorDescription' in result_json ) {
            log.error(result_json);
            res.json({result: false, msg: result_json['errorDescription'] } );
          } else {
            log.info(result_json);
            res.json({result: true, fullHash: result_json['fullHash']} );
          }
        } catch { 
          log.error('Broadcast error', result);
          res.json({result: false, 'msg': 'Ardor node cannot handle this request.'})
        }
        return;
      });

      broadcast_res.on('error', function (err) {
        log.error('Broadcast parsing error', err);
        res.json(err);
        return;
      })
    });
     
    // req error
    broadcast.on('error', function (err) {
      log.error('Broadcast error', err);
      res.json(err);
      return;
    });
     
    //send request witht the postData form
    broadcast.write(postData);
    broadcast.end();

  } else {
    log.error('Wrong json', tx);
    res.json({result: 'fail', message: 'Wrong json.'});
    return
  }
});

module.exports = router;
