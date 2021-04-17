const deletebutton = document.querySelectorAll('.x_circle')

const confirmdelete = document.querySelector('#confirm')
const confirmbutton = confirmdelete.querySelector('#confirmbutton')

const dirname = document.querySelector('#dirname')

let active = false
let code

deletebutton.forEach(button => {
    button.addEventListener('click',() => {
        code = button.dataset.code
        dirname.innerText = `Usuwanie: ${code}`
        confirmdelete.style.display = "block";
        active = true
        
        
    })
})


confirmbutton.addEventListener('click', async()=> {
    if(!active)
        return false
    
    

    const resp = await fetch(`/api/sharedir/${code}/`,{
        method : 'DELETE',
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
            }
    })

    if(resp.ok) location.reload()



})


function cancel(){
    confirmdelete.style.display = 'none';
    active = false

}