var QUESTION_STATE = (function (QUESTION_STATE) {
    
    const DICT_ENTRY_TEMPLATE = `
<tr class="dict-entry">
    <td class="removeActive">${REMOVE_TEMPLATE}</td>
    <td class="dict-kv">
        <span>Key: </span><div class="dot left-start lineActive sourceNode key-cell source hash-entry"></div>
        <br>
        <span>Value: </span><div class="dot left-start lineActive sourceNode val-cell source"></div>
    </td>
</tr>`

const DICT_TEMPLATE = `<div class="box lineRecipient">
    <span class="box-label">dict</span>
    <table class="grid">
        <tr class="dict-entry">
            <td class="removeActive">${REMOVE_TEMPLATE}</td>
            <td class="dict-kv">
            <span>Key: </span><div class="dot left-start lineActive sourceNode key-cell source hash-entry"></div>
            <br>
            <span>Value: </span><div class="dot left-start lineActive sourceNode val-cell source"></div>
            </td>
        </tr>
        <tr>
            <td class="addDictEntry clickable">+</td>
        </tr>
    </table>
</div>`

QUESTION_STATE.createDict = (json_data=null, lines_to_make=null) => {
    const element = $(DICT_TEMPLATE);

    if (json_data){
        value = json_data["value"];
        element.find(".dict-entry").remove()
        for (entry_data of value) {
            // entry_data is in the format of {“key_id”:{metadata}, “val_id”:{metadata}
            const entry = $(DICT_ENTRY_TEMPLATE);
            let key_object = entry.find(".key-cell");
            let val_object = entry.find(".val-cell");
            
            console.log("entry data", entry_data)
            key_metadata = QUESTION_STATE.get_metadata(entry_data["key_id"]);
            val_metadata = QUESTION_STATE.get_metadata(entry_data["val_id"]);
            // if either the key or the value pointers are fixed, we make the entry fixed
            if (key_metadata.fixed || val_metadata.fixed) {
                entry.find(".remove").removeClass("removeActive");
            }

            QUESTION_STATE.makeLine(key_object, key_metadata, lines_to_make);
            QUESTION_STATE.makeLine(val_object, val_metadata, lines_to_make);
            entry.insertBefore(element.find(".addDictEntry").parent());
        }
    }

    element.on("getJson", function() {
        const element = $(this);
        const value = []
        element.find('.dict-entry').each(function () {
            let key = $(this).find(".key-cell");
            let val = $(this).find(".val-cell");
            let entry = {}
            entry["key_id"] = QUESTION_STATE.processSource(key)
            entry["val_id"] = QUESTION_STATE.processSource(val)
            value.push(entry);
        });
        return value;
    })

    return element;
}

QUESTION_STATE.DROPZONE
    .on('click', '.addDictEntry', function() {
        let newEntry = $(DICT_ENTRY_TEMPLATE)
        newEntry.insertBefore($(this).parent())
    })

    return QUESTION_STATE;
})(QUESTION_STATE || {})