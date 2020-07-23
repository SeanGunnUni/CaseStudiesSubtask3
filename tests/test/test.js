var assert = require('assert');

describe('JavaScript tests',function(){
	describe('formSubmition()',function(){
		var today = new Date();
		var temp;
		var testsDate = [
			{args: [""],expected:temp = (today.getDate()+"/0"+(today.getMonth()+1)+"/"+today.getFullYear())},
			{args: [temp = (today.getDate()+"/"+today.getMonth()+"/"+today.getFullYear())],
			 expected:temp = (today.getDate()+"/"+today.getMonth()+"/"+today.getFullYear())},
			{args: ["05/05/2020"], expected:"05/05/2020"},
			{args: ["01/01/2019"], expected:"01/01/2019"},
		];
	
		var testsComment = [
			{args: [""],expected:"No comments needed"},
			{args: ["Hi"], expected:"Hi"},
		];
	
		testsDate.forEach(function(test){
			it('date values '+test.args.length + ' args',function(){
				var res = setDateValuesToPassToDatabase(test.args);
				assert.equal(res, test.expected);
			});
		});
	
		testsComment.forEach(function(test){
		it('comment values '+test.args.length + ' args',function(){
				var res = setDateValuesToPassToDatabase2(test.args);
				assert.equal(res, test.expected);
			});
		});
	});
	
	describe('visualWarnings()',function(){
		var testsWarning = [
			{args: ["R"],expected:"<button type=\"button\" class=\"btn-success\" style=\"margin: auto; display:block;\">‎⠀</button>"},
			{args: ["G"], expected:"<button type=\"button\" class=\"btn-warning\" style=\"margin: auto; display:block;\">‎⠀</button>"},
			{args: ["Y"], expected:"<button type=\"button\" class=\"btn-danger\" style=\"margin: auto; display:block;\">‎⠀</button>"},
			{args: [""], expected:""},
			{args: [0], expected:""},
			{args: [2147483647], expected:""},
			{args: [-2147483647], expected:""}
		];
	
		testsWarning.forEach(function(test){
			it('warning values '+test.args.length + ' args',function(){
				var res = createWarningButton( test.args, "", "" );
				assert.equal(res, test.expected);
			});
		});
	});
});


function setDateValuesToPassToDatabase(values){
	if(values == ""){
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
		if(dd<10) {
			dd = '0'+dd
		} 
		if(mm<10) {
			mm = '0'+mm
		} 
		today = dd + '/' + mm + '/' + yyyy;
		values = today;
  }
	return values;
}

function setDateValuesToPassToDatabase2(values){
	if(values == ""){
		values = "No comments needed";
  	}
	return values;
}

function createWarningButton( data, type, row ) {
    if(data=="R"){
        return "<button type=\"button\" class=\"btn-success\" style=\"margin: auto; display:block;\">‎⠀</button>";
    }
    else if (data=="G"){
        return "<button type=\"button\" class=\"btn-warning\" style=\"margin: auto; display:block;\">‎⠀</button>";
    }
    else if(data=="Y"){
        return "<button type=\"button\" class=\"btn-danger\" style=\"margin: auto; display:block;\">‎⠀</button>";
    }
    else{
    	return "";
    }
}