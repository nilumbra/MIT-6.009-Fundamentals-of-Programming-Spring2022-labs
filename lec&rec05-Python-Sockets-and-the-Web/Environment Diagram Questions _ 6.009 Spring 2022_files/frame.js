var QUESTION_STATE = (function (QUESTION_STATE) {

    const FRAME_TEMPLATE = `<div class="box frame frameLineRecipient">
        <span class="box-label">frame</span>
        <div class="dot-container top-dot-container">${QUESTION_STATE.FRAME_DOT_TEMPLATE}</div>
        <table id="frame-content-template" style="display: block">
            <tr style="height:24px;">
                <td></td>
                <td>Name</td>
                <td>Value</td>
            </tr>
        </table>
        <div class = "return-container">
            <div style="float:left;">return:  </div>
            <div style="position:relative; float:left;">
                <div class="dot return-dot left-start line lineActive sourceNode source"></div>
            </div>
        </div>
        
    </div>
    `

    const ENTRY_INACTIVE = `<tr class="assignment">
    <td class="remove">${REMOVE_TEMPLATE}</td>
    <td class="varCol"><input type="text" name="" placeholder="..." class="nextEntry"></td>
    <td class="dot-container relative-box">${QUESTION_STATE.SOURCE_DOT_HORIZ_TEMPLATE}</td>
    </tr>`

    QUESTION_STATE.ENTRY_ACTIVE = `<tr class="assignment">
    <td class="remove removeActive">${REMOVE_TEMPLATE}</td>
    <td class="varCol"><input type="text" name="" placeholder="..." class=""></td>
    <td class="dot-container relative-box"><div class="dot left-start line lineActive sourceNode source"></div></td>
    </tr>`


    QUESTION_STATE.createFrame = (json_data = null, lines_to_make = null) => {
        // value should be a dictionary of the type {"body":"text here", "arguments":["x","y"], parent:4}
        element = $(FRAME_TEMPLATE);
        element.find(".frameSource").addClass("parent-frame-ptr");
        table = element.find("table")

        if (json_data) {
            // console.log("Here json data", json_data)
            value = json_data["value"];
            if (value["is_global"]){
                element.find(".box-label").html("Global Frame")
                element.addClass("is_global")
                element.find(".return-container").remove()
                element.find(".top-dot-container").remove()
                
            }
            

            for (variable in value["assignments"]) {
                const entry = $(QUESTION_STATE.ENTRY_ACTIVE) 
                entry.find("input").val(variable);

                table.append(entry)
                const lineElt = entry.find(".sourceNode")
                metadata = QUESTION_STATE.get_metadata(value["assignments"][variable]);
                if (metadata.fixed || QUESTION_STATE.ALL_FIXED) {
                    entry.find(".remove").removeClass("removeActive");
                    entry.find('input').prop('disabled', true);
                }
                // console.log("metadata for line", metadata)
                QUESTION_STATE.makeLine(lineElt, metadata, lines_to_make);
            }

            if (value["parent"] !== null && value["parent"] !== undefined) {
                QUESTION_STATE.makeLine(element.find(".frameSource"), QUESTION_STATE.get_metadata(value["parent"]), lines_to_make);
            }

            if (value["return"]) {
                QUESTION_STATE.makeLine(element.find(".return-dot"), QUESTION_STATE.get_metadata(value["return"]), lines_to_make);
            }
        }

        if ((!json_data || !json_data["fixed_length"]) && !QUESTION_STATE.ALL_FIXED) {
            table.append(ENTRY_INACTIVE);
        }

        element.on("getJson", function() {
            const frame = $(this);
            const assignments = {};
        
            frame.find(".assignment").each(function () {
                const name = $(this).find(".varCol").find("input").val()
                if (name != "") {
                    const source = $(this).find(".sourceNode")
                    if (name in assignments) {
                        assignments[name] = QUESTION_STATE.processSource(source);
                        assignments[name]["error"] = `Variable ${name} has multiple bindings in some frame.`;
                    } else {
                        assignments[name] = QUESTION_STATE.processSource(source);
                    }
                }
            });
            const name = frame.find(".frame-name").val();
            const parent = QUESTION_STATE.processSource(frame.find(".frameSource"));
            const return_id = QUESTION_STATE.processSource(frame.find(".return-dot"));
            
            return {"name":name, "parent": parent, "return":return_id, "assignments":assignments, "is_global": $(this).hasClass("is_global")};
            
        })

        

        return element;
    }



    QUESTION_STATE.DROPZONE
        .on('keyup', '.nextEntry', function () {
        // remove nextEntry since this row is now active, create a new row
        $(this).removeClass('nextEntry');

        var entry = $(ENTRY_INACTIVE)
        entry.find("input").each(QUESTION_STATE.resizeInput);
        
        // get the table and add in a new row with the copy
        var tr = $(this).parent().parent();
        var table = tr.parent();
        table.append(entry);

        // make the entry that now has a variable name active
        tr.find(".remove").addClass("removeActive")
        tr.find(".line").addClass("lineActive")
        })

    return QUESTION_STATE;
})(QUESTION_STATE || {})