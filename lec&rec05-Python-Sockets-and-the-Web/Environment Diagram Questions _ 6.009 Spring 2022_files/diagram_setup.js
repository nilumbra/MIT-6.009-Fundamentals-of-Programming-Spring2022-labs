var QUESTION_STATE = (function (QUESTION_STATE) {
  QUESTION_STATE.POPUP_TEMPLATE = `<span class="edit-popup">📝</span>`
  QUESTION_STATE.ANNOTATION_TEMPLATE = `<textarea class="annotation" placeholder="enter notes here"></textarea>`

  QUESTION_STATE.TYPE_CREATORS = {"frame":QUESTION_STATE.createFrame, "function":QUESTION_STATE.createFunction, "bool":QUESTION_STATE.createBool, "None":QUESTION_STATE.createNone,
    "int":QUESTION_STATE.createInt, "float":QUESTION_STATE.createFloat, "str":QUESTION_STATE.createStr, "dict":QUESTION_STATE.createDict,
    "set":QUESTION_STATE.createSet, "list":QUESTION_STATE.createList, "tuple":QUESTION_STATE.createTuple, "class":QUESTION_STATE.createClass,
    "instance":QUESTION_STATE.createInstance, "bound_method":QUESTION_STATE.createBoundMethod}

  QUESTION_STATE.JSON_HISTORY = [];
  QUESTION_STATE.HISTORY_INDEX = -1;
  
  const TYPE_TEMPLATE = `<div class="box template draggable ui-widget-content"></div>`
  
  let ids_to_dom = {};
  const roundPosition = QUESTION_STATE.roundPosition;
  const recalculateLines = QUESTION_STATE.recalculateLines;

  QUESTION_STATE.RESIZE_OBSERVER = setupResizeObserver(QUESTION_STATE);

  // mouse event triggers
  // on every keyup we store the current state
  QUESTION_STATE.DROPZONE
    .keyup( () => setTimeout(QUESTION_STATE.toJson, 500 ))
    .droppable({
      drop: dropzoneDrop(QUESTION_STATE)
    })


function setupResizeObserver(QUESTION_STATE) {
  return new ResizeObserver(entries => {
    for (let entry of entries) {
      window.requestAnimationFrame(() => {
        if (!Array.isArray(entries) || !entries.length) {
          return;
        }
        
        element = $(entry.target);
        if (element.hasClass("child-box")) {
          // for frames, instances, classes, and functions we adjust placement of the parent pointer box
          // so that the dot stays on the grid
          let dot_container = element.find(".top-dot-container");
          dot_container.css("right", Math.round(parseInt(element.css("width")) % GRID_SIZE));
        }
  
        // to avoid recalculating during setup
        if (QUESTION_STATE.SETUP_COMPLETE) {
          console.log("resize observer of", element, "causing recalc lines")
          recalculateLines(QUESTION_STATE);
        }
      });
    }
  });
}


  

  function setupOptionTypes() {
    const container = QUESTION_STATE.CONTAINER.find(".type-container");
    for (type of QUESTION_STATE.TYPE_OPTIONS) {
      const element = $(TYPE_TEMPLATE);
      element.attr("data-type",type);
      element.html(type)
      element.addClass(type);
      element.draggable({
        helper: "clone",
        cursor: 'move',
        zIndex: 10,
      });

      element.click(function() {
        console.log("clicked")
        offset = {"top":60,"left":200}
        elt = QUESTION_STATE.createElement($(this).data("type"), offset);
        // element = QUESTION_STATE.createElement(ui.helper.data("type"), offset);
        QUESTION_STATE.DROPZONE.append(elt);
        QUESTION_STATE.RESIZE_OBSERVER.observe(elt[0]);
        QUESTION_STATE.resizeInputs(elt);

      })
      container.append(element);
    }
  }


QUESTION_STATE.fromJson = (parsed) => {
  // clear the dropzone
  QUESTION_STATE.SETUP_COMPLETE = false;
  DROPZONE = QUESTION_STATE.DROPZONE;
  DROPZONE.children(".box").remove();
  STORED_LINES = QUESTION_STATE.STORED_LINES;
  STORED_LINES.length = 0;

  
  const lines_to_make = []

  // TODO naive placement strategy, keep placing objects in the next available spot
  let bottom_bound = 60;
  let right_bound = 40;
  let curr_left_offset = 40;


  for (subset of ["frames", "objects"]) {
    for (objectId in parsed[subset]){
      object_json = parsed[subset][objectId];
      let offset;
      if ("offset" in object_json) {
        offset = object_json['offset'];
      } else {
        offset = {"top":bottom_bound,"left":curr_left_offset}
      }

      const element = QUESTION_STATE.createElement(object_json['type'], offset, lines_to_make, object_json);
      if (object_json["fixed"]) {
        element.addClass("fixed-box");
      }
      if (object_json["fixed-length"]) {
        element.addClass("fixed-length");
      }
      if ("annotation" in object_json) {
        element.find(".annotation").html(object_json["annotation"]);
      }
      DROPZONE.append(element);
      QUESTION_STATE.RESIZE_OBSERVER.observe(element[0]);
      
      // for frames, instances, classes, and functions we adjust placement of the parent pointer box
      // so that the dot stays on the grid
      if (element.hasClass("child-box")) {
        let dot_container = element.find(".top-dot-container");
        dot_container.css("right", Math.round(parseInt(element.css("width")) % GRID_SIZE));
      }
      
      bottom_bound = offset.top + element.height()+60
      
      if (bottom_bound > DROPZONE.height()+60) {
        element.css("top", 60);
        element.css("left", right_bound+10)
        curr_left_offset = right_bound;
        bottom_bound = 40 + element.height()
      }
      right_bound = Math.max(right_bound, offset.left + element.width())
    }

    bottom_bound = 60;
    curr_left_offset = right_bound;
  }

  // After elements exist, create a list of the connected points
  for (line of lines_to_make) {
    STORED_LINES.push({
      start: line.start_object,
      end: ids_to_dom[line.end_id],
    });
  }


  
  
  QUESTION_STATE.resizeInputs(DROPZONE);
  QUESTION_STATE.recalculateLines();
  QUESTION_STATE.DROPZONE.find(".CodeMirror").each(function(){
    console.log("this2",this, $(this).find("textarea").val()); this.CodeMirror.refresh()
  });

}





QUESTION_STATE.DROPZONE.find(".trash").droppable({
  tolerance: "touch",
  drop: function(event, ui) {
    var trash = ui.draggable;
    if (trash.hasClass("fixed-box")) {
      // console.log("Cannot trash this object.", QUESTION_STATE)
      QUESTION_STATE.notify("Cannot trash this object.")
      // put object back inside the dropzone
      position = QUESTION_STATE.getPosition(trash);
      trash.css({
        left: Math.round(Math.min(DROPZONE.width()-trash.width()-40, Math.max(position.left, 20))/GRID_SIZE)*GRID_SIZE,
        top: Math.round(Math.min(DROPZONE.height()-trash.height()-20, Math.max(position.top, 40))/GRID_SIZE)*GRID_SIZE,
      });
      $(this).removeClass("droppable-over");
      return;
    }
    trash.remove();
    QUESTION_STATE.removeLines(trash);
    trash.find(".source").each(function() {
      QUESTION_STATE.removeLines($(this))
    });
    $(this).removeClass("droppable-over");
    QUESTION_STATE.toJson();
  },
  over: function(event, ui) {
    if (!ui.draggable.hasClass("fixed-box")) {
      $(this).addClass("droppable-over");
    }
  },
  out: function(event, ui) {
    $(this).removeClass("droppable-over");
  }
})

function dropzoneDrop(QUESTION_STATE) {
  return function(event, ui) {
    if (ui.draggable.hasClass('template')) {
      var dropzoneOffset = QUESTION_STATE.DROPZONE.position();
      var offset = {
        left: ui.position.left - dropzoneOffset.left,
        top: ui.position.top - dropzoneOffset.top
      };
      element = QUESTION_STATE.createElement(ui.helper.data("type"), offset);
      QUESTION_STATE.DROPZONE.append(element);
      QUESTION_STATE.RESIZE_OBSERVER.observe(element[0]);
      QUESTION_STATE.resizeInputs(element);
      QUESTION_STATE.toJson();
      
    }
  }
}



  
QUESTION_STATE.createElement = (type, canElOff, lines_to_make = null, json_data=null) => {
  // console.log("here json data", json_data)
  let element;
  if (type in QUESTION_STATE.TYPE_CREATORS) {
    element = QUESTION_STATE.TYPE_CREATORS[type](json_data, lines_to_make);
  } else {
    console.log("INVALID TYPE", type);
    return;
  }

  element.data("type", type);
  if (json_data === null) {
    id = QUESTION_STATE.uniq_id();
  } else {
    id = json_data["id"]
    QUESTION_STATE.unique_id_count = Math.max(QUESTION_STATE.unique_id_count, parseInt(id))
  }
  
  element.attr("id", QUESTION_STATE.CSQ_NAME + "_" + id);
  ids_to_dom[id] = element;

  // set position to be entirely inside of the DROPZONE
  element.css({
    left: Math.round(Math.min(QUESTION_STATE.DROPZONE.width()-element.width(), Math.max(canElOff.left, 20))/GRID_SIZE)*GRID_SIZE,
    top: Math.round(Math.min(QUESTION_STATE.DROPZONE.height()-element.height(), Math.max(canElOff.top, 40))/GRID_SIZE)*GRID_SIZE,
    position: 'absolute',
    Zindex: 10
  });

  element.append($(QUESTION_STATE.POPUP_TEMPLATE))

  element.append($(QUESTION_STATE.ANNOTATION_TEMPLATE))
  element.hover(
    function () {
      $(this).find(".edit-popup").addClass("show");
    },
    function () {
      $(this).find(".edit-popup").removeClass("show");
    }
  )
  
  element.mouseup( () => setTimeout(QUESTION_STATE.toJson, 500 ))
      
  // whenever this element is moved, we redraw any lines it involves, and contain the element in the dropzone
  element.draggable({
    cursor: 'move',
    containment: QUESTION_STATE.DROPZONE.find('.dropzone-background'),
    drag: function(event, ui) {
      if (QUESTION_STATE.isDown)
        return false;
      
      QUESTION_STATE.redrawStoredLines();
    },
    start: function(event, ui) {
      // we can record all the sources and the box itself to check whether an object is being drug when redrawing paths
      QUESTION_STATE.DRAG_OBJECTS = [];
      $(this).find(".source").each(function(){
        QUESTION_STATE.DRAG_OBJECTS.push($(this))
      });
      QUESTION_STATE.DRAG_OBJECTS.push($(this));
      // console.log("here Drage Objects", QUESTION_STATE.DRAG_OBJECTS)
    },
    stop: function(event, ui) {
      QUESTION_STATE.DRAG_OBJECTS = [];
      // snap the position to the grid
      const position = $(this).position()
      $(this).css({
        left: Math.max(Math.round(position.left/GRID_SIZE)*GRID_SIZE, GRID_SIZE*2),
        top: Math.max(Math.round(position.top/GRID_SIZE)*GRID_SIZE, GRID_SIZE*3),
      })
      if (!QUESTION_STATE.isDown) {
        console.log("here drop", QUESTION_STATE);
        recalculateLines();
      }
      
    }
    // drag: function(event, ui) {
    //   if (QUESTION_STATE.isDown)
    //     return false;
    //   },
    // stop: function(event, ui) {
    //   // snap the position to the grid
    //   const position = $(this).position()
    //   $(this).css({
    //     left: Math.max(Math.round(position.left/GRID_SIZE)*GRID_SIZE, GRID_SIZE*2),
    //     top: Math.max(Math.round(position.top/GRID_SIZE)*GRID_SIZE, GRID_SIZE*3),
    //   })
    //   if (!QUESTION_STATE.isDown) {
    //     console.log("here drop", QUESTION_STATE);
    //     QUESTION_STATE.recalculateLines();
    //   }
      
    // }
  });

  return element
}


// console.log("making tojson")
QUESTION_STATE.toJson = () => {

  const memoryObjects = {};
  const frames = {};
  QUESTION_STATE.DROPZONE.children('.box').each(function () {

    const element = $(this);
    // I don't understand why this is necessary to re-select the element before calling the getJson handler
    
    const value = element.triggerHandler("getJson");
    // console.log("get json", element, value);
    // const value = TYPE_TO_JSON[QUESTION_STATE.DROPZONE.find(`#${element.attr("id")}`).data("type")](element);
    const id = QUESTION_STATE.parseId(element);
    const json = {"id":id, "value":value, "offset":roundPosition(element.position()), "type":element.data("type"),
                  "annotation":element.find(".annotation").html(), "fixed":element.hasClass("fixed-box"), 
                  "fixed-length":element.hasClass("fixed-length")}
    if (element.hasClass("starter-box")) {
      json["starter"] = true;
    }

    if (element.hasClass('frame')){
      frames[id] = json;
    } else {
      memoryObjects[id] = json;
    }

  });
  const submission = {"frames": frames, "objects": memoryObjects}
  // store the submitted_json into the hidden input
  // console.log("submission stored is", submission, QUESTION_STATE.CSQ_NAME, $(`#${QUESTION_STATE.CSQ_NAME}`))
  $(`#${QUESTION_STATE.CSQ_NAME}`).val(JSON.stringify(submission));
  // truncate any json history that had been undone
  console.log("history pre", QUESTION_STATE.JSON_HISTORY)
  QUESTION_STATE.JSON_HISTORY = QUESTION_STATE.JSON_HISTORY.slice(0, QUESTION_STATE.HISTORY_INDEX+1)
  QUESTION_STATE.JSON_HISTORY.push(submission);
  console.log("history", QUESTION_STATE.JSON_HISTORY)
  QUESTION_STATE.HISTORY_INDEX = QUESTION_STATE.JSON_HISTORY.length - 1;
  if (QUESTION_STATE.HISTORY_INDEX > 0) {
    $(`#${QUESTION_STATE.CSQ_NAME}_undo`).removeClass("inactive")
  }
  
}

  // function add_reset_button() {
  //   btn_container = $(`#${QUESTION_STATE.CSQ_NAME}_buttons`);
  //   reset_btn = $();
  //   reset_btn.on("click", () => QUESTION_STATE.fromJson(QUESTION_STATE.STARTER_JSON));
  //   btn_container.append(reset_btn);
  // }

  $(`#${QUESTION_STATE.CSQ_NAME}_save`).on("click", () => QUESTION_STATE.toJson());


  $(`#${QUESTION_STATE.CSQ_NAME}_reset_confirm`).on("click", function(){
    QUESTION_STATE.CONTAINER.find(".reset-modal").css("display", "none");
    QUESTION_STATE.fromJson(QUESTION_STATE.STARTER_JSON); 
    QUESTION_STATE.toJson()});

  $(`#${QUESTION_STATE.CSQ_NAME}_undo`).on("mouseup", (e) => {
    // stop propogation so that an undo doesn't add to history
    e.stopPropagation();
    e.preventDefault();  
    e.returnValue = false;
    e.cancelBubble = true;
    return false;
  })

  $(`#${QUESTION_STATE.CSQ_NAME}_redo`).on("mouseup", (e) => {
    // stop propogation so that an redo doesn't add to history
    e.stopPropagation();
    e.preventDefault();  
    e.returnValue = false;
    e.cancelBubble = true;
    return false;
  })

  $(`#${QUESTION_STATE.CSQ_NAME}_undo`).on("click", (e) => {
    
    if (QUESTION_STATE.HISTORY_INDEX > 0) {
      QUESTION_STATE.HISTORY_INDEX--;
      console.log("json from index", QUESTION_STATE.HISTORY_INDEX)
      QUESTION_STATE.fromJson(QUESTION_STATE.JSON_HISTORY[QUESTION_STATE.HISTORY_INDEX]);
      if (QUESTION_STATE.HISTORY_INDEX < QUESTION_STATE.JSON_HISTORY.length-1) {
        $(`#${QUESTION_STATE.CSQ_NAME}_redo`).removeClass("inactive")
      }
      if (QUESTION_STATE.HISTORY_INDEX === 0) {
        $(`#${QUESTION_STATE.CSQ_NAME}_undo`).addClass("inactive")
      }
    }
  });


  $(`#${QUESTION_STATE.CSQ_NAME}_redo`).on("click", (e) => {
    
    if (QUESTION_STATE.HISTORY_INDEX < QUESTION_STATE.JSON_HISTORY.length-1) {
      QUESTION_STATE.HISTORY_INDEX++;
      console.log("redo - json from index", QUESTION_STATE.HISTORY_INDEX)
      QUESTION_STATE.fromJson(QUESTION_STATE.JSON_HISTORY[QUESTION_STATE.HISTORY_INDEX]);
      $(`#${QUESTION_STATE.CSQ_NAME}_undo`).removeClass("inactive")
      if (QUESTION_STATE.HISTORY_INDEX === QUESTION_STATE.JSON_HISTORY.length-1) {
        $(`#${QUESTION_STATE.CSQ_NAME}_redo`).addClass("inactive")
      }
    }
  });

  // Set up initialization
  QUESTION_STATE.CTX.strokeStyle = "orange";
  QUESTION_STATE.CTX.lineWidth = 2;
  QUESTION_STATE.resizeCanvas();
  setupOptionTypes();
  if (QUESTION_STATE.LAST_SUBMISSION !== "") {
    QUESTION_STATE.fromJson(QUESTION_STATE.LAST_SUBMISSION); 
  } else if (QUESTION_STATE.STARTER_JSON !== "") {
    QUESTION_STATE.fromJson(QUESTION_STATE.STARTER_JSON); 
  }
  setTimeout(QUESTION_STATE.toJson, 500);
  // setTimeout(add_reset_button, 200);


  return QUESTION_STATE;

})(QUESTION_STATE || {})