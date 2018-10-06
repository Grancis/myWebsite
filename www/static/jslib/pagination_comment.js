_page=0;
_max_page=1;
_num=10;
_url="/api/get_comment_list";
function nextPage(){
    if (_page<_max_page){
        //尝试获取下一个page
        next_page=_page+1
        $.ajax({
            type: "post",
            url: _url,
            data: {
                "blog_id":_blog_id,
                "page":next_page,
                "num":_num+""
            },
            dataType: "json",
            success: function (data){
                _page=data.page //当前获取到的page
                $("#page").text(_page);
                _max_page=data.max_page;
                list_box=$('#box-comment');
                $(list_box).children().remove();
                $.each(data.comments,function(i,obj){
                    item=createListItem(obj.user_name,obj.content,obj.create_at);
                    $(list_box).append(item);
                    window.location.href="#box-add-comment";
                })
                
            },
            error: function (e){
                alert("error, inform administrator.");
            }
        })
    }
    else{
        alert("已经到达最后一页啦")
    }
}

function prePage(blogid){
    if(_page>1){
        pre_page=_page-1;
        $.ajax({
            type:"post",
            url:_url,
            data:{
                "blog_id":_blog_id,
                "page":pre_page,
                "num":_num+""
            },
            dataType:"json",
            success: function(data){
                _page=data.page//获得返回的page值
                $("#page").text(_page);//设置当前页面值
                list_box=$('#box-comment');
                $(list_box).children().remove();
                $.each(data.comments,function(i,obj){
                    item=createListItem(obj.user_name,obj.content,obj.create_at);
                    $(list_box).append(item);
                })
                
                window.location.href="#box-add-comment";
                
                
            },
            error: function (e){
                alert("error, inform administrator.");
            }
        })
    }
    else{
        alert("已经是第一页啦");
    }
}