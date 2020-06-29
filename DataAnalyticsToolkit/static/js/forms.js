// Get the nested select options from a HTTP GET, using a parent selected value
let getNestedOptions = (endpoint, parent, child) => {

    let filter = document.getElementById(parent).value

    fetch(`${endpoint}?filter=${filter}`)
        .then(response => response.json())
        .then(data => {
            let child_select = document.getElementById(child)
            while (child_select.options.length) child_select.remove(0);
            child_select.options.add(new Option('', ''))
            data.forEach((option) => {
                child_select.options.add(new Option(option.name, option.value))
            })
        })

}

let serializeToJson = form => {
    var json_data = {}
    $(form).find(':input').each(function(){
        json_data[this.name] = $(this).val()
    })
    return JSON.stringify(json_data)
}
