var QUESTION_STATE = (function (QUESTION_STATE) {
    
  SET_TEMPLATE = `<div class="box lineRecipient">
      <span class="box-label">set</span>
      <div id="set-content-template" class="set-add" data-items="{}"></div>
  </div>`

  SET_ENTRY_TEMPLATE = `<div class="dot set-entry hash-entry any-start line lineActive sourceNode source" data-value="{}"></div>`
  SET_WIDTH = 75;
  SET_HEIGHT = 100;

  QUESTION_STATE.createSet = (json_data=null, lines_to_make=null) => {
      element = $(SET_TEMPLATE);

      if (json_data){
        value = json_data["value"]
          for (key of value) {
              let entry = $(SET_ENTRY_TEMPLATE);
              let content = element.find(".set-add");
              randomSetPosition(content, entry)
              
              // console.log("key object", key_object, entry)
              // we'll store sublists of the start object for the line, and the id of the object that it will eventually point to
              metadata = QUESTION_STATE.get_metadata(key);
              QUESTION_STATE.makeLine(entry, metadata, lines_to_make);
              entry.data("value", metadata.value)
              // console.log("setting up a set with metadata", metadata, metadata.value, entry.data("value"))
              
              content.append(entry);
          } 
      }

      element.on("getJson", function() {
          const element = $(this);
          const value = []
          element.find('.set-entry').each(function () {
              value.push(QUESTION_STATE.processSource($(this)));
          });
          return value;
      })

      // element.find("set-add").css({
      //     width: SET_WIDTH,
      //     height: SET_HEIGHT
      // })

      return element;
  }

  function randomSetPosition(container, entry) {
      let finished = false;
      let x,y;
      let i = 0;
      
      
      while (!finished) {
        let [width, height] = [container.width(), container.height()];
        console.log("set width height", width, height);
        finished = true;
        x = QUESTION_STATE.round_to_grid(QUESTION_STATE.getRandomInt((width-20)))*GRID_SIZE+5;
        y = QUESTION_STATE.round_to_grid(QUESTION_STATE.getRandomInt((height-20)))*GRID_SIZE+5;
        container.find('.set-entry').each(function () {
          const otherEntry = $(this);
          const x2 = otherEntry.position().left;
          const y2 = otherEntry.position().top;
          if ((Math.abs(x-x2)) < 20 && (Math.abs(y-y2) < 20)){
            finished = false;
          }
        })
        i++;
        if (i > 20) {
          QUESTION_STATE.SETUP_COMPLETE = false
          container.width(container.width()+5);
          container.height(container.height()+5);
          i = 0;
        }
      }
      
      entry.css({top: y, left: x, position:'absolute'});
      
    }

  function handleSetAdd() {
      if ($(this).hasClass("fixed-length")) {
        QUESTION_STATE.notify("item has fixed length");
        return;
      }
      QUESTION_STATE.isDown = true;
      
      const entry = $(SET_ENTRY_TEMPLATE)
      randomSetPosition($(this), entry)
      
      $(this).append(entry);
      QUESTION_STATE.startObj = entry;
      QUESTION_STATE.lineColor = "blue";
      [QUESTION_STATE.startX, QUESTION_STATE.startY] = QUESTION_STATE.getDotXY(entry);
  }

  QUESTION_STATE.CONTAINER
      .on('mousedown', '.set-add', handleSetAdd)
  return QUESTION_STATE;
})(QUESTION_STATE || {})