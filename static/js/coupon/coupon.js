$(function () {
    var content = $('.content');
    var grapTrue = $('.parent #grap_true');
    var money = $('.money h3');
    var hbNum = $('.hb_num');
    var cloudList = $('.cloudList');
    var submit = $('.submit');
    var share = $('#share');
    var aftershare = $('#aftershare');
    var aftermoney = $('#aftershare .money_bg .money h3');
    var afterphonenum = $('.afterphonenum');
    var full = $('#full');
    var oUl = $('#ul1');
    var newlist = $('#newlist');
        userlist();
        newlist.click(function(){
            oUl.html('');
            userlist();
        });
        //alert('测试勿扰')
        submit.click(function () {
            share.show();
            
        });
    function userlist() {
        $.ajax({
            url: '/promote/redpackettop/',
            /* type:'post',*/
            success: function (json) {
                var arr = json.redpacket_top;
                for (var i = 0; i < arr.length; i++) {
                    var oLi = $('<li class="clearfix"></li>');
                    oLi.html(' <div class="head" style="background:url(' + arr[i].headimgurl + ') no-repeat left top;background-size:cover;" ></div>' +
                        '<div class="date">' +
                        '<span class="fl">' + arr[i].nickname + '</span>' +
                        '<span class="fr">' + arr[i].create_timemonth + '月' + arr[i].create_timeday + '日</span><p class="fl">拆红包的姿势有点厉害</p>' +
                        '</div><span class="price fr">' + arr[i].money + '元</span>');
                    oLi.appendTo(oUl);

                }
            }
        });
    }

    wx.ready(function () {
        // 1 判断当前版本是否支持指定 JS 接口，支持批量判断
        wx.onMenuShareAppMessage({
            title: '师兄的衣柜发红包啦！定制西服衬衫大优惠！', // 分享标题
            desc: '', // 分享描述
            link: 'http://weixin.brosbespoke.com/promote/redpacket/', // 分享链接
            imgUrl: 'http://weixin.brosbespoke.com/static/images/couponimg/Forward.png/', // 分享图标
            type: '', // 分享类型,music、video或link，不填默认为link
            dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
            success: function (obj) {
                // 用户确认分享后执行的回调函数
                $.ajax({
                    url: '/promote/forward_post/',
                    type: 'GET',
                    success: function (json) {
                        if (json.code == 0) {
                            /*alert(json.code)*/
                            share.hide();
                            grapTrue.hide();
                            cloudList.hide();
                            aftershare.show();
                            aftermoney.html(json.money + '元');
                            afterphonenum.html('红包已放入' + json.phone + '<span><a href="/promote/all_coupons/">点击查看&gt</a></span>');

                        }
                        else if (json.code == 1) {
                            full.show();
                            share.hide();
                            grapTrue.hide();
                        }
                    }
                });
            },
            fail: function (obj) {
                /* alert(obj);*/
            },
            cancel: function (obj) {
                // 用户取消分享后执行的回调函数
                /* alert(obj);*/
            }
        });


        //分享到朋友圈
        wx.onMenuShareTimeline({
            title: '师兄的衣柜发红包啦！定制西服衬衫大优惠！', // 分享标题
            link: 'http://weixin.brosbespoke.com/promote/redpaket', // 分享链接
            imgUrl: 'http://weixin.brosbespoke.com/static/images/couponimg/Forward.png/', // 分享图标
            success: function (obj) {
                // 用户确认分享后执行的回调函数
                
                $.ajax({
                    url: '/promote/forward_post/',
                    type: 'GET',
                    success: function (json) {
                        /*alert(json.code)*/
                        if (json.code == 0) {
                           /* alert(json.code)*/
                            share.hide();
                            grapTrue.hide();
                            cloudList.hide();
                            aftershare.show();
                            aftermoney.html(json.money + '元');
                            afterphonenum.html('红包已放入' + json.phone + '<span><a href="/promote/all_coupons/">点击查看&gt</a></span>');

                        }
                        else if (json.code == 1) {
                            full.show();
                            share.hide();
                            grapTrue.hide();
                        }
                    }
                });
            },
            fail: function (obj) {

            },
            cancel: function () {
                // 用户取消分享后执行的回调函数
            }
        });
            
    });
    
});