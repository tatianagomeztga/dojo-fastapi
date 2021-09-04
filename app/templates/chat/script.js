const client_id = Date.now()
document.querySelector("#ws-id").textContent = client_id;
const ws = new WebSocket(`ws://${window.location.host}/api/web-socket/ws/${client_id}`);
ws.onmessage = function (event) {
    const { data } = event
    let separator = data.indexOf("-")
    const userType = data.substring(0, separator)
    const clientWithMessage = data.substring(separator + 1)
    separator = clientWithMessage.indexOf("-")
    const clientId = clientWithMessage.substring(0, separator)
    const colorId = stringToColour(clientId)
    console.log(colorId)
    const msg = clientWithMessage.substring(separator + 1)

    const messages = document.getElementById('messages')
    const messageContainer = document.createElement('div')

    const messageBox = document.createElement('div')
    messageBox.className = 'messageBox'
    messageBox.style.cssText = `--user-color: ${colorId}`

    const meta = document.createElement('span')
    meta.className = 'meta'

    const badges = document.createElement('span')
    badges.className = 'badges'

    const name = document.createElement('span')
    name.className = 'name'

    const nameContent = document.createTextNode(userType === 'yo' ? 'Yo' : `ID: #${clientId}`)

    const metaBG = document.createElement('i')
    metaBG.className = 'metaBG'

    const message = document.createElement('span')
    message.className = 'message'

    const messageContent = document.createTextNode(msg)

    message.appendChild(messageContent)
    meta.appendChild(badges)
    name.appendChild(nameContent)
    meta.appendChild(name)
    meta.appendChild(metaBG)
    messageBox.appendChild(meta)
    messageBox.appendChild(message)
    messageContainer.appendChild(messageBox)
    messages.appendChild(messageContainer)


};

const sendMessage = (event) => {
    const input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}

const stringToColour = (str) => {
    let hash = 0;
    for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    let colour = '#';
    for (var i = 0; i < 3; i++) {
        var value = (hash >> (i * 8)) & 0xFF;
        colour += ('00' + value.toString(16)).substr(-2);
    }
    return colour;
}