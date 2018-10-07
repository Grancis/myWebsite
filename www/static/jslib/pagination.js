_page=0;
_max_page=1;
_num=7;
_url="/api/get_blog_list";
_belong_to="none";
_subdivide="none";
function nextPage(){
    if (_page<_max_page){
        //尝试获取下一个page
        next_page=_page+1
        $.ajax({
            type: "post",
            url: _url,
            data: {
                "subdivide":_subdivide,
                "belong_to":_belong_to,
                "page":next_page,
                "num":_num+""
            },
            dataType: "json",
            success: function (data){
                _page=data.page //当前获取到的page
                $("#page").text(_page);
                _max_page=data.max_page;
                list_box=$('.box-list')[0];
                cnt=0;
                $(list_box).children().remove();
                $.each(data.blogs,function(i,obj){
                    item=createListItem(obj.id,obj.subdivide,obj.caption,obj.summary,obj.create_at);
                    cnt=cnt+1;
                    if (cnt%2 !=0){
                        $(item).addClass('bkgClear')
                    }
                    $(list_box).append(item);
                })
                
            },
            error: function (e){
                alert(e);
            }
        })
    }
    else{
        alert("已经到达最后一页啦")
    }
}

function prePage(){
    if(_page>1){
        pre_page=_page-1;
        $.ajax({
            type:"post",
            url:_url,
            data:{
                "subdivide":_subdivide,
                "belong_to":_belong_to,
                "page":next_page,
                "num":_num+""
            },
            dataType:"json",
            success: function(data){
                _page=data.page//获得返回的page值
                $("#page").text(_page);//设置当前页面值
                list_box=$('.box-list')[0];
                $(list_box).children().remove();
                $.each(data.blogs,function(i,obj){
                    item=createListItem(obj.id,obj.subdivide,obj.caption,obj.summary,obj.create_at);
                    $(list_box).append(item);
                })
                
                
            },
            error: function (e){
                alert(e);
            }
        })
    }
    else{
        alert("已经是第一页啦");
    }
}