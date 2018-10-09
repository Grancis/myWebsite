_belong_to="coding"
$(document).ready(function(){
    block=$(".block");
    content=$(".content-box")[0];
    i=0;
    setTimeout(showBlock,300);
    setTimeout(showContent,500);

    nextPage();
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
    window.location.href="/get_blog_list/coding_frontEnd";
}
function pythonClick(){
    window.location.href="/get_blog_list/coding_python";
}
function javaClick(){
    window.location.href="/get_blog_list/coding_java";
}
function matlabClick(){
    window.location.href="/get_blog_list/coding_matlab";
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


       
                 