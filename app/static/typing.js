/*
 * The animation at the start, made from my previous pen
 * https://codepen.io/EightArmsHQ/pen/HJsav
 */

// The base speed per character
time_setting = 30;
// How much to 'sway' (random * this-many-milliseconds)
random_setting = 100;
// The text to use NB use \n not real life line breaks!
input_text = "How fast can you type?";
// Where to fill up
target_setting = $("#output");
// Launch that function!



function encryptStringWithXORtoHex(input,key) {
    var c = '';
    while (key.length < input.length) {
         key += key;
    }
    for(var i=0; i<input.length; i++) {
        var value1 = input[i].charCodeAt(0);
        var value2 = key[i].charCodeAt(0);

        var xorValue = value1 ^ value2;

        var xorValueAsHexString = xorValue.toString("16");

        if (xorValueAsHexString.length < 2) {
            xorValueAsHexString = "0" + xorValueAsHexString;
        }

        c += xorValueAsHexString;
    }
    return c;
}

type(input_text, target_setting, 0, time_setting, random_setting);

function type(input, target, current, time, random){
  // If the current count is larger than the length of the string, then for goodness sake, stop
	if(current > input.length){
    // Write Complete
		console.log("Complete.");
	}
	else{
	 // console.log(current)
    // Increment the marker
		current += 1;
    // fill the target with a substring, from the 0th character to the current one
		target.text(input.substring(0,current));
    // Wait ...
		setTimeout(function(){
      // do the function again, with the newly incremented marker
			type(input, target, current, time, random);
      // Time it the normal time, plus a random amount of sway
		},time + Math.random()*random);
	}
}

var character_length = 31;
var index = 0;
var letters =  $("#type_text").val();
var started = false;
var current_string = letters.substring(index, index + character_length);
var start_time;
var wordcount = 0;
var timer = 0;
var wpm = 0;
var all_keys = [];
var flight_list = [];
var wpm_list = [];
var ku_list = [];
var kd_list = [];
var errors = 0;
var interval_timer;
var complete = false;
var reported = false;
var prevcorrect = false;
var prevtime = 0;

$("html, body").click(function(){
  $("#textarea").focus();
});

$("#target").text(current_string);


$(window).keyup(function(evt){
  evt = evt || window.event;
  var charCode = evt.which || evt.keyCode;
  var charTyped = evt.key;
  if (charCode < 32 )//|| charCode > 126 )
    return;
  let obj = [charTyped,new Date().getTime() - start_time];
  // obj[charTyped] =  new Date().getTime() - start_time;
  ku_list.push(obj);
  if (complete)
    if(!reported)
      finished();
});


$(window).keydown(function(evt){
  if(complete)
    return;

  evt = evt || window.event;
  var charCode = evt.which || evt.keyCode;
  var charTyped = evt.key;

  if (charCode < 32 )// || charCode > 126 )
    return;

  if(!started){
    start();
    started = true;
  }
  currTime =  new Date().getTime();
  // let obj = {};
  // obj[charTyped] =  currTime - start_time;
  let obj = [charTyped,new Date().getTime() - start_time];
  kd_list.push(obj);

  if(charTyped == letters.charAt(index)){
    if(charTyped == " "){
      wordcount ++;
      $("#wordcount").text(wordcount);
    }

    all_keys.push(currTime - start_time );

    if(prevcorrect){
      let obj = [charTyped, currTime - prevtime];
      flight_list.push(obj);
    }
    prevcorrect = true;
    prevtime = currTime;
    index ++;
    current_string = letters.substring(index, index + character_length);
    $("#target").text(current_string);
    $("#your-attempt").append(charTyped);
    if(index == letters.length){
        wordcount ++;
        $("#wordcount").text(wordcount);
        $("#timer").text(Math.round(timer*100)/100);
        if(timer == 0){
          timer = 1;
        }
        wpm = Math.round((index/5) / (timer / 60));
        $("#wpm").text(wpm);
        wpm_list.push(wpm);
        stop();

    }
  }else{
    prevcorrect = false;
    prevtime = currTime;
		element = $("#test")
		element.removeClass("mistake")
		setTimeout(function () {
				element.addClass("mistake")
			}, 1);
    $("#your-attempt").append("<span class='wrong'>" + charTyped + "</span>");
    errors ++;
    $("#errors").text(errors);
  }
});


$("#reset").click(function(){
  reset();
});

$("#change").click(function(){
  $("#type_text").show().focus();
});

$("#pause").click(function(){
  stop();
});

$("#type_text").change(function(){
  reset();
});

function start(){
  start_time= new Date().getTime();
  interval_timer = setInterval(function(){
    timer +=0.1;
    timer = Math.round(timer*100)/100;
    $("#timer").text(timer);
    wpm = Math.round((index/5) / (timer / 60));
    wpm_list.push(wpm);
    $("#wpm").text(wpm);
  }, 100)
}

function stop(){
  clearInterval(interval_timer);
  started = false;
  complete= true;
  // type("Ping divesh.naidu@collegedunia.com if you want your score on the leaderboard", $("#your-attempt"), 0, 1, 1);

}

function reset(){
  location.reload(true);
  // $("#type_text").blur().hide();;
  // $("#your-attempt").text("");
  // index = 0;
  // errors = 0;
  // clearInterval(interval_timer);
  // started = false;
  // letters = $("#type_text").val();
  // $("#wpm").text("0");
  // $("#timer").text("0");
  // $("#wordcount").text("0");
  // timer = 0;
  // wpm = 0;
  // current_string = letters.substring(index, index + character_length);
  // $("#target").text(current_string);
  // reported = false
}

function finished(){
  reported = true;

  var data = 	{
  			speed: wpm,
        hash: encryptStringWithXORtoHex(wpm.toString().repeat(10),'secretkeeeeey'),
        all_keys:all_keys,
        wpm_history:wpm_list,
        ku:ku_list,
        kd:kd_list,
        flight:flight_list,
        letters:letters,
  	};

  $.ajax({
      type: 'POST',
      contentType: 'application/json',
      url: '/postscore',
      dataType : 'json',
      data : JSON.stringify(data),
      success : function(result) {
        console.log(result);
        show_report(result);
      },error : function(result){
         console.log(result);
         alert('failed to process'+error)
      }
  });

  // alert("Congratulations!\nWords per minute: " + wpm + "\nWordcount: " + wordcount + "\nErrors:" + errors);
}


function show_report(resp){
  data= resp[0];
  brackets = resp[1]['brackets'];
  $("#test").hide();
  $("#result").show();
  $(".result_stat").html(data['wpm']+' WPM</br>' + Math.round(data['accuracy'] * 10000) / 100  + '% Accuracy');
  $(".typed_text").html(data['text']);
  texts =[];
  scores =[];
  for (var i = 0; i < brackets.length; i++) {
      texts.push(brackets[i][1]);
      scores.push(brackets[i][0]);
  }

  var ctx = document.getElementById("myChart").getContext('2d');
  min = parseInt(Math.min(...scores)/10)
  max = parseInt(Math.max(...scores)/10)
  console.log(min)
  min -=1; min *=10;
  max +=1; max *=10;
  var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: texts,
          datasets: [{
              label: 'WPM',
              data: scores,
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              hoverBackgroundColor: 'rgba(153, 102, 255, 0.2)',
              hoverBorderColor: 'rgba(153, 102, 255, 1)',
              borderWidth: 1
          }]
      },
      options: {
          legend: {
              display: false
          },
          scales: {
              yAxes: [{
                  ticks: {
                      min: min,
                      max: max
                  }
              }],
              xAxes:[{
                display:false
              }]
          }
      }
  });
}
var window_focus;

$(window).focus(function() {
    window_focus = true;
}).blur(function() {
  window_focus = false;
});

$(document).ready(function(){
  $("#result").hide();
  if(window_focus){
    $("#focus").hide();
  }
  $(window).focus(function() {
    $("#focus").hide();
  });
});
