const bioTextArea = document.getElementById('bio')


bioTextArea.addEventListener('click',() => {
    bioTextArea.focus()
    bioTextArea.setSelectionRange(0,0)
})