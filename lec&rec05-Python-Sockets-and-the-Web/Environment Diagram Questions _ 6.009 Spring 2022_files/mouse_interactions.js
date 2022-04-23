((QUESTION_STATE) => {
    
  
  QUESTION_STATE.startX = 0;
  QUESTION_STATE.startY = 0;
  QUESTION_STATE.startObj = null;
  const MUTABLE_TYPES = ["dict", "set", "list"]
  // Get the modal
  const instr_modal = QUESTION_STATE.CONTAINER.find(".instruction-modal")
  const reset_modal = QUESTION_STATE.CONTAINER.find(".reset-modal")

  $(QUESTION_STATE.CONTAINER)
      .on('click', '.removeActive', function() {
        var tr = $(this).parent()
        box = QUESTION_STATE.getParentBox($(this));
        // clean up any line
        tr.find(".sourceNode").each((e, endpoint) => QUESTION_STATE.removeLines($(endpoint)));
        tr.remove();

        // we reset the size of a sequence upon removals
        if (box.hasClass("sequence")) {
          box.css("min-width", `${10+box.find("tr").length*20}px`)
          box.css("max-width", `${10+box.find("tr").length*20}px`)
        }
      })

      .on('click', ".instruction-btn", () => openModal(instr_modal))
      .on('click', `#${QUESTION_STATE.CSQ_NAME}_reset`, () => openModal(reset_modal))
      .on('click', ".edit-popup", annotationsModal)
      .on('click', ".close-modal", () => closeModal(instr_modal))
      .on('click', `#${QUESTION_STATE.CSQ_NAME}_reset_close`, () => closeModal(reset_modal))


      .on('mousedown', '.CodeMirror', handleCodeMirrorMouse)
      .on('mousedown', '.lineActive', handleMouseDown)
      .on('mouseup', '.lineRecipient', handleMouseUp)
      .on('mouseup', '.frameLineRecipient', handleMouseUpFrame)
      .on('mouseup', '.classLineRecipient', handleMouseUpClass)
      
      .on('mousemove', '.dropzone', handleMouseMove)
      
      .on('mouseover', '.box:not(.template)', handleMouseOver)
      .on('mouseout', '.box:not(.template)', handleMouseOut)
      .on('keydown', 'textarea',  function(e) {
        if (e.key == 'Tab') {
          e.preventDefault();
          var start = this.selectionStart;
          var end = this.selectionEnd;
      
          // set textarea value to: text before caret + tab + text after caret
          this.value = this.value.substring(0, start) +
            "\t" + this.value.substring(end);
      
          // put caret at right position again
          this.selectionStart =
            this.selectionEnd = start + 1;
        }
      });
      
  $(document).on('mouseup', handleMouseUpOutside);

  function mousePosition(e) {
    // handle scroll offsets
    canvas_off = QUESTION_STATE.CANVAS.offset()
    return [parseInt(e.clientX - canvas_off.left + document.documentElement.scrollLeft ), parseInt(e.clientY - canvas_off.top + document.documentElement.scrollTop)]
  }

  function handleMouseDown(e) {
    e.stopPropagation();
    [mouseX, mouseY] = mousePosition(e); 
    QUESTION_STATE.startObj = $(this);
    // if the start object if fixed, then do not allow changes
    if (QUESTION_STATE.startObj.hasClass('fixed')) {
      QUESTION_STATE.notify("This reference should not be changed.")
      return;
    }

    QUESTION_STATE.isDown = true;

    // remove previous line involving this startObj
    if (QUESTION_STATE.startObj.hasClass('sourceNode')){
      QUESTION_STATE.lineColor = "blue";
    } else if (QUESTION_STATE.startObj.hasClass("classSource")){
      QUESTION_STATE.lineColor = "green";
    } else if (QUESTION_STATE.startObj.hasClass("parent-frame-ptr")){
      QUESTION_STATE.lineColor = "purple";
    } else {
      QUESTION_STATE.lineColor = "red";
    }

    // remove any existing line starting from this source
    if (QUESTION_STATE.startObj.hasClass('source')){
      for (var i = QUESTION_STATE.STORED_LINES.length-1; i >=0; i--) {
        storedLine = QUESTION_STATE.STORED_LINES[i];
        if (storedLine.start.is(QUESTION_STATE.startObj)){
          QUESTION_STATE.STORED_LINES.splice(i, 1); // splice away 1 item starting at index i
          QUESTION_STATE.STORED_PATHS.splice(i, 1);
          QUESTION_STATE.redrawStoredLines();
        }
      }
    }


    

    // for drawing the line to the user mouse, we record the start x,y
    let dot = QUESTION_STATE.getDotXY($(this));
    [QUESTION_STATE.startX, QUESTION_STATE.startY] = dot;
  }



  function handleMouseMove(e) {
    if (!QUESTION_STATE.isDown) {
      return;
    }
    QUESTION_STATE.redrawStoredLines();
    
    // draw the current line
    [mouseX, mouseY] = mousePosition(e); 
    CTX = QUESTION_STATE.CTX;
    CTX.beginPath();
    CTX.strokeStyle = QUESTION_STATE.lineColor;
    CTX.moveTo(QUESTION_STATE.startX, QUESTION_STATE.startY);
    CTX.lineTo(mouseX, mouseY);
    CTX.stroke();

  }


  function handleMouseUpFrame(e) {
    if (!QUESTION_STATE.isDown) {
      return;
    }
    $(this).removeClass("highlight");
    QUESTION_STATE.isDown = false;

    if (!QUESTION_STATE.startObj.hasClass("frameSource") && QUESTION_STATE.ENFORCE_CORRECTNESS){
      QUESTION_STATE.notify("Only frame pointers should point to a frame.")
      if (QUESTION_STATE.startObj.hasClass("set-entry")){
        QUESTION_STATE.removeLines.call(QUESTION_STATE.startObj);
        QUESTION_STATE.startObj.remove();
      }
      QUESTION_STATE.redrawStoredLines();
      return;
    }

    QUESTION_STATE.STORED_LINES.push({
      start: QUESTION_STATE.startObj,
      end: $(this)
    });
    QUESTION_STATE.recalculateLines();
  }

  function handleMouseUpClass(e) {
    if (!QUESTION_STATE.isDown) {
      return;
    }
    $(this).removeClass("highlight");
    QUESTION_STATE.isDown = false;

    if (QUESTION_STATE.startObj.hasClass("frameSource")  && QUESTION_STATE.ENFORCE_CORRECTNESS) {
      QUESTION_STATE.notify("Frame pointers must point to a frame.")
      QUESTION_STATE.redrawStoredLines();
      if (startObj.hasClass("set-entry")){
        QUESTION_STATE.removeLines.call(QUESTION_STATE.startObj);
        QUESTION_STATE.startObj.remove();
      }
      return;
    } 

    if (QUESTION_STATE.startObj.hasClass("classSource")) {
      QUESTION_STATE.STORED_LINES.push({
        start: QUESTION_STATE.startObj,
        end: $(this)
      });
      QUESTION_STATE.recalculateLines();

    }
  }

  function handleMouseUp(e) {
    if (!QUESTION_STATE.isDown) {
      return;
    }
    $(this).removeClass("highlight");
    if (!QUESTION_STATE.startObj.hasClass("sourceNode")  && QUESTION_STATE.ENFORCE_CORRECTNESS){
      if (QUESTION_STATE.startObj.hasClass("frameSource")) {
        QUESTION_STATE.notify("Frame pointers must point to a frame.")
      } else {
        if ($(this).hasClass("classLineRecipient")){
          return;
        }
        QUESTION_STATE.notify("Class pointers must point to a class.")
      }
      QUESTION_STATE.isDown = false;
      QUESTION_STATE.redrawStoredLines();
      return;
    }

    QUESTION_STATE.isDown = false;
    // hash check to see if this is an acceptable assignment
    if(QUESTION_STATE.startObj.hasClass("hash-entry") && !hashCheck(QUESTION_STATE.startObj, $(this))) {
      return;
    }

    QUESTION_STATE.STORED_LINES.push({
      start: QUESTION_STATE.startObj,
      end: $(this)
    });
    QUESTION_STATE.recalculateLines();
  }

  function handleMouseUpOutside(e) {
    // since there isn't a lineRecipient object below, delete the current active line
    if (!QUESTION_STATE.isDown) {
      return;
    }
    QUESTION_STATE.isDown = false;

    // remove start object if it is a set
    if (QUESTION_STATE.startObj.hasClass("set-entry")){
      QUESTION_STATE.removeLines.call(QUESTION_STATE.startObj);
      QUESTION_STATE.startObj.remove();
    }
    QUESTION_STATE.redrawStoredLines();
  }

  function handleMouseOver(e) {
    if (QUESTION_STATE.isDown) {
      $(this).addClass("highlight");
    }
  }

  function handleMouseOut(e) {
    $(this).removeClass("highlight");
  }

  function hashCheck(startObj, target) {
    if (!QUESTION_STATE.ENFORCE_CORRECTNESS) {
      return true;
    }
    if (MUTABLE_TYPES.includes(target.data("type"))) {
      QUESTION_STATE.notify("cannot hash mutable types");
      startObj.remove();
      QUESTION_STATE.redrawStoredLines();
      return false;
    }

    conflict = false;
    // don't add item if it has already been added to the set
    // console.log("hash check, target id", target, QUESTION_STATE.parseId(target))
    QUESTION_STATE.getParentBox(startObj).find(".hash-entry").each(function(index, entry) {
      // console.log("entry id", entry, parseInt($(entry).data("value")))
      if (conflict || parseInt($(entry).data("value")) === QUESTION_STATE.parseId(target)) {
        conflict = true;
        return false;
      }
    })
    if (conflict) {
      QUESTION_STATE.notify("cannot have duplicate hashes");
      startObj.remove();
      QUESTION_STATE.redrawStoredLines();
      return false;
    }
    startObj.data("value", QUESTION_STATE.parseId(target));
    return true;
  }


  // prevent dragging when click dragging on a code mirror textarea
  function handleCodeMirrorMouse(e) {
    console.log("this", this, this.CodeMirror)
    this.CodeMirror.refresh();
  }
  

  // When the user clicks the button, open the modal 
  function openModal(modal) {
    modal.css("display", "block");
  }

  function closeModal(modal) {
    modal.css("display", "none");
  }

  function annotationsModal() {
    object_box = $(this).parent();
    object_box.find(".annotation").toggleClass("show");
  }


})(QUESTION_STATE || {})