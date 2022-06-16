var QUESTION_STATE = (function (QUESTION_STATE) {
  QUESTION_STATE.POPUP_TEMPLATE = `<span class="edit-popup">📝</span>`
  QUESTION_STATE.ANNOTATION_TEMPLATE = `<textarea class="annotation" placeholder="enter notes here"></textarea>`

  QUESTION_STATE.TYPE_CREATORS = {"frame":QUESTION_STATE.createFrame, "function":QUESTION_STATE.createFunction, "bool":QUESTION_STATE.createBool, "NoneType":QUESTION_STATE.createNone,
    "int":QUESTION_STATE.createInt, "float":QUESTION_STATE.createFloat, "str":QUESTION_STATE.createStr, "dict":QUESTION_STATE.createDict,
    "set":QUESTION_STATE.createSet, "list":QUESTION_STATE.createList, "tuple":QUESTION_STATE.createTuple, "class":QUESTION_STATE.createClass,
    "instance":QUESTION_STATE.createInstance, "bound_method":QUESTION_STATE.createBoundMethod, "unsupported":QUESTION_STATE.createUnsupported}

  let ids_to_dom = {};
  const recalculateLines = QUESTION_STATE.recalculateLines;

  QUESTION_STATE.RESIZE_OBSERVER = setupResizeObserver(QUESTION_STATE);



  // Set up initialization
  QUESTION_STATE.CTX.strokeStyle = "orange";
  QUESTION_STATE.CTX.lineWidth = 2;
  QUESTION_STATE.resizeCanvas();
  if (QUESTION_STATE.LAST_SUBMISSION !== "") {
    QUESTION_STATE.fromJson(QUESTION_STATE.LAST_SUBMISSION); 
  } else if (QUESTION_STATE.STARTER_JSON !== "") {
    QUESTION_STATE.fromJson(QUESTION_STATE.STARTER_JSON); 
  }






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
          console.log("resize observer causing recalc lines")
          recalculateLines(QUESTION_STATE);
        }
      });
    }
  });
}





QUESTION_STATE.fromJson = (parsed) => {
  // clear the dropzone
  console.log("from json parsed", parsed, QUESTION_STATE.CSQ_NAME)
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
      
      object_json["fixed_length"] = true;
      const element = QUESTION_STATE.createElement(object_json['type'], offset, lines_to_make, object_json);
    //   console.log("Creating elt with offset", element, offset)
      element.addClass("fixed-box");
      element.addClass("fixed-length");

      if ("annotation" in object_json) {
        element.find(".annotation").html(object_json["annotation"]);
      }
      DROPZONE.append(element);
      QUESTION_STATE.RESIZE_OBSERVER.observe(element[0]);
      
      bottom_bound = offset.top + element.height()+60
      
      if (bottom_bound > DROPZONE.height()+60) {
        console.log("making next col with left of", right_bound)
        element.css("top", 60);
        element.css("left", right_bound)
        curr_left_offset = right_bound;
        offset.left = right_bound;
        bottom_bound = element.height()+120
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
  
//   setTimeout(() => {QUESTION_STATE.SETUP_COMPLETE = true;}, 500);
  QUESTION_STATE.resizeInputs(DROPZONE);
  QUESTION_STATE.recalculateLines(QUESTION_STATE);

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



return QUESTION_STATE;

})(QUESTION_STATE || {})