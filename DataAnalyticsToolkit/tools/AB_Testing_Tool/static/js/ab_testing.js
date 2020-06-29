// AB Testing creation form submit function
let abTestingSubmit = e => {

    e.preventDefault()

    let error = ""

    let form = e.target

    if (
        Math.round((new Date(document.getElementById('from_date').value) - new Date) / 86400000) > 90 ||
        Math.round((new Date - new Date(document.getElementById('from_date').value)) / 86400000) > 90
    ) {
        error = "The From Date must be between three months before or after"
    }

    if (
        document.getElementById('to_date').value != "" &&
        (new Date(document.getElementById('to_date').value) - new Date(document.getElementById('from_date').value))
        / 86400000 < 1
    ) {
        error = "The To Date must be after the From Date"
    }

    if (error == "") {
        fetch("/ab_testing/save_ab_test",
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
                window.location.href = `/ab_testing/detail/${document.getElementById('ab_test_name').value}`
            }
        })
    } else {
        alert(error)
    }

    return false

}

// Get the mcvr_standard data from configuration
let setMcvrStandrad = e => {

    let test_location = document.getElementById('test_location').value

    fetch(`/ab_testing/get_mcvr_standard?test_location=${test_location}`)
    .then(response => response.json())
    .then(api_data => {
        document.getElementById('mcvr_standard').value = api_data.mcvr_standard
        document.getElementById('mcvr_standard_description').value = api_data.mcvr_standard_descr
    })

}

// Get the FWF Feature data
let getFWFFeature = () => {

    let fields = []

    project = document.getElementById("fwf_project").value
    property = document.getElementById("ab_test_name").value

    fetch(`/ab_testing/get_fwf_property_config?project=${project}&property=${property}`)
    .then(response => response.json())
    .then(api_data => {
        fields.push({"id": "ab_test_control", "value": api_data.offVariation})
        variations = []
        if (api_data.defaultRule !== null && api_data.defaultRule.variation != "Control") {
            variations.push(api_data.defaultRule.variation)
        }
        if (api_data.rules !== null) {
            api_data.rules.forEach((rule) => {
                if (rule.variation != "Control" && !variations.includes(rule.variation)) {
                    variations.push(rule.variation)
                }
            })
        }
        fields.push({"id": "ab_test_variations", "value": variations.join()})
        autocompleteFWFFeaturesFields(fields)
    })

}

// Autocomplete the Flag form fields using the FWF data
let autocompleteFWFFeaturesFields = fields => {
    fields.forEach((field) => {
        document.getElementById(field.id).value = field.value
    })
}

// Format the datetime to date
let formatDate = date_text => {

        dateObject = new Date(date_text)
        year = dateObject.getUTCFullYear()
        if (year < 999) year = 1000

        month = dateObject.getUTCMonth() + 1
        if (month < 10) month = `0${month}`

        date = dateObject.getUTCDate()
        if (date < 10) date = `0${date}`

        return `${year}-${month}-${date}`

}

// The selected AB Test
let current_ab_test = undefined

// Show a modal with some finishing inputs and allow to finish the test
let finishTest = e => {

    current_ab_test = $(e.target).data("id")

    let finsihTestDialog = document.getElementById('finishTestDialog')
    if (typeof finsihTestDialog.showModal === "function") {
        finsihTestDialog.showModal()
    } else {
        alert("The <dialog> API is not supported by this browser")
    }

}

// Send
let finishTestAction = e => {

    e.preventDefault()

    body_data = {
        "ab_test_to_date": $("#ab_test_to_date").datepicker("getFormattedDate"),
        "ab_test_result": document.getElementById("ab_test_result").value,
        "ab_test_explanation": document.getElementById("ab_test_explanation").value,
        "ab_test_name": current_ab_test
    }

    fetch("/ab_testing/finish_ab_test",
    {
        method: "POST",
        body: JSON.stringify(body_data),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error)
        } else {
            alert("AB Test successfully finished")
            document.getElementById('finishTestDialog').close();
        }
    })

}
