$.ajax({
      type: 'POST',
      url: "/rgx1",
      data: JSON.stringify({values}),
      contentType: "application/json;charset=utf-8",
      dataType: "json",
      success: function(data){
        // do something with the received data
      }
    });