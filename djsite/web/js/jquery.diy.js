/* diy ebook creator jquery */

var int;
function progress() {
	$.getJSON('http://localhost/import-cmd-get-progress/', function(data) {
		if (typeof data[0] === "undefined") {
			var percent = 0;
		}
		else {
			//$('div.ui-progressbar-value').css({'background-image': 'url(/static/img/pbar-ani.gif)'})
			var percent = Number(data[0]['fields']['v']);

			$("#progressbar").progressbar({value: percent});
			$('#progressbar-details').replaceWith('<p id="progressbar-details">' + Number(data[0]['fields']['k']) + ' / ' + Number(data[0]['fields']['m']) + ' ( ' + percent + '% ) ' + '<br/>' + data[0]['fields']['p'] + '</p>')
			if (percent == 100) {
				percent = 0
				clearInterval(int)
				$('#progressbar-details').append('<br/> <span class="success"> Complete </span>');
				//$('div.ui-progressbar-value').css({'background-image': 'url()'})
			}
		}
	})
}

$(document).ready(function(){
	for (var i = 1; i < 20; i++)
        window.clearInterval(i);

	$("#jqueryNext").click(function(event) {
		event.preventDefault();
		$("#dialog-confirm").dialog('open');
	});
	
	$("#left-card").click(function(event) {
		event.preventDefault();
		$.getJSON("/import-cmd-is-valid",
				{src: $('#step3-directory').val(), card: "left",},
				function(data) {
					if (data[0]['error']) {
						alert(data[0]['error'] + ' Please enter a valid photo folder.');
					}
					else if (data[0]['success']) {
						$("#dialog-progress").dialog('open');
						$.getJSON("/import-cmd",{src: $('#step3-directory').val(), card: "left",})
					    int=self.setInterval("progress()",100);						
					}
				},
				"html")
	});
	
	$("#right-card").click(function(event) {
		event.preventDefault();
		$.getJSON("/import-cmd-is-valid",
				{src: $('#step3-directory').val(), card: "right",},
				function(data) {
					if (data[0]['error']) {
						alert(data[0]['error'] + ' Please enter a valid photo folder.');
					}
					else if (data[0]['success']) {
						$("#dialog-progress").dialog('open');
						$.getJSON("/import-cmd",{src: $('#step3-directory').val(), card: "right",})
					    int=self.setInterval("progress()",100);						
					}
				},
				"html")
	});
	
	$("#both-card").click(function(event) {
		event.preventDefault();
		$.getJSON("/import-cmd-is-valid",
				{src: $('#step3-directory').val(), card: "both",},
				function(data) {
					if (data[0]['error']) {
						alert(data[0]['error'] + ' Please enter a valid photo folder.');
					}
					else if (data[0]['success']) {
						$("#dialog-progress").dialog('open');
						$.getJSON("/import-cmd",{src: $('#step3-directory').val(), card: "both",})
					    int=self.setInterval("progress()",100);						
					}
				},
				"html")
	});

	
	$("#step1").click(function(event) {
		$.get(
				"http://localhost/mountpoint",
				{ state: "before" },
				function(data) { $('#step3-directory').val((data)); },
				"html"
			);
	});
	
	$("#step2").click(function(event) {
		$.get(
				"http://localhost/mountpoint",
				{ state: "after" },
				function(data) { $('#step3-directory').val((data)); },
				"html"
			);
	});
	
	$("#dialog-confirm" ).dialog({
			autoOpen: false,
			resizable: true,
			height:340,
			width:460,
			modal: true,
			buttons: {
				"Yes, these are correct": function() {
					$( this ).dialog( "close" );
					$('#jqueryForm').submit();
				},
				'Cancel': function() {
					$( this ).dialog( "close" );
				}
			}
		});
	
	$("#dialog-progress" ).dialog({
		autoOpen: false,
		resizable: true,
		height:440,
		width:560,
		modal: true,
		buttons: {
			"OK": function() {
				$( this ).dialog( "close" );
				clearInterval(int)
			},
			'Cancel': function() {
				$( this ).dialog( "close" );
				clearInterval(int)
			}
		}
	});
})
