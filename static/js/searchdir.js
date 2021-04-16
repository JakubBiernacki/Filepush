const button =  document.querySelector('#codebutton')
const codefield =  document.querySelector('#hero-field')
const info =  document.querySelector('#code-info')


button.addEventListener('click', async (e) => {
    let code = codefield.value

    const wynik = await fetch(`/api/sharedir/${code}/`).then(response => {
        
        if(response.status === 200){
            return response.json()
        }

    })

    if(wynik){
        window.location.href = wynik.link;
    }
    else{
        codefield.style.borderColor = "red";
        codefield.style.borderWidth = "medium";
        info.innerHTML = 'Kod jest nieprawidłowy'
        info.style.color = 'red'

    }


})