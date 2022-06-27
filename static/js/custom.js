console.log("connected to custom.js")

const setMinDate = (event)=>{
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;
    event.target.min = today;
}

function dateForAppointment(id){
    date = document.querySelector('#app-date-for-'+id).value;
    document.getElementById('date-error').style.display = "none";
    if (date == ""){
        document.getElementById('date-error').style.display = "block";
        return
    }

    target = document.querySelector("#available-times-for-"+id);
    target.innerText = "Wait a moment...."
    document.getElementById('loader-wait').style.display = "block";
}