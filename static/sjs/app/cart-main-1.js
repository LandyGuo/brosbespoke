/* 购物车 */
define(function (require) {
    var $ = require('jquery'),
        modal = require("sjs/utils/bb-modal");
    require("jquery.hammer");

    $(function(){
        function showTips(txt, time, status) {
            var htmlCon = '';
            if (txt != '') {
                if (status != 0 && status != undefined) {
                    htmlCon = '<div class="tipsBox" style="width:220px;padding:10px;background-color:#4AAF33;border-radius:4px;-webkit-border-radius: 4px;-moz-border-radius: 4px;color:#fff;box-shadow:0 0 3px #ddd inset;-webkit-box-shadow: 0 0 3px #ddd inset;text-align:center;position:fixed;top:25%;left:50%;z-index:999999;margin-left:-120px;"><img src="/static/images/gouw/ok.png" style="vertical-align: middle;margin-right:5px;" alt="OK，"/>' + txt + '</div>';
                } else {
                    htmlCon = '<div class="tipsBox" style="width:220px;padding:10px;background-color:#D84C31;border-radius:4px;-webkit-border-radius: 4px;-moz-border-radius: 4px;color:#fff;box-shadow:0 0 3px #ddd inset;-webkit-box-shadow: 0 0 3px #ddd inset;text-align:center;position:fixed;top:25%;left:50%;z-index:999999;margin-left:-120px;"><img src="/static/images/gouw/err.png"" style="vertical-align: middle;margin-right:5px;" alt="Error，"/>' + txt + '</div>';
                }
                $('body').prepend(htmlCon);
                if (time == '' || time == undefined) {
                    time = 1500;
                }
                setTimeout(function () {
                    $('.tipsBox').remove();
                }, time);
            }
        }

        $("a[class='jsbtn']").click(function(){
            if(!$(".carpro").length) {
                showTips("购物车为空！");
                return;
            }

            if(!parseInt($("span.jsmoney .ex-pri").text())) {
                showTips("未选中任何商品！");
                return;
            }

            var useCoupon = $(".check-coupon input[type=checkbox]").is(":checked");

            var userChose = new Array();
            $(".check1 :checkbox:checked").each(function () {
                userChose.push($(this).val());
            });
            var userChose = userChose.toString() ;
            //alert(userChose);
            //begin upload
            $.post('/wap/cart_post/', {
                'id':userChose
            },
                function(returnedData,status){
                    if(status=='success'){
                        if(useCoupon) {
                            window.location.href = "/wap/redpacket_view"
                        } else {
                            window.location.href = "/wap/address_list";
                        }
                    }
                }
            );
            //end upload
            return false;
        });
        //
        //价格动态变化
        $(".checkboxWrap label").on("click", function (e) {
            e.preventDefault();
            var $elem = $(this).prev();
            if($elem.is(":checked")) {
                $elem.prop("checked", false);
            } else {
                $elem.prop("checked", true);
            }

            if($(this).parent().hasClass("check1")) {
                var priceText = $("span.jsmoney .ex-pri").text();
                var price = parseInt(priceText);
                var priceadd = $(this).closest('.pro-wrap').find(".ex-pri").text();
                priceadd = parseInt(priceadd);
                if ($elem.is(':checked')) {
                    price += priceadd;
                }
                else {
                    price -= priceadd;
                }
                $("span.jsmoney .ex-pri").html(price);
            }
        });

        function delCarPro(e) {
            e.preventDefault();
            e.stopPropagation();
            var $elem = $(e.currentTarget);
            var cart_id = $elem.parent().attr("data-pro-id");

            modal.openModal({
                content: '<div style="text-align: center;">您确认删除这件商品么？</div>',
                submit: function() {
                    $.ajax({
                        type: "post",
                        url: "/wap/cart_delete_post/",
                        data: {
                            cart_id:cart_id
                        },
                        success: function(res) {
                            if(res.code == 0) {
                                showTips("删除成功", '', 1);
                                $(".cnume").text(parseInt($(".cnume").text()) - 1);
                                //价格
                                var priceText = $("span.jsmoney .ex-pri").text();
                                var price = parseInt(priceText);
                                var priceadd = $elem.closest('.carpro').find(".ex-pri").text();
                                price -= priceadd;
                                $("span.jsmoney .ex-pri").html(price);
                                $elem.parent().remove();
                            } else {
                                showTips(res.msg);
                            }
                        }
                    });
                    return true;
                }
            });
        }

        var carMovedObj = {};//0为默认状态，1为显示删除
        var CARMAXMOVE = 90;
        $(".carpro").hammer().on("panstart", function(e) {
            var dataID = $(this).attr("data-pro-id")

            var leftO = $(this).find(".prolist").css("left");
            if(parseInt(leftO) == 0) {
                carMovedObj[dataID] = 0;
                $(".prolist").css("left", "0px");
                $(".carpro-del").css("right", "-90px");
            } else {
                carMovedObj[dataID] = 1;
            }
        });
        $(".carpro").hammer().on("panmove", function(e) {
            var dataID = $(this).attr("data-pro-id");
            if(!(e.gesture.direction == 2 || e.gesture.direction == 4)) {
                return;
            }
            var deltaX = e.gesture.deltaX;
            var curP;
            if(carMovedObj[dataID] == 0) {
                curP = deltaX;
            } else {
                curP = deltaX - CARMAXMOVE;

            }

            if(curP < 0 && curP > -CARMAXMOVE) {
                //左边
                $(this).find(".prolist").css("left", curP + "px");
                 //删除按钮
                if(!$(this).find(".carpro-del").length) {
                    $(this).append('<div class="carpro-del">删除</div>');
                    $(this).find(".carpro-del").on("click", delCarPro);
                }
                $(this).find(".carpro-del").css("right", - CARMAXMOVE - curP + "px");
            }
        });

        $(".carpro").hammer().on("panend", function(e) {
            var dataID = $(this).attr("data-pro-id");

            var deltaX = e.gesture.deltaX;
            var lastP;
            if(carMovedObj[dataID] == 0) {
                lastP = deltaX;
            } else {
                lastP = deltaX - CARMAXMOVE;
            }
            if(lastP < -CARMAXMOVE/2) {
                $(this).find(".prolist").css("left", - CARMAXMOVE + "px");
                $(this).find(".carpro-del").css("right", "0px");
            } else {
                $(this).find(".prolist").css("left", "0px");
                $(this).find(".carpro-del").css("right", -CARMAXMOVE + "px");
            }
        });
    });
});