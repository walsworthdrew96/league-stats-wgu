/*
    On submiting the form, send the POST ajax
    request to server and after successfull submission
    display the object.
*/
$("#champion-graph-form").submit(function (e) {
    e.preventDefault();
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'GET',
        url: "{% url 'get_graph_data' %}",
        data: serializedData,
        success: function (response) {
            // 1. clear the form.
            $("#champion-graph-form").trigger('reset');
            // 2. focus to nickname input
            $("#id_name").focus();
            // 3. display the new data points on the graph.
//                var instance = JSON.parse(response["instance"]);
//                var fields = instance[0]["fields"];
//                $("#champions_table tbody").prepend(
//                    `<tr>
//                    <td>${fields["name"]||""}</td>
//                    <td>${fields["health"]||""}</td>
//                    </tr>`
//                )
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    })
})
/*
On focus out on input champion name,
call AJAX get request to check if the name
already exists or not.
*/
$("#id_plot_div").focusout(function (e) {
    e.preventDefault();
    // get the name
    var name = $(this).val();
    // GET AJAX request
    $.ajax({
        type: 'GET',
        url: "{% url 'validate_name' %}",
        data: {"name": name},
        success: function (response) {
            // if not valid user, alert the user
            if(!response["valid"]){
                alert("You cannot create a champion with same name");
                var champion_name = $("#id_plot_div");
                champion_name.val("")
                champion_name.focus()
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
})

//get select input item

var select_element = document.getElementById("stat_select")
var option_element = select_element.options[select_element.selectedIndex];
console.log(option_element.value)
console.log(option_element.text)
var selected_stat = option_element.value
var plot_div_element = document.getElementById('id_plot_div')
console.log('plot_div_element: '+plot_div_element)

$("#champion-graph-form").submit(function (e) {
    e.preventDefault();
    selected_stat = select_element.options[select_element.selectedIndex].value
    console.log("selected: "+selected_stat)
    // GET AJAX request
    $.ajax({
        type: 'GET',
        url: "{% url 'get_graph_data' %}",
        data: {'selected_stat': selected_stat},
        success: function (response) {

        let new_element = document.createRange().createContextualFragment(response['plot_divider']);

        function removeAllChildNodes(parent) {
            while (parent.firstChild) {
                parent.removeChild(parent.firstChild);
            }
        }

        removeAllChildNodes(plot_div_element)
        plot_div_element.appendChild(new_element)
        },
        error: function (response) {
            console.log(response)
        }
    })
})

//change_input settings

var select_element = document.getElementById("stat_select")
var option_element = select_element.options[select_element.selectedIndex];
console.log(option_element.value)
console.log(option_element.text)
var selected_stat = option_element.value
var plot_div_element = document.getElementById('id_plot_div')
console.log('plot_div_element: '+plot_div_element)

$("#champion-graph-form").submit(function (e) {
    e.preventDefault();
    selected_stat = select_element.options[select_element.selectedIndex].value
    console.log("selected: "+selected_stat)
    // GET AJAX request
    $.ajax({
        type: 'GET',
        url: "{% url 'get_graph_data' %}",
        data: {'selected_stat': selected_stat},
        success: function (response) {
//        new_graph_html = plot_div_element.write(response['plot_divider'])
//        console.log('new_graph_html: ' + new_graph_html)
//        plot_div_element.innerHTML = new_graph_html

//        document.write(response['plot_divider'])

//        let dom = new DOMParser().parseFromString(response['plot_divider'], 'text/html')
//        let new_element = dom.body.firstElementChild;
//        plot_div_element.innerHTML = new_element

        let new_element = document.createRange().createContextualFragment(response['plot_divider']);

        function removeAllChildNodes(parent) {
            while (parent.firstChild) {
                parent.removeChild(parent.firstChild);
            }
        }
        removeAllChildNodes(plot_div_element)
        plot_div_element.appendChild(new_element)
        },
        error: function (response) {
            console.log(response)
        }
    })
})


//get select input item

var select_element = document.getElementById("stat_select")
var option_element = select_element.options[select_element.selectedIndex];
console.log(option_element.value)
console.log(option_element.text)
var selected_stat = option_element.value
var plot_div_element = document.getElementById('id_plot_div')
console.log('plot_div_element: '+plot_div_element)

$("#champion-graph-form").submit(function (e) {
    e.preventDefault();
    selected_stat = select_element.options[select_element.selectedIndex].value
    console.log("selected: "+selected_stat)
    // GET AJAX request
    $.ajax({
        type: 'GET',
        url: "{% url 'get_graph_data' %}",
        data: {'selected_stat': selected_stat},
        success: function (response) {

        let new_element = document.createRange().createContextualFragment(response['plot_divider']);

        function removeAllChildNodes(parent) {
            while (parent.firstChild) {
                parent.removeChild(parent.firstChild);
            }
        }
        removeAllChildNodes(plot_div_element)
        plot_div_element.appendChild(new_element)
        },
        error: function (response) {
            console.log(response)
        }
    })
})