$(document).ready(function(){
    block=$(".block");
    content=$(".content-box")[0];
    i=0;
    setTimeout(showBlock,300);
    setTimeout(showContent,1500);
})

function showBlock(){
    $(block[i]).css({"opacity":"1","transform":"translateY(0)"});
    i+=1;
    if (i<4){
        setTimeout(showBlock,300);
    }
    else{
        return;
    }
}

function showContent(){
    $(content).css("opacity","1");
}
function frontEndClick(){
    window.location.href="#";
}
function pythonClick(){
    window.location.href="#";
}
function javaClick(){
    window.location.href="#";
}
function matlabClick(){
    window.location.href="#";
}