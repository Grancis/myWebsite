_blog_id="";

function createListItem(user_name,content,create_at){
    card_box=$('<div class="card-comment col-md-8 col-md-offset-2 col-xs-12"></div>');
    card_name=$('<div id="card-name"></div>');
    $(card_name).css("background-color",getRandomRGB());
    label_name=$('<label id="name">'+user_name.substring(0,1)+'</label>');
    card_content=$('<div id="card-content"></div>');
    card_content_p=$('<p id="card-content-p"><strong>'+user_name+':</strong>'+content+'</p>');
    br=$('<br>');
    card_date=$('<div class="card-date"></div>');
    label_date=$('<label id="date">'+create_at+'</label>');

    $(card_date).append(label_date);
    $(card_content).append(card_content_p);
    $(card_content).append(br);
    $(card_name).append(label_name);
    $(card_box).append(card_name);
    $(card_box).append(card_content);
    $(card_box).append(card_date)

    return card_box;
}

$(document).ready(function () {
    $("#box-content").html($("#box-content").text())
    _blog_id=$('input[name="blog_id"]').val();
    nextPage();
});

function addComment(){
    comment=$('textarea[name="comment"]').val()
    $.ajax({
        type:"post",
        url:"/api/add_comment",
        dataType:"json",
        data:{
            "blog_id":_blog_id,
            "content":comment
        },
        success: function(rs){
            if(rs.error=="none"){
                _page=0;
                nextPage();
            }
            else{
                alert(rs.error);
            }
        },
        error: function(){
            alert("请重试或联系管理员")
        }
    })
}