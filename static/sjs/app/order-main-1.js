/* 为谁定制 */
define(function (require) {
    var $ = require('jquery'),
        modal = require("sjs/utils/bb-modal");

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
    function openReserveModal() {
        modal.openModal({
            content: "尊敬的用户，我们的数据库里还没有您的尺寸，但可以免费预约上门量体。您希望享受这项服务吗？",
            submit: function() {
                window.location.href = '/wap/reserve_measure';
            }
        });
    }

    $(function () {
        $(".jsbtn").on("click", function(e) {
            e.preventDefault();
            modal.openModal({
                title: "For whom 您要为谁定制？",
                content: '<div class="checkline">' +
                '<div class="checkboxWrap-sm">' +
                '<input type="radio" name="me" id="me" checked="">' +
                '<label for="me"></label>' +
                '</div>' +
                '<span class="chb-tx">我自己</span>' +
                '</div>' +
                '<div class="checkline">' +
                '<div class="checkboxWrap-sm">' +
                '<input type="radio" name="me" id="fri">' +
                '<label for="fri"></label>' +
                '</div>' +
                '<span class="chb-tx">作为礼品</span>' +
                '</div>' +
                '<input type="tel" placeholder="请输入TA的手机号" class="num" id="friend" style="display:none" maxlength=11>',
                extraEvents: {
                    "click .checkline": "doCheck",
                },
                submit: function () {
                    var number = $("input[class='num']").val();
                    var bool = $("#fri").is(":checked");
                    var is4friend = 0;
                    var isMobile = /^(?:13\d|15\d|18\d)\d{5}(\d{3}|\*{3})$/;
                    if (bool) {
                        is4friend = 1;
                        if (!isMobile.test(number)) {
                            showTips('请输入正确的手机号！');
                            return;
                        }
                    }

                    $.post(
                        "/wap/order4who_post/",
                        {
                            "is4friend":is4friend,
                            "phone":number
                        },function(returnedData){
                            if(returnedData.code == 0) {
                                window.location.href = returnedData.url;
                            } else if (returnedData.code == 1) {
                                openReserveModal();
                            } else {
                                showTips("网络忙，请重试");
                            }
                        }
                    );

                    return;
                },
                doCheck: function (e) {
                    e.preventDefault();
                    var $cur = $(e.currentTarget);
                    $cur.find("input").prop("checked", "checked");

                    if ($("#fri").is(':checked')) {
                        document.getElementById('friend').style.display = "block";
                        $("#friend").focus();
                    } else {
                        document.getElementById('friend').style.display = "none";
                    }

                    var $label = $cur.find('label');
                    $(".checkline label").removeClass('active');
                    $label.addClass("active");
                }
            });
        });
    });
});