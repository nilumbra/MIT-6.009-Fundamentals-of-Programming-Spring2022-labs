var QUESTION_STATE = (function (QUESTION_STATE) {

    const FUNCTION_TEMPLATE = `<div class="box function child-box lineRecipient">
    <span class="box-label">func</span>
    <div class="dot-container top-dot-container">${QUESTION_STATE.FRAME_DOT_TEMPLATE}</div>
    Arguments: <span class="addArg clickable">${ADD_TEMPLATE}</span>
    <table>
    </table>
    Body:<br>
    <textarea class="function-body"></textarea>
    </div>`

    const ARG_TEMPLATE = `<tr class="argument">
    <td class="remove removeActive">${REMOVE_TEMPLATE}</td>
    <td class="argCol"><input type="text" name="" placeholder="..." ></td>
    </tr>`

    QUESTION_STATE.createFunction = (json_data = null, lines_to_make = null) => {
        // value should be a dictionary of the type {"body":"text here", "arguments":["x","y"], parent:4}
        element = $(FUNCTION_TEMPLATE);
        

        if (json_data) {
            value = json_data["value"]
            body_metadata = QUESTION_STATE.get_metadata(value["body"]);
            console.log("setting textarea html to", body_metadata.value, element.find("textarea"))
            element.find("textarea").html(body_metadata.value);
            if (body_metadata.fixed) {
                element.find("textarea").prop('disabled', true);
            }  


            const arg_table = element.find("table");
            for (arg of value["arguments"]){
                const arg_entry = $(ARG_TEMPLATE);
                metadata = QUESTION_STATE.get_metadata(arg);
                arg_entry.find("input").val(metadata.value);
                if (metadata.fixed) {
                    arg_entry.addClass("fixed");
                    arg_entry.find("input").prop("disabled", true);
                }
                arg_table.append(arg_entry);
            }

            if (json_data["fixed_length"]) {
                element.find(".addArg").css("display", "hidden")
            }
            
            if (value["frame"] !== null) {
                metadata = QUESTION_STATE.get_metadata(value["frame"]);
                QUESTION_STATE.makeLine(element.find(".frameSource"), metadata, lines_to_make);
            }

            
        }

        // init codemirror after populating textarea
        QUESTION_STATE.init_codemirror(element.find("textarea")[0])

        element.on("getJson", function() {
            const element = $(this);
            const frame = QUESTION_STATE.processSource(element.find(".frameSource"));
            const body_metadata = {"value":element.find("textarea").val(), "fixed":$(this).hasClass("fixed-content")};
            const args = [];
        
            element.find(".argument").each(function () {
                const name = $(this).find(".argCol").find("input").val()
                if (name != ""){
                    let metadata = {"value":name, "fixed":$(this).hasClass("fixed")}
                    args.push(metadata);
                }
            });
            return {"frame":frame, "body": body_metadata, "arguments":args};
        })

        return element;
    }

    QUESTION_STATE.DROPZONE
        .on('click', '.addArg', function () {
        const arg_table = $(this).parent().find("table");

        const arg_entry = $(ARG_TEMPLATE);
        arg_table.append(arg_entry);
        QUESTION_STATE.resizeInputs();
        })

    return QUESTION_STATE;
})(QUESTION_STATE || {})


