odoo.define('Refund.test_list_view', function (require) {
"use strict";
var Widget = require('web.Widget');

var DetailsListWidget = Widget.extend({
    template: 'DetailsListWidget',

    init: function () {
        this._super.apply(this, arguments)
     },

    willStart: function () {
        return this._supper.apply(this, arguments);
    },

    renderElement: function () {
        this._super.apply(this, arguments);
    },
})
return DetailsListWidget;
})