// update slider q
function outputUpdate(input_id, output_id, num) {
    input_id = '#'+input_id
    output_id = '#'+output_id
    input_element = document.querySelector(input_id)
    output_element = document.querySelector(output_id)
    output_element.value = input_element.value;
}

function printChampName(val) {
    console.log('c1_select value: ' + val)
}

// 1. send simulation input
// 2. simulation on backend
// 3. receive response and display graph and action history on page

$("#champion_select_form").submit(function (e) {
    console.log('submit button clicked')
    // input elements
    var c1_select = document.getElementById('c1_select')
    var c1_q_hit_output = document.getElementById('c1_q_hit_output')
    var c1_w_hit_output = document.getElementById('c1_w_hit_output')
    var c1_e_hit_output = document.getElementById('c1_e_hit_output')
    var c1_r_hit_output = document.getElementById('c1_r_hit_output')
    var c2_select = document.getElementById('c2_select')
    var c2_q_hit_output = document.getElementById('c2_q_hit_output')
    var c2_w_hit_output = document.getElementById('c2_w_hit_output')
    var c2_e_hit_output = document.getElementById('c2_e_hit_output')
    var c2_r_hit_output = document.getElementById('c2_r_hit_output')

    // output elements
    var plot_div = document.getElementById('id_plot_div')
    var action_history = document.getElementById('action_history')
    var c1_name = document.getElementById('c1_name')
    var c2_name = document.getElementById('c2_name')
    var c1_img = document.getElementById('c1_img')
    var c1_win_percent = document.getElementById('c1_win_percent')
    var c2_img = document.getElementById('c2_img')
    var c2_win_percent = document.getElementById('c2_win_percent')

    // input values
    var c1_select_val = c1_select.value
    var c1_q_hit_val = c1_q_hit_output.value
    var c1_w_hit_val = c1_w_hit_output.value
    var c1_e_hit_val = c1_e_hit_output.value
    var c1_r_hit_val = c1_r_hit_output.value

    var c2_select_val = c2_select.value
    var c2_q_hit_val = c2_q_hit_output.value
    var c2_w_hit_val = c2_w_hit_output.value
    var c2_e_hit_val = c2_e_hit_output.value
    var c2_r_hit_val = c1_r_hit_output.value


    // debug
    console.log('c1_select_val: '+c1_select_val)
    console.log('c1_q_hit_val:  '+c1_q_hit_val)
    console.log('c1_w_hit_val:  '+c1_w_hit_val)
    console.log('c1_e_hit_val:  '+c1_e_hit_val)
    console.log('c1_r_hit_val:  '+c1_r_hit_val)
    console.log('c2_select_val: '+c2_select_val)
    console.log('c2_q_hit_val:  '+c2_q_hit_val)
    console.log('c2_w_hit_val:  '+c2_w_hit_val)
    console.log('c2_e_hit_val:  '+c2_e_hit_val)
    console.log('c2_r_hit_val:  '+c2_r_hit_val)

    if(c1_select_val == c2_select_val){
        console.log("Champions can't be the same.")
        alert("Champions can't be the same. Please select different champions and try again.")
        return
    }
    else{
        // GET AJAX request
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: "{% url 'get_simulation_results' %}",
            data: {
            'c1_select_val': c1_select_val,
            'c1_q_hit_val': c1_q_hit_val,
            'c1_w_hit_val': c1_w_hit_val,
            'c1_e_hit_val': c1_e_hit_val,
            'c1_r_hit_val': c1_r_hit_val,
            'c2_select_val': c2_select_val,
            'c2_q_hit_val': c2_q_hit_val,
            'c2_w_hit_val': c2_w_hit_val,
            'c2_e_hit_val': c2_e_hit_val,
            'c2_r_hit_val': c2_r_hit_val
            },
            success: function (response) {
            console.log('response received')
            // update graph
            let new_element = document.createRange().createContextualFragment(response['plot_divider']);
            function removeAllChildNodes(parent) {
                while (parent.firstChild) {
                    parent.removeChild(parent.firstChild);
                }
            }
            removeAllChildNodes(plot_div)
            plot_div.appendChild(new_element)

            // update action history
            action_history.innerHTML = ''
            action_history.innerHTML = response['simulation_results']['action_history'].join('')
            console.log('action_history: '+action_history)

            //update champion name, portrait, and win %
            c1_name.innerHTML = c1_select_val
            c2_name.innerHTML = c2_select_val

            c1_img.setAttribute('src', 'data:image/png;base64,'+response['c1_img'])
            c2_img.setAttribute('src', 'data:image/png;base64,'+response['c2_img'])

            c1_win_percent.innerHTML = 'Win Rate: ' + (Math.round(response['simulation_results']['champion_a_probability']*100)).toString() + '%'
            c2_win_percent.innerHTML = 'Win Rate: ' + (Math.round(response['simulation_results']['champion_b_probability']*100)).toString() + '%'
            },
            error: function (response) {
                console.log(response)
            }
        })
    }
})