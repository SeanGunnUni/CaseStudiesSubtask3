var assert = require('assert');

describe('JavaScript tests',function(){
	describe('individ()',function(){
		var testsBlank = [
			{args: ["N"],expected:"false"}
		];
    
    var testsColourBlind = [
      {args: ["false"],expected:"true"},
      {args: ["true"],expected:"false"}
		];
	
		testsBlank.forEach(function(test){
      it('blank values '+test.args.length + ' args',function(){
          var res = checkIfLocalStorageIsBlank(test.args);
          assert.equal(res, test.expected);
      });
    });
        
    testsColourBlind.forEach(function(test){
      it('colourbind values '+test.args.length + ' args',function(){
        var res = colourBlindMode(test.args);
        assert.equal(res, test.expected);
     });
    });
	});
});

function colourBlindMode(values){
    // mock the localStorage
    window.localStorage = storageMock();
    window.localStorage.setItem("ColourBlindUser",values);
	if(window.localStorage.getItem('ColourBlindUser') == "false"){
        window.localStorage.setItem('ColourBlindUser', 'true');
        return values ="true";
	}
	else{
        window.localStorage.setItem('ColourBlindUser', 'false');
        return values ="false";
	}
}

function checkIfLocalStorageIsBlank(values){
    // mock the localStorage
    window.localStorage = storageMock();
	if(window.localStorage.getItem('ColourBlindUser') == values){
        window.localStorage.setItem('ColourBlindUser', 'false');
        return values ="false";
    }
    return values ="wrong";
}

// Storage Mock
function storageMock() {
    let storage = {};

    return {
      setItem: function(key, value) {
        storage[key] = value || '';
      },
      getItem: function(key) {
        return key in storage ? storage[key] : null;
      },
      removeItem: function(key) {
        delete storage[key];
      },
      get length() {
        return Object.keys(storage).length;
      },
      key: function(i) {
        const keys = Object.keys(storage);
        return keys[i] || null;
      }
    };
  }