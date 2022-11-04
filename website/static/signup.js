$(document).ready(function () {
    var info = document.querySelector("#info")
    var loginBtn = document.querySelector("#logemail")
    loginBtn.addEventListener("input", (e) => {
        info.style.display = "block"
        fetch("/avail_username?name="+loginBtn.value)
        .then(res => res.json())
        .then(data => {
            json_data = JSON.parse(data)
            if (json_data == true){
                info.innerHTML = "Username already exists"
                info.style.color = "#f70f13"
            }
            else
            {
                info.innerHTML = "Username available"
                info.style.color = "#19ff5b"
            }
        })
    })
    
})
