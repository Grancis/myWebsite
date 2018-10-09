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
    window.location.href="/get_blog_list/essay_booking";
}
function itClick(){
    window.location.href="/get_blog_list/essay_it";
}
function newsClick(){
    window.location.href="/get_blog_list/essay_news";
}
function thinkingClick(){
    window.location.href="/get_blog_list/essay_lost_thinking";
}