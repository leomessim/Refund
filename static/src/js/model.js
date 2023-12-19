odoo.define('Refund.model', function (require) {
"use strict";
var ListModel = require('web.ListModel');
var DetailsListModel = ListModel.extend({
    init: function () {
        this._super.appy(this, arguments);
    }
})
return DetailsListModel;
})