function validatePhone(string){
    const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/
    if(string === ""){
        return false
    }
    return (re.test(string))
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(email === ""){
        return false
    }
    return re.test(String(email).toLowerCase());
}

function validateName(name){
    const re = /^[A-Za-z\ ]+$/
    if(name === ""){
        return false
    }
    return re.test(name)
}
function validateInt(num){
    const re = /^[0-9]+$/
    if(num === ""){
        return false
    }
    return re.test(num)
}
function validateMoney(num){
    const re = /^[0-9/.]+$/
    if(num === ""){
        return false
    }
    return re.test(num)
}
function validateEmpty(string){
    if(string === ""){
        return false
    }
    return true
}