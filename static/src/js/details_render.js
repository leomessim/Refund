odoo.define('Refund.details_render', function (require) {
"use strict";
var ListRenderer = require('web.ListRenderer');

var DetailsListRenderer = ListRenderer.extend({
    start: function () {
        this.$el.addClass('o_lunch_kanban_view position-relative align-content-start flex-grow-1 flex-shrink-1')
        return this._super.apply(this, arguments);
    }
})
return DetailsListRenderer;
});