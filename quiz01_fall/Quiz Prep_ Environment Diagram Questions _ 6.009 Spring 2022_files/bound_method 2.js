var QUESTION_STATE = (function (QUESTION_STATE) {
    
    const BOUND_METHOD_TEMPLATE = `<div class="box lineRecipient bound-method">
    <div class="box-label">Bound Method</div>
    <table>
    <tr>
        <td>Instance: </td>
        <td class="relative-box"><div class="dot left-start lineActive instance-source sourceNode source"></div></td>
    </tr>
    <tr>
        <td>Function: </td>
        <td class="relative-box"><div class="dot left-start lineActive function-source sourceNode source"></div></td>
    </tr>
    </table>
    </div>`



    QUESTION_STATE.createBoundMethod = (json_data = null, lines_to_make = null) => {
        // value should be a dictionary of the type {"instance": {}, "function": {}}
        element = $(BOUND_METHOD_TEMPLATE);


        if (json_data) {
            value = json_data["value"];
            if (value["instance"] !== null) {
                QUESTION_STATE.makeLine(element.find(".instance-source"), QUESTION_STATE.get_metadata(value["instance"]), lines_to_make);
            }
            if (value["function"] !== null) {
                QUESTION_STATE.makeLine(element.find(".function-source"), QUESTION_STATE.get_metadata(value["function"]), lines_to_make);

            }
        }

        element.on("getJson", function() {
            const element = $(this);
            const instance = QUESTION_STATE.processSource(element.find(".instance-source"));
            const func = QUESTION_STATE.processSource(element.find(".function-source"));
            return {"instance":instance, "function": func};
        })

        console.log("returning bound method elt", element)
        return element;
    }

    return QUESTION_STATE;
})(QUESTION_STATE || {})