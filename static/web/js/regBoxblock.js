/**
 * 
 * @authors wangfengquan (you@example.org)
 * @date    2015-05-22 09:58:51
 * @version $Id$
 */
addReady(function(){
    var oWarp=document.getElementById('warp');
    var regBlock=getByClass(oWarp,'regBlock')[0];
    var loginBlock=getByClass(oWarp,'loginblock')[0];
    var regRight=getByClass(oWarp,'login_right')[0];
    var bFlag=false;
    regBlock.onclick=function(){
        if(bFlag){
            move(regRight,{opacity:0},{complete:function(){
                          move(regRight,{left:145});
                          move(loginBlock,{left:145})
            }});

            this.innerHTML='新用户？点击注册';
            bFlag=false;
        }
        else{
            move(regRight,{left:290},{complete:function(){
                move(regRight,{opacity:1})
            }});
            move(loginBlock,{left:0})
            this.innerHTML='不想注册？关闭注册';
            bFlag=true;
        }
      
    };
});
