odoo.define('Refund.details_view', function (require) {
"use strict";
var DetailsListController = require('Refund.DetailsListController');
var DetailsListModel = require('Refund.DetaisListModel')
var DetailsListRenderer = require('Refund.DetailsListRenderer');

var ListView = require('web.ListView');
var view_registry = require('web.view_registry');

var DetailsListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: DetailsListController,
        Model: DetailsListModel,
        Renderer: DetailsListRenderer,
    }),

    _getViewDomain: function (parent) {
        const model = this.getModel(parent);
        return model.getLocationDomain();
    },
});
view_registry.add('refund_tree_dashboard', DetailsListView);
return DetailsListView;
});