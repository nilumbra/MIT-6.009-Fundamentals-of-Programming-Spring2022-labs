var QUESTION_STATE = (function (QUESTION_STATE) {
    // Fill QUESTION_STATE
    QUESTION_STATE.CONTAINER = $(`#${QUESTION_STATE.CSQ_NAME}-container`);
    QUESTION_STATE.DROPZONE = QUESTION_STATE.CONTAINER.find(`.dropzone`);
    QUESTION_STATE.CANVAS = QUESTION_STATE.DROPZONE.find("canvas");
    QUESTION_STATE.CTX = QUESTION_STATE.CANVAS[0].getContext("2d");

    QUESTION_STATE.WARNING_DIV = QUESTION_STATE.CONTAINER.find(`.warnings`)
    QUESTION_STATE.STORED_PATHS = [];
    QUESTION_STATE.STORED_LINES = [];
    QUESTION_STATE.DRAG_OBJECTS = [];

    QUESTION_STATE.SETUP_COMPLETE = false;

    return QUESTION_STATE;
})(QUESTION_STATE || {})