var QUESTION_STATE = (function (QUESTION_STATE) {
    
  
  QUESTION_STATE.isDown = false;
  QUESTION_STATE.unique_id_count = 0;


  QUESTION_STATE.uniq_id = () => {
    QUESTION_STATE.unique_id_count = QUESTION_STATE.unique_id_count+1;
    return String(QUESTION_STATE.unique_id_count);
  }

  QUESTION_STATE.getPosition = (object) => {
    offset = object.offset()
    canvas_off = QUESTION_STATE.CANVAS.offset()
    return {left:offset.left  - canvas_off.left, top:offset.top - canvas_off.top}
  }

  QUESTION_STATE.getDotXY = (object) => {
    position = QUESTION_STATE.getPosition(object)
    return [position.left + object.width()/2, position.top + object.height()/2]
  }



  QUESTION_STATE.getLineEndID = (start_point) => {
    // console.log("called getLineEndID of", start_point, QUESTION_STATE.STORED_LINES, QUESTION_STATE.STORED_LINES.length)
    for (const stored_line of QUESTION_STATE.STORED_LINES) {
      // console.log("line comp", stored_line.start, start_point, stored_line.start.is(start_point))
      if (stored_line.start.is(start_point)){
        return QUESTION_STATE.parseId(stored_line.end);
      }
    }
    return null;
  }
  
  return QUESTION_STATE;
})(QUESTION_STATE || {})