var QUESTION_STATE = (function (QUESTION_STATE) {

    const CLASS_TEMPLATE = `<div class="box child-box class-box classLineRecipient lineRecipient">
        <span class="box-label">class</span>
        <div class="dot-container top-dot-container">${QUESTION_STATE.CLASS_DOT_TEMPLATE}</div>
    
        Attributes
        <table id="frame-content-template" style="display: block">
            <tr class="assignment template">
            <td class="remove">${REMOVE_TEMPLATE}</td>
            <td class="varCol"><input type="text" name="" placeholder="..." class="nextEntry"></td>
            <td class="relative-box"><div class="dot left-start line sourceNode source"></div></td>
            </tr>
        </table>
    </div>
    `


    QUESTION_STATE.createClass = (json_data = null, lines_to_make = null) => {
        // value should be a dictionary of the type {"body":"text here", "arguments":["x","y"], parent:4}
        element = $(CLASS_TEMPLATE);

        if (json_data) {
            value = json_data["value"];
            for (variable in value["attributes"]) {
                
                const entry = $(QUESTION_STATE.ENTRY_ACTIVE) 
                entry.find("input").val(variable);
                entry.insertBefore(element.find(".template"));
                const lineElt = entry.find(".sourceNode")

                metatdata = QUESTION_STATE.get_metadata(value["attributes"][variable])
                if (metadata.fixed) {
                    entry.find(".remove").removeClass("removeActive");
                    entry.find('input').prop('disabled', true);
                }
                QUESTION_STATE.makeLine(lineElt, metatdata, lines_to_make);
            }

            if (value["parent"]) {
                QUESTION_STATE.makeLine(element.find(".classSource"), QUESTION_STATE.get_metadata(value["parent"]), lines_to_make);
            }
        }

        element.on("getJson", function() {
            const element = $(this);
            const attributes = {};
        
            element.find(".assignment").each(function () {
                const name = $(this).find(".varCol").find("input").val()
                if (name != "") {
                    const source = $(this).find(".sourceNode")
                    attributes[name] = QUESTION_STATE.processSource(source);
                }
            });
            // NOTE we do not support multiple parents
            const parent = QUESTION_STATE.processSource(element.find(".classSource"));
            return {"parent": parent, "attributes":attributes};

        })

        return element;
    }
    return QUESTION_STATE;

})(QUESTION_STATE || {})