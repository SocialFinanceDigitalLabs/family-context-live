import "../styles/index.scss";
import M from "materialize-css/dist/js/materialize.min";

window.document.addEventListener("DOMContentLoaded", function () {
M.AutoInit();
AlertInit();
});

const AlertInit = () => {
    const removeAlert = (alertref) => {
        alertref.remove();
    }

    let currentTime = 0
    const alerts = document.querySelectorAll(".alerts");
    const timeoutRemoveAlert= (alerts)=>{
        alerts.forEach((alert) => {
            let timeout = alert.getAttribute("data-timeout"); 
            timeout = timeout ? Number(timeout) : null;
            
            if (timeout && timeout>= currentTime) {
                    removeAlert(alert);
            }
        })
    }

    if (alerts.length > 0){
        setInterval(()=>{
            console.log("interval running");
            currentTime += 1000;
            timeoutRemoveAlert(alerts);
        }, 1000)

    }

    alert.forEach.addEventListener("click", (evt) => {
        evt.preventDefault();
        removeAlert(alert);
    })
    
}