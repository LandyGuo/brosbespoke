$(function(){var content=$('.content');var grapTrue=$('.parent #grap_true');var money=$('.money h3');var reg=/^1[3|4|5|8][0-9]\d{8}$/;var hbNum=$('.hb_num');var cloudList=$('.cloudList');var submit=$('.submit');var share=$('#share');var aftershare=$('#aftershare');var aftermoney=$('#aftershare .money_bg .money h3');var afterphonenum=$('.afterphonenum');$('#phonenum').on("input",function(){var phone=$('#phonenum').val();if(reg.test(phone)){$('#grab').css({'background':'#F39700','cursor':'auto','pointer-events':'auto'});}
else{$('#grab').css('background','#ccc');$('#grab').css({'cursor':'not-allowed','pointer-events':'none'});}});$('#grab').click(function(){var phone=$('#phonenum').val();$.ajax({type:'POST',url:'/promote/hbphone_post/',data:'hbphone='+phone,success:function(json){if(json.code==0){content.hide();grapTrue.show();cloudList.show();money.html(json.money+'元');hbNum.html('红包已放入'+phone+'<span><a href="#">点击查看&gt</a></span>');}}})});wx.onMenuShareAppMessage({title:'师兄的衣柜给您发红包啦！！快来抢吧！！',desc:'',link:'http://weixin.brosbespoke.com/promote/redpaket/',imgUrl:'',type:'',dataUrl:'',success:function(obj){alert(obj.errMsg)
$.ajax({url:'/promote/forward_post/',type:'POST',success:function(str){var json=eval('('+str+')');if(json.code==0){grapTrue.show();cloudList.show();aftershare.show();aftermoney.html(json.money+'元');afterphonenum.html('红包已放入'+phone+'<span><a href="#">点击查看&gt</a></span>');}}});},fail:function(obj){alert(obj.errMsg);},cancel:function(){}});wx.onMenuShareTimeline({title:'师兄的衣柜给您发红包啦！！快来抢吧！！',link:'http://weixin.brosbespoke.com/promote/redpaket/',imgUrl:'',success:function(obj){$.ajax({url:'/promote/forward_post/',type:'POST',success:function(str){var json=eval('('+str+')');alert(json);if(json.code==0){grapTrue.show();cloudList.show();aftershare.show();aftermoney.html(json.money+'元');afterphonenum.html('红包已放入'+phone+'<span><a href="#">点击查看&gt</a></span>');}}});},fail:function(obj){alert(obj.errMsg);},cancel:function(){}});submit.click(function(){share.show();});});