/**
 *
 * @authors wangfengquan(you@example.org)
 * @date    2015-05-20 15:14:51
 * @version $Id$
 */
addReady(function () {
    var oWarp = document.getElementById('warp');
    var oFocus2=document.getElementById("focus");
    var oSuit = getByClass(oWarp, 'suit')[0];
    var oShirt = getByClass(oWarp, 'shirt')[0];
    var oNav = getByClass(oWarp, 'nav')[0];
    var aNavLi = oNav.children[0].children;
    var oFocus = getByClass(oWarp, 'focus')[0];
    var oPicUl = getByClass(oFocus, 'pic_box')[0].children[0];
    var aPicLi = null;
    var PicW = '';
    var oCircleLi = getByClass(oFocus, 'circle')[0].children;
    var oShadowBox = getByClass(document, 'shandowbox')[0];
    var oPhone = getByClass(oWarp, 'phone')[0];
    var oWeiXin = getByClass(oWarp, 'wechat')[0];
    var oClose = getByClass(oShadowBox, 'close');
    var oWeChat = getByClass(oShadowBox, 'weixinchat')[0];
    var oCauentUs2=oWeChat.children[0];
    var oCauentUs = getByClass(oShadowBox, 'ContactUs')[1];
    var downMenu = getByClass(oWarp, 'downMenu')[0];
    var aOl=downMenu.getElementsByTagName('ol');
    var focusL = getByClass(oFocus, 'left')[0];
    var focusR = getByClass(oFocus, 'right')[0];
    var userTxt=document.getElementById('userTxt');
    var n = 0;
    var circle=document.getElementById('circle');
    var circleBtn=null;
    var focustimer=null;
    var timer=null;
    var downMenutimer=null;
     var downMenutimer2=null;
    var downMenutimer3=null;

    oPhone.onclick = function () {
        oShadowBox.style.display = 'block';
        oCauentUs.style.display = 'block';
        shandowmove(oCauentUs,'0','50');
        clearInterval(focustimer);
    };
    oWeiXin.onclick = function () {
        oShadowBox.style.display = 'block';
        oWeChat.style.display = 'block';
        shandowmove(oCauentUs2,'0','50');
        clearInterval(focustimer);

    };
    oClose[0].onclick = oClose[1].onclick = function () {
        oShadowBox.style.display = 'none';
        oCauentUs.style.display = 'none';
        oWeChat.style.display = 'none';
        oCauentUs.style.top='-50%';
        oCauentUs2.style.top='-50%';
        focus();
    };
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

    //轮播图获取和海报获取
    ajax({
            url: '/web/home_post/',
            success: function (str) {
                var json = eval('(' + str + ')');
                var arr = json.poster;
                var arr2 = json.focus;
                console.log(json);
                for (var i = 0; i < arr.length; i++) {
                    var oLi = document.createElement('li');
                    oLi.innerHTML = '<a href="javascript:;"><img src="' + arr[i].img + '" alt=""></a>' ;
                    oLi.tit=arr[i].title;
                    if(i<4){
                         oSuit.appendChild(oLi);
                    }else{
                         oShirt.appendChild(oLi);
                    }

                }
                for(var i=0;i<arr2.length;i++){
                    var oLi=document.createElement('li');
                    var oCle=document.createElement('li');
                    oLi.innerHTML="<a href='javascript:;'><img src='"+arr2[i].img+"' alt=''></a>"
                    oCle.innerHTML='<a href="javascript:;"></a>';
                    oLi.title=arr2[i].title;
                    if(i==0){
                        oCle.className='active';
                    }
                    circle.appendChild(oCle);
                    oFocus2.appendChild(oLi);
                }
                aPicLi=oPicUl.children;
                circleBtn=circle.children;
                PicW=aPicLi[0].offsetWidth;
                  //下面是轮播图滚动
                    oPicUl.innerHTML+=oPicUl.innerHTML;
                    oPicUl.style.width = aPicLi[0].offsetWidth * aPicLi.length + 'px';
                        focustimer=setInterval(function(){
                        n++;
                        tabmove();
                        },7000);

                        for(var i=0;i<aPicLi.length;i++){
                            aPicLi[i].onclick=function(){
                                window.location.href="/web/focus/"+this.title;
                            };
                        }
                 //停止轮播图
                oFocus.onmouseover = function () {
                    move(focusL, {opacity: 1});
                    move(focusR, {opacity: 1});
                };
                //这是左右切换按钮 上面
                oFocus.onmouseout = function () {
                    move(focusL, {opacity: 0});
                    move(focusR, {opacity: 0});
                };
                for(var i=0; i<circleBtn.length; i++){
                    (function(index){
                        circleBtn[i].onclick=function(){
                            n=index;
                            tabmove();
                        }
                    })(i);
                }
                focusR.onclick=function(){
                    n++;
                   tabmove();
                };
                focusL.onclick=function(){
                    n--;
                    tabmove();
                };
                //下面的小海报
                var oShop = getByClass(oWarp, 'shop')[0];
                var agoodsLi = oShop.getElementsByTagName('li');
                var aCloarr = [];
                for (var i = 0; i < agoodsLi.length; i++) {
                    //进入产品详情
                    (function (index) {
                        agoodsLi[i].onclick = function () {
                            window.location.href="/web/poster/"+this.tit;
                        };
                    })(i)
                        //小海报移入放大效果
                        agoodsLi[i].onmouseover=function(){
                                poster(this.children[0].children[0],{'width':130,'height':130,'marginLeft':15,'marginTop':15});
                        };
                        agoodsLi[i].onmouseout=function(){
                                poster(this.children[0].children[0],{'width':100,'height':100,'marginLeft':0,'marginTop':0});
                        };

                }
            }
    });
    //海报运动函数封装
    function poster(obj,options){
            var json=options || {};
            var start=0;
            var dis={};
            for(var name in json){
                if(name=='width' || name=='height'){
                    start=100;
                }else{
                    start=0;
                }
                if(json[name]<=start){
                    if(name=='width' || name=='height'){
                        start=130;
                    }else{
                        start=15;
                    }
                    dis[name]=start-json[name];
                }else{
                     dis[name]=json[name]-start;
                }

            }
            var count=Math.round(1000/30);
            var speed=0;
           clearInterval(obj.timer);
            obj.timer=setInterval(function(){
                speed++;
                for(var name in json){
                    var a=1-speed/count;
                    if(name=='width' || name=='height'){

                        if(json[name]==100){
                            start=130;
                            obj.style[name]=start-dis[name]*(1-a*a*a)+'%';
                        } else{
                             start=100;
                             obj.style[name]=start+dis[name]*(1-a*a*a)+'%';
                        }

                        }else{
                            if(json[name]==0){
                                start=-15;
                                obj.style[name]=start+dis[name]*(1-a*a*a)+'%';
                            } else{
                                    start=0;
                                  obj.style[name]=-(start+dis[name]*(1-a*a*a))+'%';
                            }
                        }

                }
                if(speed==count)
                {
                    clearInterval(obj.timer);
                }
            },30);
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
    //上面是头部小按钮；
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

                            /*switch(index){
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
                                   /* window.location.href="/web/test1/"*/
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
    //运动封装
    function tabmove(){
          for (var i = 0; i < oCircleLi.length; i++) {
                oCircleLi[i].className = '';
        }
		if(n<0){
            oCircleLi[(n % circleBtn.length+ circleBtn.length)%circleBtn.length].className = 'active';
		}else{
            oCircleLi[n % circleBtn.length].className = 'active';
		}
          move2(oPicUl, -n * aPicLi[i].offsetWidth,'left',oPicUl.offsetWidth/2);
    }
    //move函数封装
    var left=0;
    function move2(obj,iTarget,type,size){
		var count=Math.round(600/30);
		var start=left;
		var dis=iTarget-start;
		var n=0;
		clearInterval(obj.timer);
		obj.timer=setInterval(function(){
			n++;
			var a=1-n/count;
            left=start+dis*(1-Math.pow(a,3));
			if(left<0){
				obj.style[type]=left%size+'px';
			}else{
				obj.style[type]=(left%size-size)%size+'px';
			}
			if(n==count){
				clearInterval(obj.timer);
			}
		},30);
	}
});