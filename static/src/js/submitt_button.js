document.getElementById("submit").style.display = "none";
console.log('loaded again')
odoo.define('Refund.Sample', function(require){
    "use strict"
    var rpc =require("web.rpc");
    document.getElementById("vehicle1").addEventListener("click", function() {
    var isAgreed = this.checked;
    if (!isAgreed) {
        document.getElementById("submit").style.display = "none";
        console.log('kkk');
    } else {
        document.getElementById("submit").style.display = "block";
    }
});

})