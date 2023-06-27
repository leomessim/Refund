document.getElementById("submit").style.display = "none";
console.log('loaded again')
odoo.define('Refund.Sample', function(require){
    "use strict"
    $(document).ready(function() {
        $('#amount_one').on('change', function() {
            console.log('kok');
            var value1 = parseFloat($('#amount_one').val());
            var value2 = parseFloat($('#amount_two').val());
            var value3 = parseFloat($('#amount_three').val());

            var total = (isNaN(value1) ? 0 : value1) + (isNaN(value2) ? 0 : value2) + (isNaN(value3) ? 0 : value3);

            $('#amount_total').val(total.toFixed(2));
        });
        $('#amount_two').on('change', function() {
            console.log('kok');
            var value1 = parseFloat($('#amount_one').val());
            var value2 = parseFloat($('#amount_two').val());
            var value3 = parseFloat($('#amount_three').val());

            var total = (isNaN(value1) ? 0 : value1) + (isNaN(value2) ? 0 : value2) + (isNaN(value3) ? 0 : value3);

            $('#amount_total').val(total.toFixed(2));
        });
        $('#amount_three').on('change', function() {
            console.log('kok');
            var value1 = parseFloat($('#amount_one').val());
            var value2 = parseFloat($('#amount_two').val());
            var value3 = parseFloat($('#amount_three').val());

            var total = (isNaN(value1) ? 0 : value1) + (isNaN(value2) ? 0 : value2) + (isNaN(value3) ? 0 : value3);

            $('#amount_total').val(total.toFixed(2));
        });
    });
//    const input1 = document.getElementById('amount_one');
//    const input2 = document.getElementById('amount_two');
//    const input3 = document.getElementById('amount_three');
//    const result = document.getElementById('amount_total');
//
//    input1.addEventListener('change', calculateSum);
//    input2.addEventListener('change', calculateSum);
//    input3.addEventListener('change', calculateSum);
//
//    function calculateSum() {
//      const value1 = Number(input1.value);
//      const value2 = Number(input2.value);
//      const value3 = Number(input3.value);
//      const sum = value1 + value2 + value3;
//      result.textContent = sum;
//      console.log('kok');
//    }

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