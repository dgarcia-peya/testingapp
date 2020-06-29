// Query Automation creation form submit function
let queryAutomationSubmit = e => {

    e.preventDefault()

    let error = ""

    let form = e.target

    if (error == "") {
        fetch("/query_automation/save_query_automation",
        {
            method: "POST",
            body: serializeToJson(form),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                if (data.field !== undefined) {
                    alert(`Error on field ${data.field}:\n${data.error}`)
                } else {
                    alert(`Generic Error:\n${data.error}`)
                }
            } else {
                redirection_path = '/query_automation/detail/'
                redirection_path += `${document.getElementById('destination_dataset').value}-`
                redirection_path += `${document.getElementById('destination_table').value}`
                window.location.href = redirection_path
            }
        })
    } else {
        alert(error)
    }

    return false

}
