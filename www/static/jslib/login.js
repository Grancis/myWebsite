function change_to_register(){
    login_box=$("#login-box")
    register_box=$("#register-box")
    $(login_box).css("display","none")
    $(register_box).css("display","block")
}

function change_to_login(){
    login_box=$("#login-box")
    register_box=$("#register-box")
    $(register_box).css("display","none")
    $(login_box).css("display","block") 
}

function validateEmail(email) {
    var re = /^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$/;
    return re.test(email.toLowerCase());
}

function login(){
    history_href=document.referrer
    e_error=$('#l-form-error');
    email=$("input[name='l-email']").val();
    passwrd=$("input[name='l-passwrd']").val();
    if (!validateEmail(email)){
        $(e_error).text("邮箱格式错误");
    }
    $.ajax({
        type:'post',
        url:"/api/authenticate",
        dataType:"json",
        data:{
            "email":email,
            "passwrd":passwrd
        },
        success: function(rs){
            if(rs.email==email){
                // alert("注册成功，确认后跳转至原页面");
                //无历史则跳转index
                if(history_href){window.location.href=history_href}
                else{window.location.href="/"}
            }
        },
        error: function(){alert("请重试或联系管理员");}
    })
}

function register(){
    history_href=document.referrer
    error=""
    name = $("#r-name").val();
    // e_email = $("#r-eamil");
    // e_passwrd = $("#r-passwrd");
    // e_com_passwrd = $("#r-com-passwrd");
    e_error=$('#r-form-error');
    email=$("input[name='r-email']").val();
    passwrd=$("input[name='r-passwrd']").val();
    com_passwrd=$("input[name='r-com-passwrd']").val();
    if(!validateEmail(email)){
        error+="邮箱格式错误";
    }
    if (passwrd.length<6){
        error+="，密码长度至少为6位字符";
    }
    if (passwrd!=com_passwrd){
        error+="，两次输入的密码不一致";
    }
    if(error!=""){
        $(e_error).text(error);
    }
    else{
        $.ajax({
            type:"post",
            url:"/api/register_user",
            dataType:"json",
            data:{
                "name":name,
                "email":email,
                "passwrd":passwrd,
            },
            success: function(rs){
                if(rs.email==email){
                    alert("注册成功，确认后跳转至原页面");
                    if(history_href){window.location.href=history_href}
                    else{window.location.href="/"}
                }
            },
            error: function(){alert("请重试或联系管理员")}
        })
    }

}