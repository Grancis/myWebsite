_belong_to="photography"

function packUp(id){
    hidden_content=$("#"+id);
    $(hidden_content).css("display","none");
}

function unFold(id){
    hidden_content=$("#"+id);
    $(hidden_content).css("display","inline");
}
function cardContentSwitch(obj){
    
    pri_text=$(obj).text();
    if(pri_text=="More"){
        unFold("hidden-content");
        $(obj).text("pack up");
    }
    else{
        packUp("hidden-content")
        $(obj).text("More");
    }
}
function clickTo(url){
    window.open(url);
}

// realW=window.innerWidth;
// var oldW;
// window.onresize=function(){
//     oldW=realW;
//     if(window.innerWidth)
//         realW=window.innerWidth;
//     else if((document.body)&&(document.body.clientWidth))
//         realW=document.body.clientWidth;
//     else ;
//     if(realW<997&&oldW>997){
//         $("#card-content-switch").click();
//     }
// }


$(document).ready(function () {
    // if (realW>997)
    //     $("#card-content-switch").click();
    videos=$(".video-card");
    videos_num=$(videos).length;
    video_cnt=0;
    content=$(".content-box")[0];
    setTimeout(showVideos,300);
    setTimeout(showContent,300*videos_num+300);

    nextPage();
});
function showVideos(){
    $(videos[video_cnt]).css({"opacity":"1","transform":"translateY(0)"});
    video_cnt+=1;
    if (video_cnt<4){
        setTimeout(showVideos,300);
    }
    else{
        return;
    }
}

function showContent(){
    $(content).css("opacity","1");
}

function createListItem(id,subdivide,caption,suammry,date){
    var box_div=$('<div class="list-item"></div>');
    img_src='../static/image/'+subdivide+'.svg';
    var img=$('<img src='+img_src+' class="list-icon img-responsive">');
    var caption_div=$('<div class="list-info"></div>');
    var link=$('<a href="/get_blog/'+id+'">'+caption+'</a>');
    var date_div=$('<div class="list-date">'+date+'</div>');
    $(caption_div).append(link);
    $(box_div).append(img);
    $(box_div).append(caption_div);
    $(box_div).append(date_div);
    return $(box_div);
}
