$(function(){var content=$('.content');var grapTrue=$('.parent #grap_true');var money=$('.money h3');var reg=/^1[3|4|5|8][0-9]\d{8}$/;var hbNum=$('.hb_num');var cloudList=$('.cloudList');var submit=$('.submit');var share=$('#share');var aftershare=$('#aftershare');var aftermoney=$('#aftershare .money_bg .money h3');var afterphonenum=$('.afterphonenum');var full=$('#full');var oUl=$('#ul1');var newlist=$('#newlist');if(navigator.userAgent.match(/ [iPad | iPhone | iPod] /i)){$('#phonenum').css({'width':'82%','height':'30px'});}
if(navigator.userAgent.match(/ android /i)){$('#phonenum').css({'width':'82.03125%','height':'35px'});}
$('#phonenum').on("input",function(){var phone=$('#phonenum').val();if(reg.test(phone)){$('#grab').css({'background':'#F39700','cursor':'auto','pointer-events':'auto'});}
else{$('#grab').css('background','#ccc');$('#grab').css({'cursor':'not-allowed','pointer-events':'none'});}});$('#grab').click(function(){var phone=$('#phonenum').val();$.ajax({type:'POST',url:'/promote/hbphone_post/',data:'hbphone='+phone,success:function(json){if(json.code==0){content.hide();grapTrue.show();cloudList.show();money.html(json.money+'元');hbNum.html('红包已放入'+phone+'<span><a href="/promote/all_coupons/">点击查看&gt</a></span>');userlist();newlist.click(function(){oUl.html('');userlist();});}
else if(json.code==1){full.show();grapTrue.hide();}}})});function userlist(){$.ajax({url:'/promote/redpackettop/',success:function(json){var arr=json.redpacket_top;for(var i=0;i<arr.length;i++){var oLi=$('<li class="clearfix"></li>');oLi.html(' <div class="head" style="background:url('+arr[i].headimgurl+') no-repeat left top;background-size:cover;" ></div>'+'<div class="date">'+'<span class="fl">'+arr[i].nickname+'</span>'+'<span class="fr">'+arr[i].create_timemonth+'月'+arr[i].create_timeday+'日</span><p class="fl">拆红包的姿势有点厉害</p>'+'</div><span class="price fr">'+arr[i].money+'元</span>');oLi.appendTo(oUl);}}});}
wx.ready(function(){wx.onMenuShareAppMessage({title:'师兄的衣柜给您发红包啦！！快来抢吧！！',desc:'',link:'http://weixin.brosbespoke.com/promote/redpacket/',imgUrl:'/static/images/couponimg/Forward.png/',type:'',dataUrl:'',success:function(obj){$.ajax({url:'/promote/forward_post/',type:'POST',success:function(json){if(json.code==0){share.hide();grapTrue.hide();cloudList.hide();aftershare.show();aftermoney.html(json.money+'元');alert(json.money)
afterphonenum.html('红包已放入'+json.phone+'<span><a href="/promote/all_coupons/">点击查看&gt</a></span>');}
else if(json.code==1){full.show();share.hide();grapTrue.hide();}}});},fail:function(obj){},cancel:function(obj){}});wx.onMenuShareTimeline({title:'师兄的衣柜给您发红包啦！！快来抢吧！！',link:'http://weixin.brosbespoke.com/promote/redpaket',imgUrl:'/static/images/couponimg/Forward.png/',success:function(obj){$.ajax({url:'/promote/forward_post/',type:'POST',success:function(json){if(json.code==0){share.hide();grapTrue.hide();cloudList.hide();aftershare.show();aftermoney.html(json.money+'元');afterphonenum.html('红包已放入'+json.phone+'<span><a href="/promote/all_coupons/">点击查看&gt</a></span>');}
else if(json.code==1){full.show();share.hide();grapTrue.hide();}}});},fail:function(obj){},cancel:function(){}});submit.click(function(){share.show();});});});