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