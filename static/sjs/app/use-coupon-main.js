/**
 * Created by lhfu on 2015/6/3.
 */
define(function (require) {
    var $ = require('jquery'),
        modal = require("sjs/utils/bb-modal");

    $(function(){
        var ORIGTOTAL = parseInt($(".jsmoney .ex-pri").text());

        function calcCouponTotal() {
            var per, total = 0;
            $(".check-use-coupon input:checked").each(function() {
                per = $(this).closest(".con-container").find(".cou-per-price").text();
                total += parseInt(per);
            });

            $(".cou-price").text(total);
        }

        function calcTotal() {
            var limit = parseInt($(".cou-limit-num").text());
            var total = parseInt($(".cou-price").text());
            var mini = total > limit? limit: total;
            $(".jsmoney .ex-pri").html(ORIGTOTAL - mini);
        }

        //for qq x5
        //价格动态变化
        $(".checkboxWrap label").on("click", function (e) {
            e.preventDefault();
            var $elem = $(this).prev();
            if($elem.is(":checked")) {
                $elem.prop("checked", false);
            } else {
                $elem.prop("checked", true);
            }
            calcCouponTotal();
            calcTotal($elem);
        });

        $(".jsbtn").on("click", function() {
            var limit = parseInt($(".cou-limit-num").text());
            var total = parseInt($(".cou-price").text());
            if(total > limit) {
            //if(1){
                modal.openModal({
                    content: "<span style='color:rgb(149,149,149);'>你本次支付可使用优惠券总金额上限为2000元</span>",
                    cancelText: "我知道了",
                    submitText: ""
                })
            } else {
                var red_packs = [];
                $(".check-use-coupon input[type=checkbox]:checked").each(function() {
                    red_packs.push($(this).attr("data-id"));
                });
                $.ajax({
                    type: "post",
                    url: "/wap/redpacket_post/",
                    data: {
                        redpacket_id: red_packs.toString()
                    },
                    success: function(res){
                        if(res.code == 0) {
                            window.location.href = "/wap/address_list";
                        }
                    }
                })
            }
        });
    })
});