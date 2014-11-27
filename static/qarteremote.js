
// handle success for video info request
function onVideoInfoReceived(videoInfo, status)
{
	$('#full_video_title').html("<em>" + videoInfo.video.title + "</em>  -  " + videoInfo.video.date + " (" + videoInfo.video.duration + " m.)");
	$('#video_description').html(videoInfo.video.pitch);
}

// handle error for video info request
function onVideoInfoError(result, status, error)
{
	//TODO
	console.log("onVideoInfoError");
}

// display video information when the mouse goes over a video thumbnail
function onVideoThumbnailMouseOver(event)
{
	// get video item index
	videoId = event.target.id.replace('video_item_', '');

	// get video item info
	$.ajax({
	   url : '/api/1.0/arteplus/video/info/' + videoId,
	   type : 'GET',
	   dataType : 'json',
	   success : onVideoInfoReceived,
	   error : onVideoInfoError
	});
}

// add the video in the download list
function onVideoThumbnailClick(event)
{
	// get video item index
	videoId = event.target.id.replace('video_item_', '');

	//TODO

	// add the video in the download list
//	$.ajax({
//	   url : '/api/1.0/arteplus/video/info/' + videoId,
//	   type : 'GET',
//	   dataType : 'json',
//	   success : onVideoInfoReceived,
//	   error : onVideoInfoError
//	});
}

$(document).ready(function() {
	$('img.medium_video_thumbnail').mouseover(onVideoThumbnailMouseOver);
	$('img.medium_video_thumbnail').click(onVideoThumbnailClick);
});
