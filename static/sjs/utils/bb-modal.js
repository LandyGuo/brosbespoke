define([
    'jquery', 'underscore', 'backbone',
    'text!templates/utils/modal.tpl'
], function(
    $, _, Backbone, modalTemplate
) {
    var ModalView = Backbone.View.extend({
        template: _.template(modalTemplate),

        className: "bb-m",

        events: {
            "click .bb-cnl": "cancelR",
            "click .bb-sbt": "submitR",
            "click .bb-btn-one": "cancelR"
        },

        initialize: function() {
            this.render();
        },

        cancelR: function() {
            this.cancel && this.cancel();
            this.remove();
            $('body').css("overflow", "auto");
        },

        submitR: function() {
            if(!(this.submit && this.submit())){
                return;
            }
            this.remove();
            $('body').css("overflow", "auto");
        },

        render: function() {
            this.$el.html(this.template({
                title: this.title,
                content: this.content,
                submitText: this.submitText,
                cancelText: this.cancelText
            }));
            $('body').css("overflow", "hidden").append(this.$el);
            return this;
        }
    });

    var openModal = function(options) {
        var defaults = {
            cancel: undefined,
            submit: undefined,
            submitText: "确定",
            cancelText: "取消"
        };
        var newModalView = ModalView.extend(defaults).extend(options).extend({
            events: function(){
                return _.extend({},ModalView.prototype.events, options.extraEvents);
            }
        });
        var newModal = new newModalView();
    };

    return {
        openModal: openModal
    };
});