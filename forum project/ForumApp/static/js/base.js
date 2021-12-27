//  Like Post

function setState(state, id)
{
	$(id).attr("state").value(state);
}

// $('#postlike').click(function (e) {
// 	// Change based on state
// 	var likescounttext = ' Like';
// 	var likescount = $("likescount").value();
// 	var text = (state == false) ? " Like" : " Unlike";
// 	var likes_count_state = (state == false) ? likescount - 1 : likescount + 1;
// 	var liketext = (likescount > 1) ? likescounttext + 's' : likescounttext;

// 	$("#likescount").html(likes_count_state);
// 	$("#liketext").html('' + liketext);
// 	$("#postlike").html('' + text);
// 	(state == false) ? setState(false, '#postlike'): setState(true, '#postlike');


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


function likeUnlikePost(obj, state, post_id) {
	var likescounttext = ' Like';
	var likescount = $("likescount").value();
	var text = (state == false) ? " Like" : " Unlike";
	var likes_count_state = (state == false) ? likescount - 1 : likescount + 1;
	var liketext = (likescount > 1) ? likescounttext + 's' : likescounttext;

	$("#likescount").html(likes_count_state);
	$("#liketext").html('' + liketext);
	$("#postlike").html('' + text);
	(state == false) ? setState(false, '#postlike') : setState(true, '#postlike');


	$.ajax({

		url: $(this).attr("href"),
		success: function (dat) {
			console.log(typeof dat);
		},

		error: function (error) {
			console.log(error.responseText);
		},
	});

}

function shareUnsharePost(obj, state, post_id) {

	var sharescounttext = ' Share';
	var sharescount = $("sharescount").value();
	var text = (state == false) ? " Share" : " Un-Share";
	var shares_count_state = (state == false) ? sharescount - 1 : sharescount + 1;
	var sharetext = (sharescount > 1) ? sharescounttext + 's' : sharescounttext;

	$("#sharescount").html(shares_count_state);
	$("#sharetext").html('' + sharetext);
	$("#postshare").html('' + text);

	//  if state is false 
	(state == false) ? setState(false, '#postshare') : setState(true, '#postshare');

	$.ajax({

		url: $(this).attr("href"),
		success: function (dat) {

			console.log(typeof dat);
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
function followUnfollowTopic(obj, state, topic_id) {
	url = $(obj).attr("href");

	// Add the .val() to get the value and change based on that state

	var follow_text = (state == false) ? " Follow" : " Unfollow";
	$(this).html(text);
	$("#topicfollow").html(follow_text);
	(state == false) ? setState(false, '#topicfollow'): setState(true, '#topicfollow');

	$.ajax({

		url: url,
		data:topic_id,
		success: function (dat) {
			console.log(typeof dat);
		},

		error: function (error) {
			console.log(error.responseText);
		},
	});

}

function followBoard(obj, state, board_id) {
	url = $(obj).attr("href");

	// Add the .val() to get the value and change based on that state

	var text = (state == false) ? " Follow" : " Unfollow";
	$(this).html(text);
	$("#boardfollow").html(text);
	(state == false) ? setState(false, '#boardfollow'): setState(true, '#boardfollow');

	$.ajax({

		url: url,
		data:board_id,
		success: function (dat) {

			console.log(typeof dat);
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