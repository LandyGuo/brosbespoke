/**
 * Created by lhfu on 2015/6/3.
 */
define(function (require) {
    var $ = require('jquery');

    $(function(){
        $(".checkboxWrap label").on("click", function (e) {
            e.preventDefault();
            var price;
            var $elem = $(this).prev();
            $elem.prop("checked", true);

            if($elem.attr("id") == "MTM") {
                $(".slt-mtm .sec-container").show();
                $(".slt-bespoke .sec-container").hide();
            } else if($elem.attr("id") == "bespoke") {
                $(".slt-bespoke .sec-container").show();
                $(".slt-mtm .sec-container").hide();
            }

            if($elem.attr("id") == "MTM" || $elem.attr('name') == 'type2'){
                price = $("[name=type2]:checked").closest(".sec-title").find(".ex-price").text();
            } else {
                price = $("[name=type3]:checked").closest(".sec-title").find(".ex-price").text();
            }
            $(".jsmoney .ex-pri").html(parseInt(price));
        });

        $(".jsbtn").on("click", function(e) {
            e.preventDefault();
            var add_bespoke, add_majia;
            var suitType = $("[name=type1]:checked").attr("id");
            if(suitType == "MTM") {
                var right = $("[name=type2]:checked").attr("id");
                if(right == 'two-suit') {
                    add_majia = 0;
                } else {
                    add_majia = 1;
                }
                add_bespoke = 0;
            } else {
                var right = $("[name=type3]:checked").attr("id");
                if(right == 'two-h-suit') {
                    add_majia = 0;
                } else {
                    add_majia = 1;
                }
                add_bespoke = 1;
            }


            $.ajax({
                type: 'post',
                url: "/wap/type_post/",
                data: {
                    add_majia: add_majia,
                    add_bespoke: add_bespoke
                },
                success: function(res) {
                    if(res.code == 0) {
                        window.location.href = "/wap/fabric_select/";
                    }
                }
            })
        });
    })
});