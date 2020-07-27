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