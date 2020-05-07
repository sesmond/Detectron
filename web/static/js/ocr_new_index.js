let g_do_correct;

$(function(){
    $( "#upload_file" ).change( function () {
        var v = $( this ).val();
        var reader = new FileReader();
        reader.readAsDataURL( this.files[ 0 ] );
        reader.onload = function ( e ) {
            var result = reader.result.split( "," )[ 1 ]
            $( '#file_base64' ).val( result );
        };
    } );

    $('#submit_ocr').click(function() {
        return submit_ocr();
    });
});


function submit_ocr() {
    var img_base64 = $("#file_base64").val()
    var detect_model  =$("#detect_model").val()
    var do_correct  =$("#do_correct").val()
    console.log(do_correct)
    //清空
    $("#small_table  tr:not(:first)").empty("");
    $("#big_image").attr("src","")

    $.ajax({
        url: '../ocr_new',
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data:JSON.stringify({
            'img':img_base64,
            'do_correct': g_do_correct,
            'detect_model':detect_model,
            'do_verbose':true
        }),
        success: function(res){
            if (res.code =='0'){
                // 成功处理逻辑
                load_result(res)
            }else{
                showMessage(res.message)
            }
         },
        error: function(res){
            // 错误时处理逻辑
            debugger
            }
        });
}


function load_result(result) {
    $("#big_image").attr("src","data:image/jpg;base64," + result.image)
    var $table = $("#small_table");
    var small_images =result['small_images']
    small_images.forEach(function (e,i,array) {
        // console.log(i)
        var $tr ='<tr>'
              +'<td width="60%" align="left"><img style="min-height:20px;max-width:95%" src="data:image/jpg;base64,'+e+'"></td>'
              +'<td width="20%">'+result['text'][i]+'</td>'
              +'<td>'+result['text_corrected'][i]+'</td>'
            +'</tr>'
        $table.append($tr)
    });
}



function queryCorrect(is_correct, id) {
    // $("#do_correct").val(is_correct);
    g_do_correct = is_correct
    $("#correct_true").removeClass("btn-primary");
    $("#correct_false").removeClass("btn-primary");
    $("#" + id).addClass("btn-primary");
}



function queryModel(detect_model, id) {
    $("#detect_model").val(detect_model);
    $("#model_ctpn").removeClass("btn-primary");
    $("#model_psenet").removeClass("btn-primary");
    $("#" + id).addClass("btn-primary");
}


function showMessage(message){
    // TODO 暂时alert，之后优化样式
	alert(message)
}