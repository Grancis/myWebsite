function createSubSelect(){
    belong_to=$("#belong_to option:selected").text()
    // options_text;
    if (belong_to=="essay"){
        options_text=new Array("booking","it","news","lost_thinking")
    }
    else if(belong_to=="coding"){
        options_text=new Array("frontEnd","python","java","matlab","ohter")
    }
    else if(belong_to=="photography"){
        options_text=new Array ("pr","ps","ae","other")
    }
    else ;
    select_form=$("#select-form");
    if($("#col-subdivide")){
        $("#col-subdivide").remove()
    }
    div_col=$('<div class="col-md-3 col-xs-6" id="col-subdivide"></div>')
    div_form_group=$('<div class="form-group"></div>')
    div_form=$('<div class="form-group" id="'+belong_to+'" class="subdivide"></div>')
    label=$('<label for="subdivide">具体分类</label>')
    select=$('<select class="form-control" name="subdivide" id="subdivide"></select')
    options= new Array()
    for (i in options_text){
        options.push($('<option>'+options_text[i]+'</option>'))
    }

    for (i in options){
        $(select).append(options[i])
    }
    $(div_form).append(select)
    $(div_form_group).append(label)
    $(div_form_group).append(div_form)
    $(div_col).append(div_form_group)
    $(select_form).append(div_col)

}

$(document).ready(function () {
    createSubSelect()
    $("#belong_to").change(function(){
        // alert("change...")
        createSubSelect()
    })
});

function push_blog(){
    caption=$('input[name="caption"').val();
    summary=$('textarea[name="summary"]').val();
    content=$('textarea[name="content"]').val();
    belong_to=$("#belong_to option:selected").text();
    subdivide=$("#subdivide option:selected").text();
    //检查非空
    if (caption==""){alert("标题不能为空")}
    if (summary==""){alert("摘要不能为空")}
    if (content==""){alert("正文不能为空")}

    $.ajax({
        type:"post",
        url:"/manage/api/push_blog",
        datatype:"json",
        data:{
            "caption":caption,
            "summary":summary,
            "content":content,
            "belong_to":belong_to,
            "subdivide":subdivide
        },
        success: function(rs){
            if(rs.error=="none"){
                cap=rs.blog.caption;
                sum=rs.blog.summary;
                alert("push successfully...\ncaption:"+cap+"\nsummmary:"+sum);
            }
            else{
                alert("请检查后台....\n"+rs.error)
            }
        },
        error: function(e){
            alert("error, check the console");
        }
    })
}