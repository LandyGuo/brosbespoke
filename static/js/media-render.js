function media_render() {
    var id_picture = document.getElementById('id_user').value;
                    var user_name = '';
                      //alert(id_picture);
                    $.get(document.location.origin + '/order/get_user_name/', {user_id: id_picture},

                                        function(data){
                                            //data = JSON.parse(data);
                                            user_name = data['user_name']
                                            document.getElementById('user_name').innerHTML = user_name;});
                    };
window.onfocus = media_render;
alert(id_picture);
document.getElementById('id_user').onchange = media_render;