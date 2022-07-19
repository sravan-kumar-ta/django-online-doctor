var showPayment = (charge, paypal_acc, id, date, time) => {

    // clear button section
    document.getElementById('paypal-button-container-'+id).innerHTML="";

    paypal.Buttons({
        style: {
            shape: 'pill',
            color: 'gold',
            layout: 'vertical',
            label: 'pay',
        },

        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: parseFloat(charge),
                    },
                    payee : {
                        email_address : paypal_acc,
                    }
                }]
            });
        },

        onApprove: function (data, actions) {
            return actions.order.capture().then(function (orderData) {
                var transaction = orderData.purchase_units[0].payments.captures[0];
                if(transaction.status === "COMPLETED"){
                    a = document.querySelector('#successful-payment-'+id);
                    a.href = "/makeappointment/"+id+"/"+date +"/"+time+"/";
                    a.click();
                    alert("Payment Done!");
                }
                else{
                    console.log("payment Failed");
                }
            });
        },

        onError: function (err) {
            console.log(err);
        }
    }).render('#paypal-button-container-'+id);
}