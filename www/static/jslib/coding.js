
$(document).ready(function(){
    block=$(".block");
    content=$(".content-box")[0];
    i=0;
    setTimeout(showBlock,300);
    setTimeout(showContent,500);

    nextPage("coding");
})

function showBlock(){
    $(block[i]).css({"opacity":"1","transform":"translateY(0)"});
    i+=1;
    if (i<4){
        setTimeout(showBlock,300);
    }
    else{
        return;
    }
}

function showContent(){
    $(content).css("opacity","1");
}
function frontEndClick(){
    window.location.href="#";
}
function pythonClick(){
    window.location.href="#";
}
function javaClick(){
    window.location.href="#";
}
function matlabClick(){
    window.location.href="#";
}

function createListItem(id,subdivide,caption,suammry,date){
    var box_div=$('<div class="list-item"></div>')
    img_src='../static/image/'+subdivide+'.svg'
    var img=$('<img src='+img_src+' class="list-icon img-responsive">')
    var caption_div=$('<div class="list-info"></div>')
    var link=$('<a href="/get_blog?id='+id+'">'+caption+'</a>')
    var date_div=('<div class="list-date">'+date+'</div>')
    $(caption_div).append(link);
    $(box_div).append(img);
    $(box_div).append(caption_div);
    $(box_div).append(date_div);
    return $(box_div)
}


       
                 