$.validator.addMethod( "nameFor", function( value, element ) {
	return this.optional( element ) || /^[a-z ,.'-]+$/i.test( value );
}, "Allowed Special charecters are ,.'-" );


$.validator.addMethod( "alphabets", function( value, element ) {
	return this.optional( element ) || /^[a-z ]+$/i.test( value );
}, "Only Alphabets are allowed");



$.validator.addMethod( "phone", function( value, element ) {
	return this.optional( element ) || /^\d{3,5}([- ]*)\d{6,8}$/.test( value );
}, "Enter Valid Phone No");


$.validator.addMethod( "address", function( value, element ) {
	return this.optional( element ) || /^[a-z0-9 ,-./\n]+$/i.test( value );
}, "Allowed Special charecters are  ,-./");


$.validator.addMethod( "main_subjects", function( value, element ) {
	return this.optional( element ) || /^[a-z0-9 ,.-]+$/i.test( value );
}, "Allowed Special charecters are  ,.-");


$.validator.addMethod( "organisation", function( value, element ) {
	return this.optional( element ) || /^[a-z0-9 ,.'-]+$/i.test( value );
}, "Allowed Special charecters are  ,.'-");


$.validator.addMethod( "university_board", function( value, element ) {
	return this.optional( element ) || /^[a-z0-9 ,.]+$/i.test( value );
}, "Allowed Special charecters are  ,.");

$.validator.addMethod( "division", function( value, element ) {
	return this.optional( element ) || /^[a-z0-9 +]+$/i.test( value );
}, "Only alphanumeric and + are allowed");


$.validator.addMethod( "otherpercentage", function( value, element ) {
	return this.optional( element ) || /(^100(\.0{1,2})?$)|(^[3-9]{1}[0-9]{1}([.]\d{1,2})?$)/.test( value );
}, "Enter Percentage between 30 - 100");


$.validator.addMethod( "percentage", function( value, element ) {
	return this.optional( element ) || /(^100(\.0{1,2})?$)|(^[6-9]{1}[0-9]{1}([.]\d{1,2})?$)/.test( value );
}, "Enter valid Percent for first class");


$.validator.addMethod( "othercgpa", function( value, element ) {
	return this.optional( element ) || /(^10([.]0{0,1})?)$|(^[3-9]{1}([.]\d{0,1})?)$/.test( value );
}, "Enter CGPA between 3 - 10");

$.validator.addMethod( "cgpa", function( value, element ) {
	return this.optional( element ) || /(^10([.]0{0,1})?)$|(^[6-9]{1}([.]\d{0,1})?)$/.test( value );
}, "Enter valid CGPA equivalent to first class");





