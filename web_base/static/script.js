var sleepSetTimeout_ctrl;

let tog = (modId) => {
    $(`.ui.tiny.modal#${modId}`).modal('setting', 'transition', 'vertical flip').modal('toggle')
}

let col = (modId) => {
    for (let x of $(`.ui.tiny.modal#${modId} input`)) {
        x.value = ''
    }

    $(`.ui.tiny.modal#${modId}`).modal('setting', 'transition', 'vertical flip').modal('toggle')
}

let notify = async (nump, jsonResponse) => {
    $.toast({
        displayTime: 2000,
        title: `A new device`,
        message: `Device ${nump} is being registered`,
    })

    await sleep(2000)

    $('.ui.tiny.modal#showDevicePassword .header').text(`Password for ${nump}`)
    $('.ui.tiny.modal#showDevicePassword #pasd').val(jsonResponse['pasd'])
    tog('showDevicePassword')
}

let copyToClipboard = (input) => {
    input.select()
    input.setSelectionRange(0, 99999)

    navigator.clipboard.writeText(input.value)
}

let sleep = (ms) => {
    clearInterval(sleepSetTimeout_ctrl);
    return new Promise(resolve => sleepSetTimeout_ctrl = setTimeout(resolve, ms));
}

let logOut = async () => {
    formData = new FormData()

    formData.append('csrfmiddlewaretoken', document.querySelector("input[name='csrfmiddlewaretoken']").value)

    await fetch('../api/logOut', {
        body: formData,
        method: 'POST'
    }).then((response) => {
        if (response.redirected) {
            window.location.href = response.url
        }
    })
}

let addADevice = async () => {
    formData = new FormData($('.ui.tiny.modal#addADevice form')[0])

    formData.append('csrfmiddlewaretoken', document.querySelector("input[name='csrfmiddlewaretoken']").value)

    await fetch('api/addADevice', {
        body: formData,
        method: 'POST'
    }).then(async (result) => {
        await result.json().then((jsonResponse) => {
            notify(formData.get('nump'), jsonResponse)
            col('addADevice')
        })
    })
}

let deviceLogOut = async() => {
    formData = new FormData()

    formData.append('csrfmiddlewaretoken', document.querySelector("input[name='csrfmiddlewaretoken']").value)

    await fetch('../api/deviceLogOut', {
        body: formData,
        method: 'POST'
    }).then((response) => {
        if (response.redirected) {
            window.location.href = response.url
        }
    })
}