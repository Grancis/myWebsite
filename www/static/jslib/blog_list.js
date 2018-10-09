_subdivide=null;
_num=10;
_id=null;

function wrapper(){
    clickTo(_id);
}

function clickTo(id){
    window.location.href="/get_blog/"+id;
}

function createListItem(id,subdivide,caption,summary,date){
    _id=id;
    var card_blog=$('<div class="card-blog col-md-8 col-md-offset-2 col-xs-12" onclick=clickTo('+'"'+id+'"'+')>'+'</div>')
    var box_caption=$('<div class="box-caption"></div>');
    var c_caption=$('<h1 class="caption">'+caption+'</h1>');
    var box_summary=$('<div class="box-summary"></div>');
    var c_summary=$('<p class="summary">'+summary+'</p>');
    var box_date=$('<div class="box-date"></div>');
    var c_date=$('<label class="date">'+date+'</label>');
    var br=$('<br>')

    $(box_date).append(c_date);
    $(box_summary).append(c_summary);
    $(box_caption).append(c_caption);
    
    $(card_blog).append(box_caption);
    $(card_blog).append(box_summary);
    $(card_blog).append(br);
    $(card_blog).append(box_date);

    return $(card_blog);
}


$(document).ready(function () {
    _subdivide=$('input[name="subdivide"]').val();
    nextPage()
});

