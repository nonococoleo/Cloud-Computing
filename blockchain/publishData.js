var HelloBlockchain = artifacts.require("HelloBlockchain");
var myArgs = process.argv.slice(6);
 console.log(myArgs);

module.exports = function(done) {
  console.log("Getting the deployed version of the ccData smart contract")
  HelloBlockchain.deployed().then(function(instance) {
    console.log("Calling publishData function for contract ", instance.address);
    return instance.publishData( myArgs[0], myArgs[1], myArgs[2], myArgs[3], myArgs[4], myArgs[5], myArgs[6]);
    // return instance.publishData("May1", "10", "20", "30", "40", "50", "60");
  }).then(function(result) {
    console.log("Transaction hash: ", result.tx);
    console.log("Request complete");
    done();
  }).catch(function(e) {
    console.log(e);
    done();
  });
};