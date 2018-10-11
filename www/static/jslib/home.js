$(document).ready(function(){
    p=$("#introduction").children("p");
    cards=$(".card");
    // card_outHeight=new Array($(cards[0]).outerHeight(),$(cards[1]).outerHeight(),$(cards[2]).outerHeight(),$(cards[3]).outerHeight());
    // showCards();
    i=0;
    j=0;
    setTimeout(show,500);
    setTimeout(showCards,800)
})

function show(){
    $(p[i]).css("opacity","1");
    i+=1;
    if(i>=7){
        return ;
    }
    else{
        setTimeout(show,500);
    }
}

function blogClick(){
    window.location.href="/blog";
}
function codingClick(){
    window.location.href="/coding";
}
function photographyClick(){
    window.location.href="/photography";
}
function aboutClick(){
    window.location.href="/about";
}


function showCards(){
    $(cards[j]).css({"opacity":"1","transform":"translateY(0px)"});
    j+=1;
    if (j>=3){
        return ;
    }
    else{
        setTimeout(showCards,800);
    }
}
// function showCards(){
//     $(document).scroll(function(){
//         viewHeight=$(window).scrollTop()+$(window).height();
//         if (viewHeight>card_outHeight[3]){
//             $(cards[0]).css("opacity","1");
//             $(cards[1]).css("opacity","1");
//             $(cards[2]).css("opacity","1");
//             $(cards[3]).css("opacity","1");
//         }
//         else if(viewHeight>card_outHeight[2]){
//             $(cards[2]).css("opacity","1");
//             $(cards[1]).css("opacity","1");
//             $(cards[0]).css("opacity","1");
//         }
//         else if(viewHeight>card_outHeight[1]){
//             $(cards[1]).css("opacity","1");
//             $(cards[0]).css("opacity","1");
//         }
//         else if(viewHeight>card_outHeight[0]){
//             $(cards[0]).css("opacity","1");
//         }
//     })
// }