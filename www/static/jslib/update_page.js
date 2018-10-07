function update(){
    home=$('input[name="home"]').val()
    booking=$('input[name="booking"]').val()
    it=$('input[name="it"]').val()
    news=$('input[name="news"]').val()
    thinking=$('input[name="thinking"]').val()
    coding=$('input[name="coding"]').val()
    photography=$('input[name="photography"]').val()

    $.ajax({
      type:"post",
      url:"/manage/api/update_pages",
      datatype:"json",
      data:{
        "home":home,
        "booking":booking,
        "it":it,
        "news":news,
        "thinking":thinking,
        "coding":coding,
        "photography":photography
      },
      success: function (rs){
        if(rs.error=="none"){
          alert('update succcessfully!');
        }
        else{
          alert(rs.error);
        }
      },
      error: function (e){
        alert('error,check the console')
      }
    })
  }