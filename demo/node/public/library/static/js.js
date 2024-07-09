function dismissDisclaimer() {
    disclaimer.classList.add('hidden')
    content.classList.remove('hidden')
    localStorage.setItem('disclaimer-accepted', 'true')
}

function showDisclaimer() {
    disclaimer.classList.remove('hidden')
    content.classList.add('hidden')
    console.log('gne')

}

async function requestMoreInfo(id) {
    const resp = await fetch('/library/info/' + id)
    const text = await resp.text()
    alert(text)
}

if (!localStorage.getItem('disclaimer-accepted')) {
    showDisclaimer()
}