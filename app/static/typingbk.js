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



// Crypto = CryptoJS;
// var KEY = 'This is a key123';
// var IV = 'This is an IV456';
// var MODE = new Crypto.mode.CFB(Crypto.pad.ZeroPadding);
// var plaintext = 'The answer is no';
// var input_bytes = Crypto.charenc.UTF8.stringToBytes(plaintext);
// var key = Crypto.charenc.UTF8.stringToBytes(KEY);
// var options = {iv: Crypto.charenc.UTF8.stringToBytes(IV), asBytes: true, mode: MODE};
// var encrypted = Crypto.AES.encrypt(input_bytes, key, options);
// var encrypted_hex = Crypto.util.bytesToHex(encrypted);
// console.log(encrypted_hex); // this is the value you send over the wire
// output_bytes = Crypto.util.hexToBytes(encrypted_hex);
// output_plaintext_bytes = Crypto.AES.decrypt(output_bytes, key, options);
// output_plaintext = Crypto.charenc.UTF8.bytesToString(output_plaintext_bytes);
// console.log(output_plaintext); // result: 'The answer is no'

var publicKey = ("-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVLVq7BCbYVSj3SmVaAcvaN3LXcR701ZTNLfiSUOfDFAr0g+A29RNQxxc5+nK+TXiIbIzNgjostC23zN16xEAZrilX4xzABe6jz89+KTJyeWWTTMstpL4v73nt9e/8q/euIEdzGzMhSLNpIPe8UTusV51pfqGjCKAjG7ow3X8JuQIDAQAB-----END PUBLIC KEY-----");
// var secretMessage = "user input goes here";
// var encrypted = publicKey.encrypt(secretMessage, "RSA-OAEP", {
//             md: forge.md.sha256.create(),
//             mgf1: forge.mgf1.create()
//         });
// var base64 = forge.util.encode64(encrypted);

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
// console.log(encryptStringWithXORtoHex('plaintext1234wpm','secretkeeeeey'))

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

/*
 * The typing test stuff
 */

var character_length = 31;
var index = 0;
var letters =  $("#type_text").val();
var started = false;
var current_string = letters.substring(index, index + character_length);
var start_time;
var wordcount = 0;

$("html, body").click(function(){
  $("#textarea").focus();
});

$("#target").text(current_string);
$(window).keypress(function(evt){
  if(complete)
    return;

  if(!started){
    start();
    started = true;
  }
  evt = evt || window.event;
  var charCode = evt.which || evt.keyCode;
  var charTyped = String.fromCharCode(charCode);
  if(charTyped == letters.charAt(index)){
    if(charTyped == " "){
      wordcount ++;
      $("#wordcount").text(wordcount);
    }
    all_keys.push(charTyped, new Date().getTime() - start_time );
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
        finished();
    }
  }else{
		element = $("#typewrapper")
		element.removeClass("mistake")
		setTimeout(function () {
				element.addClass("mistake")
			}, 1);
    $("#your-attempt").append("<span class='wrong'>" + charTyped + "</span>");
    errors ++;
    $("#errors").text(errors);
  }
});

var timer = 0;
var wpm = 0;
var all_keys = [];
var wpm_list = [];
var errors = 0;
var interval_timer;
var complete = false;

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
}

function finished(){


  var data = 	{
  			speed: wpm,
        hash: encryptStringWithXORtoHex(wpm.toString().repeat(10),'secretkeeeeey'),
        all_keys:all_keys,
        wpm_history:wpm_list,
        errors:errors
  	};

  $.ajax({
      type: 'POST',
      contentType: 'application/json',
      url: '/postscore',
      dataType : 'json',
      data : JSON.stringify(data),
      success : function(result) {
        console.log(result);
      },error : function(result){
         console.log(result);
      }
  });

	// $.post("/postscore",
	// {
	// 		speed: wpm,
  //     hash: encryptStringWithXORtoHex(wpm.toString().repeat(10),'secretkeeeeey'),
  //     all_keys:all_keys,
  //     wpm_history:wpm_list,
  //     errors:errors
	// },
	// function(data, status){
	// 		console.log("Data: " + data + "\nStatus: " + status);
	// });

  alert("Congratulations!\nWords per minute: " + wpm + "\nWordcount: " + wordcount + "\nErrors:" + errors);
}

var window_focus;

$(window).focus(function() {
    window_focus = true;
}).blur(function() {
  window_focus = false;
});

$(document).ready(function(){
  if(window_focus){
    $("#focus").hide();
  }
  $(window).focus(function() {
    $("#focus").hide();
  });
});
