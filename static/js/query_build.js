// This file contains Javascript to configure QueryBuilder for VA.html
// The form properties are set here
// The action of the buttons are set here

// This block sets the default search parameters
// var rules_basic = {
//
//     rules: [{
//     id: 'final',
//     operator: 'fulltext',
//     },
//     {
//     id: 'staff',
//     operator: 'contains',
//     value: '',
//     }]
// }


// SET either server to DEV or PRODUTION


// DEV SERVER
//var server = 'http://10.88.45.54:8080/pathtools_dev';

// PROD SERVER
var server = 'https://pathtools.ccf.org';

//This block sets the types of filters and the operators they use

$('#builder-basic').queryBuilder({
  plugins: ['bt-tooltip-errors'],
  
  filters: [{
    id: 'text',
    label: 'Terms',
    type: 'string',
    operators: ['fulltext', 'not_contains', ]
    //operators: ['fulltext' ,'not_regexp']

  },

{
    id: 'synoptic',
    label: 'Synoptic',
    type: 'string',
    operators: ['fulltext', 'not_contains', ]
    //operators: ['fulltext' ,'not_regexp']

  },
{
    id: 'clinical',
    label: 'Clinical',
    type: 'string',
    operators: ['fulltext', 'not_contains', ]
    //operators: ['fulltext' ,'not_regexp']

  },
{
    id: 'intraoperative',
    label: 'Intraoperative',
    type: 'string',
    operators: ['fulltext', 'not_contains', ]
    //operators: ['fulltext' ,'not_regexp']

  },
{
    id: 'gross',
    label: 'Gross',
    type: 'string',
    operators: ['fulltext', 'not_contains', ]
    //operators: ['fulltext' ,'not_regexp']

  },

  // {
  //     id:'accession_date',
  //     label: 'Datepicker',
  //     type: 'date',
  //     operators: ['between', 'greater_or_equal', 'less_or_equal'],
  //     validation: {
  //         format: 'YYYY/MM/DD'
  //     }
  //     },
  {
      id:'age',
      label: 'Age',
      type: 'integer',
      operators: ['greater_or_equal', 'less_or_equal'],
      },
{
    id: 'specimen_type',
    label: 'Specimen Type',
    type: 'string',
    input: 'select',
    // The keys what is passed in the query 
    // The values are displayed in the drop-down
    values: {
        SP: 'Surg Path',
        CYTO: 'Cyto',
        BM: 'Bone Marrow'
            },
    operators: ['equal', 'not_equal', ],
 },

  {
    id: 'staff',
    label: 'Attending',
    type: 'string',
    input: 'select',
    // The keys what is passed in the query 
    // The values are displayed in the drop-down
    values: {
        AESIF: 'Aesif',
        ALLENDE: 'Allende',
        ARROSSI: 'Arrossi',
        BEJARANO: 'Bejarano',
        BENNETT: 'Bennett',
        BERGFELD: 'Bergfeld',
        BERHO: 'Berho',
        BILLINGS: 'Billings',
        BISCOTTI: 'Biscotti',
        BOOTH: 'Booth',
        BRAINARD: 'Brainard',
        CARLSON: 'Carlson',
        CHIESA: 'Chiesa-Vottero',
        CHUTE: 'Chute',
        COOK: 'Cook',
        COTTA: 'Cotta',
        COX: 'Cox',
        CRANE: 'Crane',
        CRACOLICI: 'Cracolici',
        CRUISE: 'Cruise',
        DAWSON: 'Dawson',
        DIACOVO: 'Diacovo',
        DOWNS_KELLY: 'Downs-Kelly',
        DOXTADER: 'Doxtader',
        DYHDALO: 'Dyhdalo',
        ELSHEIKH: 'Elsheikh',
        FERNANDEZ: 'Fernandez',
        FONG: 'Fong',
        FULMER: 'Fulmer',
        GOLDBLUM: 'Goldblum',
        GOLUSIN: 'Golusin',
        GORDON: 'Gordon',
        GRIFFITH: 'Griffith',
        HAMADEH: 'Hamadeh',
        HERLITZ: 'Herlitz',
        HODA: 'Hoda',
        HOSCHAR: 'Hoschar',
        HU_S: 'Hu',
        HSI: 'Hsi',
        KILPATRICK: 'Kilpatrick',
        KOMFORTI: 'Komforti',
        JOEHLIN: 'Joehlin-Price',
        JOHNSTON: 'Johnston',
        KO: 'Ko',
        LAI: 'Lai',
        LAPINSKI: 'Lapinski',
        MCHUGH: 'McHugh',
        MCINTIRE: 'McIntire',
        MCKENNEY_J: 'McKenney J',
        MCKENNEY_A: 'McKenney A',
        MELARAGNO: 'Melaragno',
        MUKHOPADHYAY: 'Mukhopadhyay',
        MYLES: 'Myles',
        NAKASHIMA: 'Nakashima',
        NGUYEN: 'Nguyen',
        ONDREJKA: 'Ondrejka',
        OSHILAJA: 'Oshilaja',
        PILIANG: 'Piliang',
        PLESEC: 'Plesec',
        POLICARPIO: 'Policarpio-Nicolas',
        PORTER: 'Porter',
        PRAYSON: 'Prayson',
        PRZYBYCIN: 'Przybycin',
        PUA: 'Pua',
        RABINOWITZ: 'Rabinowitz',
        RAHMAN: 'Rahman',
        REITH: 'Reith',
        REYNOLDS: 'Reynolds',
        ROBERTSON: 'Robertson',
        ROBERTS_D: 'Roberts',
        RODRIGUEZ: 'Rodriguez',
        ROGERS: 'Rogers',
        RONEN: 'Ronen',
        ROWE: 'Rowe',
        RUBIN: 'Rubin',
        SAVAGE: 'Savage',
        SHAH_A: 'Shah A',
        SHARE: 'Share',
        SETRAKIAN: 'Setrakian',
        SIERK: 'Sierk',
        TAN: 'Tan', 
        WILLIAMSON: 'Williamson',
        YANG: 'Yang B',
        YEANEY: 'Yeaney',
        YERIAN: 'Yerian',
        ZHANG: 'Zhang',
            },
    operators: ['contains', ],
 },

{
    id: 'sex',
    label: 'Sex',
    type: 'string',
    input: 'select',
    // The keys what is passed in the query 
    // The values are displayed in the drop-down
    values: {
        F: 'Female',
        M: 'Male',
            },
    operators: ['equal', 'not_equal', ],
 },

{
    id: 'consult_flag',
    label: 'Inside/Outside Selector',
    type: 'integer',
    input: 'select',
    // The keys what is passed in the query 
    // The values are displayed in the drop-down
    values: {
        0: 'CCF Case',
        1: 'Outside/Consult Case',
            },
    operators: ['equal', 'not_equal', ],
 },

{
    id: 'florida_flag',
    label: 'Florida/Ohio Selector',
    type: 'integer',
    input: 'select',
    // The keys what is passed in the query 
    // The values are displayed in the drop-down
    values: {
        0: 'Ohio Case',
        1: 'Florida Case',
            },
    operators: ['equal', 'not_equal', ],
 },

  ],

 rules: rules_basic
     

});

// This is is an old function that doens't work

// reset builder
//$('.reset').on('click', function() {
//  var target = $(this).data('target');
//  
//  $('#builder-'+target).queryBuilder('reset');
//  $('#query').text('SQL query text');
//});

// set rules
$('.set-json').on('click', function() {
  var target = $(this).data('target');
  var rules = window['rules_'+target];
  
  $('#builder-'+target).queryBuilder('setRules', rules);
});

// Function triggered by the "submit" button
// var myFunction_submit = function(){
//         var base = 'SELECT * FROM dbo.ap_case ';
// 	var result = $('#builder-basic').queryBuilder('getSQL',  false); 
// 	var query = ( base + "WHERE " + result.sql + "");
//         //$('#query').text(query);
//         
//         var test_data = {
//             'key1' : query,
//             'key2' : 'value2'
//         }
//         console.log(test_data)
//
//         $('#result').html("SEARCHING" );
//
//    $.post('http://10.88.45.54/pathtools/dx_search/search', test_data, function(data)
//     //$.post('127.0.0.1:8000/dx_search/search', test_data, function(data)
//
//            {
//             $('#result').html(data);
//            })
//
// }
//
// $('.submit').on('click', myFunction_submit)

// Function triggered by the "submit" button
// This was a test function to see how the query formatting worked. 
//
//var myFunction_format= function(){
//        //var base = 'SELECT * FROM dbo.ap_case ';
//	var result = $('#builder-basic').queryBuilder('getSQL',  false); 
//	var query = ( "WHERE " + result.sql + "");
//        //$('#query').text(query);
//        
//        var test_data = {
//            'key1' : query,
//            'key2' : 'value2'
//        }
//        console.log('FORMAT FUNCTION')
//
//        $('#result').html("FORMATTING" );
//
//   $.post('http://10.88.45.54/pathtools/dx_search/search_format', test_data, function(data)
//           {
//            $('#result').html(data);
//           })
//
//}
//
//$('.format').on('click', myFunction_format)

var myFunction_reload = function(){
        location = location
}

$('.reload').on('click', myFunction_reload)

// Function triggered by the "TOP100" button
var myFunction_submit_top = function(){
	var result = $('#builder-basic').queryBuilder('getSQL',  false); 
	var query = (result.sql + "ORDER BY accession_date DESC");
        // $('#query').text(query);
        //
        var test_data = {
            'key1' : query,
            'key2' : query,
        }
        console.log(test_data)

        $('#result').html("SEARCHING" );

   $.post(server + '/dx_search/execute_search_preview', test_data, function(data)

           {
            $('#result').html(data);
           })

        $(".toggle_container").show();

        // $("#formatted_string").text(query);

}

$('.top').on('click', myFunction_submit_top)

// Function triggered by the "TOP 5000" button
var myFunction_submit_5000 = function(){
        var result = $('#builder-basic').queryBuilder('getSQL',  false); 
	var query = (result.sql);
        // $('#query').text(query);
        //
        var test_data = {
            'key1' : query,
            'key2' : query,
        }
        console.log(test_data)

        $('#result').html("SEARCHING" );

   $.post(server + '/dx_search/execute_search_research', test_data, function(data)

           {
            $('#result').html(data);
           })

        $(".toggle_container").show();

        // $("#formatted_string").text(query);

}

$('.five_thousand').on('click', myFunction_submit_5000)

// Function triggered by the "TOP 1000" button
var myFunction_submit_1000 = function(){
        var base = 'SELECT TOP(1000) * FROM dbo.ap_case ';
	var result = $('#builder-basic').queryBuilder('getSQL',  false); 
	var query = ( base + "WHERE " + result.sql + "ORDER BY accession_date DESC");
        //$('#query').text(query);
        
        var test_data = {
            'query' : query,
        }
        console.log(test_data)

        $('#result').html("SEARCHING" );

   $.post(server + '/dx_search/execute_search_preview', test_data, function(data)
    //$.post('127.0.0.1:8000/dx_search/search', test_data, function(data)

           {
            $('#result').html(data);
           })

        $(".toggle_container").show();

        // $("#formatted_string").text(query);

}

$('.one_thousand').on('click', myFunction_submit_1000)

var myFunction_download = function(){

    window.location.href = server + '/dx_search/capture_cases';

}


$('.download').on('click', myFunction_download)

var myFunction_download_case_finding = function(){

    window.location.href = server + '/dx_search/case_finding_save';

}

$('.download_case_finding').on('click', myFunction_download_case_finding)
