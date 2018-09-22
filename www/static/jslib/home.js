$(document).ready(function(){
    p=$("#introduction").children("p");
    i=0;
    setTimeout(show,500);
})

function show(){
    $(p[i]).css("opacity","1");
    i+=1;
    if(i>=7){
        return ;
    }
    else{
        setTimeout(show,1000);
    }
}

function blogClick(){
    window.location.href="blog.html";
}
function codingClick(){
    window.location.href="Coding.html";
}
function photographyClick(){
    window.location.href="photography.html";
}
function aboutClick(){
    window.location.href="about.html";
}