//  Like Post

function setState(state, id)
{
	$(id).attr("state", state);
}

function delete_post(obj, post_id){


	$.ajax({

		url: $(obj).attr("url"),
		success: function (dat) {
			console.log(dat);
			// $('#')
		},

		error: function (error) {
			console.log(error.responseText);
		},
	});


}


function likeUnlikePost(obj, state, post_id) {
	var likescounttext = ' Like';
	var likescount = (isNaN(parseInt($("#likescount-"+ post_id).html()))) ? 0 : parseInt($("#likescount-"+ post_id).html())
	console.log('likescount - ' + likescount)
	var text = (state == false) ? "Unlike" : "Like";
	var likes_count_state = (state == false) ? likescount + 1 : --likescount;
	var liketext = (likes_count_state > 1) ? likescounttext + 's' : ((likes_count_state == 1) ? likescounttext : '');


	(likes_count_state === 0) ? $("#likescount-"+ post_id).html('') : $("#likescount-"+ post_id).html(likes_count_state) ;

	// $("#likescount").html(likes_count_state)
	$("#liketext-"+ post_id).html('' + liketext);
	$("#postlike-"+ post_id).html('' + text);

	(state == false) ?  $("#postlike-"+post_id).attr('onclick', "likeUnlikePost(this,true,"+post_id+")"): $("#postlike-"+ post_id).attr('onclick',"likeUnlikePost(this,false,"+post_id+")");


	$.ajax({

		url: $(obj).attr("url"),
		data:post_id,
		success: function (dat) {
			console.log(dat);
		},

		error: function (error) {
			console.log(error.responseText);
		},
	});

}

function shareUnsharePost(obj, state, post_id) {

	var sharescounttext = ' Share';
	var sharescount = (isNaN(parseInt($("#sharescount-"+ post_id).html()))) ? 0 : parseInt($("#sharescount-"+post_id).html());
	var text = (state == false) ? "Un-Share" : "Share";
	var shares_count_state = (state == false) ? sharescount + 1 : sharescount - 1;
	var sharetext = (shares_count_state > 1) ? sharescounttext + 's' : (shares_count_state == 1 ? sharescounttext : '');

	console.log('share count - '+shares_count_state);

	(shares_count_state === 0) ? $("#sharescount-"+ post_id).html('') : $("#sharescount-"+ post_id).html(shares_count_state);

	// $("#sharescount").html(shares_count_state);
	$("#sharetext-"+ post_id).html('' + sharetext);
	$("#postshare-"+ post_id).html('' + text);

	//  if state is false 

	(state == false) ?  $("#postshare-"+ post_id).attr('onclick', "shareUnsharePost(this,true,"+post_id+")"): $("#postshare-"+ post_id).attr('onclick',"shareUnsharePost(this,false,"+post_id+")");

	$.ajax({

		url: $(obj).attr("url"),
		success: function (dat) {
			console.log(dat);
		},

		error: function (error) {
			console.log(error.responseText);
		},
	});

}

// Share Post
// $('#postshare').click(function (e) {
	
// 	var sharescounttext = ' Share';
// 	var sharescount = $("sharescount").value();
// 	var text = (state == false) ? " Share" : " Un-Share";
// 	var shares_count_state = (state == false) ? sharescount - 1 : sharescount + 1;
// 	var sharetext = (sharescount > 1) ? sharescounttext + 's' : sharescounttext;
	
// 	$("#sharescount").html(shares_count_state);
// 	$("#sharetext").html('' + sharetext);
// 	$("#postshare").html('' + text);

// //  if state is false 
// (state == false) ? setState(false, '#postshare') : setState(true, '#postshare');

// 	$.ajax({

// 		url: $(this).attr("href"),
// 		success: function (dat) {

// 			console.log(typeof dat);
// 		},

// 		error: function (error) {
// 			console.log(error.responseText);
// 		},
// 	});

// });

// Follow Topic or Board
function follow_topic(obj, state, topic_id) {
	url = $(obj).attr("url");

	// Add the .val() to get the value and change based on that state

	var text = (state == false) ? "Unfollow" : "Follow";

	$("#topicfollow, #topicfollow1").html(text);

	(state == false) ? $("#topicfollow, #topicfollow1").attr('onclick', "follow_topic(this, true,"+topic_id+")"): $("#topicfollow, #topicfollow1").attr('onclick',"follow_topic(this,false,"+topic_id+")");

	$.ajax({
		url: url,
		data:topic_id,
		success: function (dat) {
			console.log(dat);
		},
		error: function (error) {
			console.log(error.responseText);
		},
	});

}

// document.getElementById("boardfollow").addEventListener("click", follow_board, false);

// function follow_board1() {alert('hello world!')}

function follow_board(obj, state, board_id) {
	// alert('hello world');
	url = $(obj).attr("url");

	// Add the .val() to get the value and change based on that state
	var text = (state == false) ? "Unfollow" : "Follow";

	$("#boardfollow, #boardfollow1").html(text);

	(state == false) ?  $("#boardfollow, #boardfollow1").attr('onclick', "follow_board(this,true,"+board_id+")"): $("#boardfollow, #boardfollow1").attr('onclick',"follow_board(this,false,"+board_id+")");

		
	$.ajax({
		url: url,
		data:board_id,
		success: function (dat) {
			console.log(dat);
		},
		error: function (error) {
			console.log(error.responseText);
		},
	});

}


function wrapText(elementID, openTag, closeTag) {
	var textArea = document.getElementById(elementID);
	var len = textArea.value.length;
	var start = textArea.selectionStart;
	var end = textArea.selectionEnd;
	var selectedText = textArea.value.substring(start, end);
	var replacement = openTag + selectedText + closeTag;
	textArea.value = textArea.value.substring(0, start) + replacement + textArea.value.substring(end, len);
	textArea.focus();
	textArea.selectionStart = textArea.selectionEnd = end + openTag.length + closeTag.length;
}

function addText(elementID, tag) {
	var textArea = document.getElementById(elementID);
	var len = textArea.value.length;
	var insertposition = textArea.selectionEnd;
	textArea.value = textArea.value.substring(0, insertposition) + tag + textArea.value.substring(insertposition, len);
	textArea.focus();
	textArea.selectionStart = textArea.selectionEnd = insertposition + tag.length;
}

function toEnd(elementID) {
	var textArea = document.getElementById(elementID);
	textArea.focus();
	textArea.selectionStart = textArea.selectionEnd = textArea.value.length;
}

function handleQuote(req) {
	addText("body", req.responseText);
	document.getElementById("body").focus();
}

function quotePost(post, session) {
	var requesturl = '/getpost?post=' + post + '&session=' + session;
	sendRequest(requesturl, handleQuote);
}