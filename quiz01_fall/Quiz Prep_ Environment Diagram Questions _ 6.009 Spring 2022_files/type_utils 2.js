var QUESTION_STATE = (function (QUESTION_STATE) {


    QUESTION_STATE.GRID_SIZE = 10;
    QUESTION_STATE.STORED_PATHS = [];
    QUESTION_STATE.STORED_LINES = [];

    // const DOT_TEMPLATE = `<div class="dot"></div>`
    QUESTION_STATE.FRAME_DOT_TEMPLATE = `<div style="relative"><div class="dot line lineActive frameSource source any-start"></div></div>`
    QUESTION_STATE.SOURCE_DOT_HORIZ_TEMPLATE = `<div class="dot left-start line sourceNode source"></div>`
    QUESTION_STATE.CLASS_DOT_TEMPLATE = `<div style="relative"><div class="dot line lineActive classSource source"></div></div>`
    
    // MESSAGING AND WARNINGS
    QUESTION_STATE.notify = (msg) => {
        
        warning_div = QUESTION_STATE.CONTAINER.find(".warnings")
        warning_div.html(msg);
        setTimeout(function() {warning_div.html("");}, 3000);
    }


    // SIZING UTILS
    QUESTION_STATE.resizeInput = function() {
        $(this).css('width', `${10*Math.max(1, $(this).val().length)}px`); 
    }

    function textAreaAdjust() {
        this.style.height = "1px";
        this.style.height = (5+this.scrollHeight)+"px";
    }

    QUESTION_STATE.resizeInputs = () => {
        QUESTION_STATE.DROPZONE.find('input').each(QUESTION_STATE.resizeInput);
        QUESTION_STATE.DROPZONE.find('textarea').each(textAreaAdjust);    
    }

    function resizeBox() {
        $(this).css({
        width: (round_to_grid($(this).width()) + 1)*GRID_SIZE,
        height: (round_to_grid($(this).height()) + 1)*GRID_SIZE,
        });
    }

    QUESTION_STATE.resizeCanvas = () => {
        QUESTION_STATE.CANVAS.attr("width", QUESTION_STATE.DROPZONE.width());
        QUESTION_STATE.CANVAS.attr("height", QUESTION_STATE.DROPZONE.height());
    }

    QUESTION_STATE.getRandomInt = (max) => {
        return Math.floor(Math.random() * max);
    }

    QUESTION_STATE.parseId = (element) => {
        return parseInt(element.attr("id").split("_")[1]);
    }
    

    QUESTION_STATE.get_metadata = (item) => {
        // target may be an int (the id) or a dictionary of {"value":4, "fixed":true}
        if (item.constructor !== Object) {
            return {value:item, fixed:false};
        }
        return item;
    }

    QUESTION_STATE.makeLine = (start_object, metadata, lines_to_make) => {
        if (metadata.fixed) {
            start_object.addClass("fixed");
            start_object.removeClass("lineActive");
        }
        if (metadata.value !== null) {
            lines_to_make.push({"start_object":start_object, "end_id":metadata.value, "fixed":metadata.fixed});
        }
    }

    QUESTION_STATE.processSource = (source) => {
        metadata = {"fixed":source.hasClass("fixed"), "value":QUESTION_STATE.getLineEndID(source)};
        return metadata;
      }

    QUESTION_STATE.removeLines = (endpoint) => {
        for (let i=QUESTION_STATE.STORED_LINES.length-1;i>=0;i--) {
            const storedLine = QUESTION_STATE.STORED_LINES[i];
            if (storedLine.start.is(endpoint) || storedLine.end.is(endpoint)){
                // remove that line from the stored lines
                QUESTION_STATE.STORED_LINES.splice(i,1);
                if (storedLine.start.hasClass("set-entry")) {
                    storedLine.start.remove();
                }
            }
        }
    }

    function getObjectId(object) {
        while (object && !object.hasClass("box")) {
            object = object.parent();
        }
        if (object) {
            return object.attr("id");
        }
    }

    QUESTION_STATE.roundPosition = (pos) => {
        return {"left":Math.round(pos.left), "top":Math.round(pos.top)}
    }

    QUESTION_STATE.round_to_grid = (value) => {
        return Math.round(value/GRID_SIZE)
      }


    QUESTION_STATE.getParentBox = (object) => {
        while(!object.hasClass("box")) {
        object = object.parent();
        }
        return object;
    }

    QUESTION_STATE.boundingBox = (object) => {
        const position = object.position();
        position.label_x = round_to_grid(position.left + object.find(".box-label").width());
        if (object.hasClass("function") || object.hasClass("xance-box") || object.hasClass("class-box")) {
            position.label_x = round_to_grid(position.left + object.width())+1;
        }
        position.right = round_to_grid(position.left + object.width())+1;
        if (object.hasClass("sequence")){
            console.log("position", position.top, object.outerHeight())
        }
        
        position.bottom = round_to_grid(position.top + object.outerHeight())-1;
        position.left = round_to_grid(position.left);
        position.top = round_to_grid(position.top) - 1;

        return position
    }

    QUESTION_STATE.init_codemirror = (dom_element) => {
        var cs_codemirror = 
        CodeMirror.fromTextArea(dom_element, {
            mode: 'python',
            handleMouseEvents: true,
          });
        // CodeMirror.fromTextArea(dom_element, {
        //     lineNumbers: true, 
        //     indentUnit: 4, 
        //     mode: 'python', 
        //     foldGutter: true, 
        //     gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'], 
        //     extraKeys: { 
        //       Tab: (cm) => { 
        //         if (cm.getMode().name === 'null') { 
        //           cm.execCommand('insertTab'); 
        //         } else { 
        //           if (cm.somethingSelected()) { 
        //             cm.execCommand('indentMore'); 
        //           } else { 
        //             cm.execCommand('insertSoftTab'); 
        //           } 
        //         } 
        //       }, 
        //       'Shift-Tab': (cm) => cm.execCommand('indentLess'), 
        //     }, 
        //   }); 

          cs_codemirror.on('change', function(){
            cs_codemirror.save();
          });
          console.log("cm", cs_codemirror)
        return cs_codemirror;
    }




    $(document)
        .on('keyup', '.dropzone input[type="text"]', QUESTION_STATE.resizeInput)
        .on('keyup', '.dropzone textarea', textAreaAdjust)

    return QUESTION_STATE;

})(QUESTION_STATE || {})