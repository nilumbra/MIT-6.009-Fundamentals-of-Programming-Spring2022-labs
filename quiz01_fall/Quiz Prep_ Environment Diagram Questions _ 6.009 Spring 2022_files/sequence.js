var QUESTION_STATE = (function (QUESTION_STATE) {
  
    const ENTRY = `<tr>
        <td class="remove removeActive trash-can">${REMOVE_TEMPLATE}</td>
        <td class="sequence-dot-container">
            <div class="dot any-start line lineActive sourceNode source"></div>
        </td>
    </tr>`

    const ADD_ENTRY = `<div class="addEntry clickable">+</div>`

    function sequenceTemplate(type){
        return  $(`<div class="box sequence lineRecipient">
            <span class="box-label">${type}</span>
            <table class="grid seq-content">
            </table>
        </div>`)
    }

    QUESTION_STATE.createList = (json_data=null, lines_to_make=null) => {
        return createSequence("list", json_data, lines_to_make);
    }

    QUESTION_STATE.createTuple = (json_data=null, lines_to_make=null) => {
        return createSequence("tuple", json_data, lines_to_make,);
    }

    function createSequence(type, json_data=null, lines_to_make=null){
        const element = sequenceTemplate(type);

        if (json_data) {
            value = json_data["value"];
            const table = element.find("table");
            for (item of value){
                metadata = QUESTION_STATE.get_metadata(item);
                const lineElt = $(ENTRY);
                if (metadata.fixed) {
                    lineElt.find(".trash-can").removeClass("removeActive");
                }
                
                table.append(lineElt);
                QUESTION_STATE.makeLine(lineElt.find(".dot"), metadata, lines_to_make);


            }
            element.css("min-width", `${15+element.find("tr").length*20}px`)

            if (!json_data["fixed_length"]) {
                element.append(ADD_ENTRY);
            }
        } else {
            element.append(ADD_ENTRY);
        }

        

        element.on("getJson", function() {
            const element = $(this);
            const value = []
            element.find('.sourceNode').each(function () {
                value.push(QUESTION_STATE.processSource($(this)));
            });
            return value;
        })

        element
            .on('click', '.addEntry', function() {
                
                // the sequence box is it's parent, so we go there and then find the sequence table
                box = QUESTION_STATE.getParentBox($(this))
                box.find("table").append($(ENTRY));
                // then we set the size
                box.css("min-width", `${10+box.find("tr").length*20}px`)
                box.css("max-width", `${10+box.find("tr").length*20}px`)
            })

        

        return element;  
            
    }

    

    return QUESTION_STATE;
})(QUESTION_STATE || {})