odoo.define('Refund.DetailsList', function (require) {
"use strict";
var ListController = require('web.ListController');

var DetailsListController = ListController.extend({

    init: function () {
        return this._super.apply(this, arguments);
    },

    start: function () {
        this.$('.o_content').append($('<div>').addClass('o_lunch_kanban'));
        return this._super.apply(this, arguments).then(function () {
            self.$('.o_lunch_kanban').append(self.$('.o_kanban_view'));
        });
    },

    _getViewDomain: async function () {
        return this.model.getLocationDomain();
    },
})
return DetailsListController;
});