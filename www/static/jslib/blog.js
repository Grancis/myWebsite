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
    window.location.href="#";
}
function itClick(){
    window.location.href="#";
}
function newsClick(){
    window.location.href="#";
}
function thinkingClick(){
    window.location.href="#";
}