var QUESTION_STATE = (function (QUESTION_STATE) {
    
    BOOL_TEMPLATE = `<div class="box bool lineRecipient">
    <span class="box-label">bool</span>
    <span>True:</span><input class="bool" type="checkbox" value="True">
    </div>`

    NONE_TEMPLATE = `<div class="box none lineRecipient">
        <span>None</span>
    </div>`


    QUESTION_STATE.createBool = (json_data=null, lines_to_make=null) => {
        const element = $(BOOL_TEMPLATE);
        if (json_data){
            metadata = QUESTION_STATE.get_metadata(json_data["value"]);
            element.find('input').prop('checked', metadata.value);
            if (metadata.fixed) {
                element.addClass("fixed");
                element.find('input').prop('disabled', true);
            }
        }
        

        element.on("getJson", function(QUESTION_STATE) {
            return {"value":$(this).children('input').is(':checked'), "fixed":element.hasClass("fixed")};
        })

        return element;
    }

    QUESTION_STATE.createNone = (json_data=null, lines_to_make=null) => {
        const element = $(NONE_TEMPLATE);
        element.on("getJson", function() {
            return null;
        })

        return element;
    }

    QUESTION_STATE.createUnsupported = (json_data=null, lines_to_make=null) => {
        console.log("making unsupported", json_data["value"])
        const element = $(`<div class="box unsupported lineRecipient">
                        ${json_data["value"]}
                    </div>`);
        return element;
    }


    function createConstant(type, json_data=null, lines_to_make=null){
        const element = $(`<div class="box ${type} lineRecipient">
                        <span class="box-label">${type}: </span>
                        <input type="text" name=""  placeholder="..." class="${type}">
                    </div>`)

        if (json_data){
            metadata = QUESTION_STATE.get_metadata(json_data["value"]);
            element.find("input").val(metadata.value);
            if (metadata.fixed) {
                element.addClass("fixed");
                element.find('input').prop('disabled', true);
            }
        }

        element.on("getJson", function(QUESTION_STATE) {
            metadata = {"fixed":element.hasClass("fixed")}
            if (type == "str")
                metadata["value"] = $(this).children("input").val();
            else if (type == "int")
                metadata["value"] = parseInt($(this).children("input").val());
            else
                metadata["value"] = parseFloat($(this).children("input").val());
            return metadata;
        })
        
        return element;
    }



    QUESTION_STATE.createInt = (json_data = null, lines_to_make=null) => {
        return createConstant("int", json_data, lines_to_make)
    }

    QUESTION_STATE.createFloat = (json_data = null, lines_to_make=null) => {
        return createConstant("float", json_data, lines_to_make)
    }

    QUESTION_STATE.createStr = (json_data = null, lines_to_make=null) => {
        return createConstant("str", json_data, lines_to_make)
    }

    function checkFloat(){
        $(this).parent().children('.note').remove();
        if ($(this).val() === "") {
        return;
        }
        const parsed = parseFloat($(this).val()).toString()
        let dec = $(this).val().split(".")[1];
        let mantissa = parseFloat(dec)
        let num = $(this).val().split(".")[0]
        
        if(!($(this).val() === parsed || ((mantissa === 0 || dec === "")  && parsed == num))) {
            $('<span class="note" style="color:red;">not a float</span>').insertAfter($(this))
        }

    }

    function isFloat(val) {
        return /^\d*.?\d*$/.test(val)
    }

    function checkInt(){
        $(this).parent().children('.note').remove();
        if ($(this).val() === "") {
            return;
        }
        if(parseInt($(this).val()).toString() !== $(this).val()){
            $('<span class="note" style="color:red;">not an int</span>').insertAfter($(this))
        }

    }

    function checkStr(){
        $(this).parent().children('.note').remove();
        if ($(this).val() === "") {
            return;
        }
        if (!(/^'[^']*'$/.test($(this).val()) || /^"[^"]*"$/.test($(this).val()))) {
            $('<span class="note" style="color:red;">not an str</span>').insertAfter($(this))
        }
        
        // TODO check if string is valid

    }


    $(document)
        .on('keydown', '.float', checkFloat)
        .on('keyup', '.float', checkFloat)

        .on('keydown', '.int', checkInt)
        .on('keyup', '.int', checkInt)

        .on('keydown', '.str', checkStr)
        .on('keyup', '.str', checkStr)
    return QUESTION_STATE;
})(QUESTION_STATE || {})