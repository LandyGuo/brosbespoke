/**
 * 
 * @authors wangfengquan(you@example.org)
 * @date    2015-05-20 15:48:46
 * @version $Id$
 */
addReady(function(){
    var oWarp=document.getElementById('warp');
    var oNav=getByClass(oWarp,'nav')[0];
    var aNavLi=oNav.children[0].children;
    var downMenu = getByClass(oWarp, 'downMenu')[0];
    var aOl=downMenu.getElementsByTagName('ol');
    var userTxt=document.getElementById('userTxt');
    var timer=null;
     var downMenutimer=null;
     var downMenutimer2=null;
    var downMenutimer3=null;
    //登陆后的用户显示框
    var userTimer=null;
    if(userTxt.innerHTML=="登录"){

    }else{
            var user_box=document.getElementById('user_box');
            var userListLi=user_box.getElementsByTagName("ul")[0].children;
            var exit=document.getElementById('exit');
                userTxt.onmouseover=user_box.onmouseover=function(){
                      clearTimeout(userTimer);
                    user_box.style.display='block';
                };
             userTxt.onmouseout=user_box.onmouseout=function(){
                 clearTimeout(userTimer);
                    userTimer=setTimeout(function(){
                        user_box.style.display='none';
                    },100);
            };

        for(var i=0;i<userListLi.length;i++){
            (function(index){
                 userListLi[i].onclick=function(){
                    if(index != userListLi.length-1){
                         window.location.href="/web/test9/?"+index;
                    }
                }
            })(i);
        }
        exit.onclick=function(){
                ajax({
                    url:'/web/logout_post/',
                    type:'post',
                    success:function(str){
                        var json = eval('('+str+')');
                        if(json.code==0){
                            alert("退出成功");
                            window.location.href="/web/test2/";
                        }
                    }
                });
            };
    }
      //网页脚部弹窗
     //网页脚部弹窗
    var popupbox=document.getElementById("popupbox");
    var popupBtn=document.getElementById('popupBtn');
    var  popupconTxt=document.getElementById("popupconTxt");
    var popup=document.getElementById('popup');
    var conTxt=document.getElementById("conTxt");
    var dragbox=document.getElementById('dragbox');
    var dragblock=document.getElementById("dragblock");
    var popconbox=null;
    var popupLi=popup.children;
    var foot2=document.getElementById("foot2");
    var foot2Li=foot2.children;
    var popnum=popupLi.length-1;
    var dragH=320;
    for(var i=0;i<foot2Li.length;i++){
        popnum++;
        (function(index){
             foot2Li[i].onclick=function(){
                 popupconTxt.children[2].innerHTML='';
                ajax({
                    url:'/web/footer_post/',
                    success:function(str){
                        var arr = eval('('+str+')');
                        var aTmp=arr[index].name.split('|');
                        popupconTxt.children[0].innerHTML=aTmp[0];
                        conTxt.innerHTML='';
                        var oDiv=document.createElement('div');
                            oDiv.id="popconbox";
                         for(var i=0;i<aTmp.length;i++){
                                if( i==0 || i==1){
                                }else{
                                     oDiv.innerHTML+=aTmp[i]+"<br /><br /><br />";
                                }
                            }
                        popupconTxt.children[2].appendChild(oDiv);
                            popupbox.style.display="block";
                             popconbox=document.getElementById('popconbox');
                            var dragblockH=conTxt.offsetHeight/popconbox.offsetHeight*280;
                            if(popconbox.offsetHeight>288){
                                conTxt.style.overflow="hidden";
                                 dragbox.style.display='block';
                            }
                            if(dragblockH<40){
                                dragblockH=40;
                            }
                             dragblock.style.height=dragblockH+'px';
                            popupbox.style.display="block";
                        shandowmove(popupconTxt,0,50);
                    }
                });
            };
        })(popnum)
    }
    for(var i=0;i<popupLi.length;i++){
        (function(index){
                 popupLi[i].onclick=function(){
                     popupconTxt.children[2].innerHTML=""
                    ajax({
                        url:"/web/footer_post/",
                        success:function(str){
                            var arr= eval('('+str+')');
                            console.log(arr);
                            var aTmp=arr[index].name.split('|');
                            popupconTxt.children[0].innerHTML=aTmp[0];
                            conTxt.innerHTML='';
                            var oDiv=document.createElement('div');
                            oDiv.id="popconbox";
                            for(var i=0;i<aTmp.length;i++){
                                if( i==0 || i==1){
                                }else{
                                     oDiv.innerHTML+=aTmp[i]+"<br /><br /><br />";
                                }
                            }
                           popupconTxt.children[2].appendChild(oDiv);
                            popupbox.style.display="block";
                             popconbox=document.getElementById('popconbox');
                            var dragblockH=conTxt.offsetHeight/popconbox.offsetHeight*280;
                            if(popconbox.offsetHeight>288){
                                conTxt.style.overflow="hidden";
                                 dragbox.style.display='block';
                            }
                            if(dragblockH<40){
                                dragblockH=40;
                            }
                             dragblock.style.height=dragblockH+'px';
                            shandowmove(popupconTxt,0,50);
                        }
                    });

                };
        })(i)
    }
        addWheel(conTxt,function(down){
        var MaxTop=dragbox.offsetHeight-dragblock.offsetHeight;
        var MaxTxtTop=popconbox.offsetHeight-280;
        var scale=dragblock.offsetTop/MaxTop;
        if(down){
            dragblock.style.top=dragblock.offsetTop+2+'px';
            if(dragblock.offsetTop>(dragbox.offsetHeight-dragblock.offsetHeight)){
                   dragblock.style.top=dragbox.offsetHeight-dragblock.offsetHeight+'px';
            }
             popconbox.style.top=-MaxTxtTop*scale+'px';
        }else{
            dragblock.style.top=dragblock.offsetTop-2+'px';
            if(dragblock.offsetTop<0){
                dragblock.style.top='0px';
            }

            popconbox.style.top=-MaxTxtTop*scale+'px';
        }
    })
    popupBtn.onclick=function(){
         popupbox.style.display="none";
         dragbox.style.display='none';
        popupconTxt.style.top="-50%";
    };
    popupBtn.onclick=function(){
         popupbox.style.display="none";
          dragbox.style.display='none';
        popupconTxt.style.top="-50%";
    };

    //鼠标滚轮事件
function addWheel(obj, fn){
	function _wheel(ev) {
		var oEvent=ev || event;
		var down=false;
		if (oEvent.wheelDelta){
			down=oEvent.wheelDelta>0 ? false : true;
		} else {
			down=oEvent.detail>0 ? true : false;
		}
		fn && fn(down);
		oEvent.preventDefault && oEvent.preventDefault();
		return false;
	}
	if (window.navigator.userAgent.toLowerCase().indexOf('firefox') != -1) {
		obj.addEventListener('DOMMouseScroll', _wheel, false);
	} else {
		obj.onmousewheel=_wheel;
	}
}
    //以前的旧版本
      //导航栏
    for (var i = 0; i < aNavLi.length; i++) {
        aNavLi[i].index=i;
        aNavLi[i].onmouseenter = function () {
            if(this.index==1 || this.index==2 || this.index==3){
                 clearTimeout(downMenutimer);
                  clearTimeout(downMenutimer2);
                   downMenutimer3=setTimeout(function(){
                        downMenu.style.display = 'block';
                    },300)

                    for(var i=0;i<aOl.length;i++){
                        aOl[i].style.display='none';
                    }
                    aOl[this.index].style.display='block';
            }
            for (var i = 0; i < aNavLi.length; i++) {
                aNavLi[i].children[0].style.color = "#000";
            }
            this.children[0].style.color = "#d2d2d2";
        };
        aNavLi[i].onmouseleave = function () {
               if(this.index!=1 || this.index!=2 || this.index!=3){
                    clearTimeout(downMenutimer);
                     clearTimeout(downMenutimer3);
                     downMenutimer=setTimeout(function(){
                        downMenu.style.display = 'none';
                    },10)
               }
            for (var i = 0; i < aNavLi.length; i++) {
                aNavLi[i].children[0].style.color = "#000";
            }
        };
    }

    downMenu.onmouseenter = function () {
         clearTimeout(downMenutimer);
        this.style.display = 'block';
    };
    downMenu.onmouseleave = function () {
          clearTimeout(downMenutimer);
            var _this=this;
           downMenutimer2=setTimeout(function(){
               _this.style.display = 'none';
           },1)
    };
     //大导航栏传参数
    for(var i=0;i<aNavLi.length;i++){
        (function(index){
            aNavLi[i].onclick=function(){
            ajax({
                url:'/web/menu_post/',
                type:'post',
                data:{
                    'menu':this.children[0].innerHTML
                },
                success:function(str){
                    var json =eval("("+str+")");
                        if(json.code==0){
                           /* switch(index){
                                case 0:
                                     window.location.href="/web/test1/";
                                    break;
                                 case 1:
                                     window.location.href="/web/test1/";
                                    break;
                                case 2:
                                     window.location.href="/web/test1/";
                                    break;
                                 case 3:
                                     window.location.href="/web/test1/";
                                    break;
                                 case 4:
                                     window.location.href="/web/test7/";
                                    break;
                            }*/
                        }
                }
            });
        };
        })(i)
    }
    //小导航栏传参数
     for(var i=0;i<aOl.length;i++){
        var aOlLi=aOl[i].children;
        aOl[i].index=i;

                for(var j=0;j<aOlLi.length;j++){
                    aOlLi.index=j;
                if(aOlLi[j].parentNode.index==1/*||aOlLi[j].parentNode.index==2||aOlLi[j].parentNode.index==3*/){
                var aOlLiUlLi= aOlLi[j].children[1].children;
                var aSpan= aOlLi[j].children[0];
                    aSpan.onclick=function(){
                        ajax({
                            url:'/web/menu_post/',
                            type:'post',
                            data:{
                                 'menu':aNavLi[this.parentNode.parentNode.index].children[0].innerHTML,
                                    'submenu':this.innerHTML
                            },
                            success:function(str){
                                var json=eval('('+str+')');
                                if(json.code==0){
                                    /*window.location.href="/web/test1/";*/
                                }

                            }
                        });
                    };
                for(var k=0;k<aOlLiUlLi.length;k++){
                    aOlLiUlLi[k].onclick=function(){
                        ajax({
                            url:'/web/menu_post/',
                            type:'post',
                            data:{
                                'menu':aNavLi[this.parentNode.parentNode.parentNode.index].children[0].innerHTML,
                                 'subtitle':this.children[0].innerHTML,
                                'submenu':this.parentNode.parentNode.children[0].innerHTML
                            },
                            success:function(str){

                            }
                        });
                };
                }
                 }else{
                    continue;
                }
            }


    }

    var oShadowBox=getByClass(document,'shandowbox')[0];
    var oPhone=getByClass(oWarp,'phone')[0];
    var oWeiXin=getByClass(oWarp,'wechat')[0];
    var oClose=getByClass(oShadowBox,'close');
    var oWeChat=getByClass(oShadowBox,'weixinchat')[0];
    var oCauentUs=getByClass(oShadowBox,'ContactUs')[1];
    var oCauentUs2=oWeChat.children[0];
    oPhone.onclick=function(){
         oShadowBox.style.display='block'; 
         oCauentUs.style.display='block';
         shandowmove(oCauentUs,'0','50')
    };
    oWeiXin.onclick=function(){
        oShadowBox.style.display='block'; 
        oWeChat.style.display='block';
         shandowmove(oCauentUs2,'0','50');

    };
   oClose[1].onclick=oClose[0].onclick=function(){
        oShadowBox.style.display='none';
        oCauentUs.style.display='none'; 
        oWeChat.style.display='none';
         oCauentUs.style.top='-50%';
        oCauentUs2.style.top='-50%';
        focus();
    };
    if(document.getElementById('weixinclose')){
         var weixinclose=document.getElementById('weixinclose');
        addEvent(weixinclose,"click",function(){
             oShadowBox.style.display='none';
               oWeChat.style.display='none';
             oCauentUs2.style.top='-50%';
        });
    }
      //弹出层运动函数封装
    function shandowmove(obj,start,iTarget){
        var count=Math.round(1000/30);
        var speed=0;
        var dis=iTarget-start;
        clearInterval(timer);
        timer=setInterval(function(){
            speed++;
            var a=1-speed/count;
            obj.style.top=start+dis*(1-a*a*a)+'%';
            if(speed==count)
            {
                clearInterval(timer);
            }
        },30);
    }
    //事件绑定
    function addEvent(obj,sEv,fn){
        if(obj.addEventListener){
            obj.addEventListener(sEv,fn.false);
        }else{
            obj.attachEvent("on"+sEv,fn);
        }
    }
})
