const links = document.querySelectorAll('.download')
const file_c = document.querySelector('#file_c')
const down_c = document.querySelector('#down_c')

const showstat = async() => {
    const data = await fetch('/api/statistics/').then(r => r.json())

    file_c.innerHTML = data.files_count
    down_c.innerHTML = data.download_count
}

links.forEach(link => link.addEventListener('click', () => {
    const filename = link.download;
    
    fetch('/api/statistics/',{
        method : 'POST',
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
            },
        body: JSON.stringify({'filename': filename})
    })

    showstat()
    
}))

showstat()
