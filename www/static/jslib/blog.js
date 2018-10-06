$(document).ready(function(){
    cards=$(".card-across");
    i=0;
    setTimeout(show,500);
})

function show(){
    $(cards[i]).css({"opacity":"1","transform":"translateY(0)"});
    i+=1;
    if (i>=4){
        return ;
    }
    else{
        setTimeout(show,500);
    }
}

function bookingClick(){
    window.location.href="/get_blog_list/booking";
}
function itClick(){
    window.location.href="/get_blog_list/it";
}
function newsClick(){
    window.location.href="/get_blog_list/news";
}
function thinkingClick(){
    window.location.href="/get_blog_list/lost_thinking";
}