var HelloBlockchain = artifacts.require("HelloBlockchain");
var myArgs = process.argv.slice(6);

module.exports = function(done) {
  console.log("Getting the deployed version of the ccData smart contract")
  HelloBlockchain.deployed().then(function(instance) {
    console.log("Calling getData function for contract ", instance.address);
    return instance.getData(myArgs[0]);
  }).then(function(result) {
    console.log("Request message value: ", result);
    console.log("Request complete");
    done();
  }).catch(function(e) {
    console.log(e);
    done();
  });
};
