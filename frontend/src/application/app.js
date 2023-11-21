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


    const alerts = document.querySelectorAll(".alerts");
    alerts.forEach((alert) => {
        let timeout = alert.getAttribute("data-timeout"); 
        timeout = timeout ? Number(timeout) : null;
        
        if (timeout) {
            setTimeout(() => {
                removeAlert(alert);
            }, timeout);
        }
        
        alert.addEventListener("click", (evt) => {
            evt.preventDefault();
            removeAlert(alert);
        })
    })
}
 