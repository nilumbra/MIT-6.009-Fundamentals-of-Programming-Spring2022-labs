((QUESTION_STATE) => {
    
    GRID_SIZE = QUESTION_STATE.GRID_SIZE;
    HEADLEN = 8;
    BEND_PENALTY = 15;
    BOX_CROSS_PENALTY = 80;
    LINE_CROSS_PENALTY = 10;
    LINE_PARALLEL_PENALTY = 1000; // cost of two parallel lines occupying the same space. shouldn't be allowed

    const UP = "up";
    const DOWN = "down";
    const LEFT = "left";
    const RIGHT = "right";
    const OPPOSING_DIRECTION = {"up":DOWN, "down":UP, "left":RIGHT, "right":LEFT};

    let LINE_COVERAGE = {};
    let COVERAGE_MAP = {};
    boundingBox = QUESTION_STATE.boundingBox;
    getParentBox = QUESTION_STATE.getParentBox;
    round_to_grid = QUESTION_STATE.round_to_grid;

    

    function default_heuristic(node) {
        return 0;
    }

    function retrace_path(node, parent) {
        out = []
        while (node !== null) {
            out.push(node)
            node = parent[node]
        }
        out.reverse();
        return out;
    }

    function a_star(start, goal_func, neighbor_func, heuristic = default_heuristic, extra_starts=[]) {
        // start should be of the form [x, y, DIRECTION]
        distances = QUESTION_STATE.MinHeap();
        final_distances = {};

        distances.insert(start, 0, 0)
        keys_to_nodes = {};
        keys_to_nodes[start] = start;
        parent = {};
        parent[start] = null;
        
        for (source of extra_starts) {
            distances.insert(source, 0, 0);
            parent[source] = null;
            keys_to_nodes[source] = source;
        }

        visited = new Set();
        expanded = new Set();
        agenda = new Set();
        let neighb;

        while (Object.keys(distances).length > 0) {
            min_node = distances.extract_min();
            min_key = min_node.val;
            distance = min_node.distance;
            final_distances[min_key] = distance;
            delete distances[min_key];
            expanded.add(String(min_key));
            node = keys_to_nodes[min_key];
            

            if (goal_func(node, parent)) {
                return retrace_path(node, parent);
            }
            for (neighb_cost of neighbor_func(node, parent)) {
                [neighb, edge_cost] = neighb_cost;
                if (expanded.has(String(neighb))) {
                    continue;
                }
                
                if (!(distances.has(neighb))) {
                    distances.insert(neighb, distance + edge_cost + heuristic(neighb), distance + edge_cost)
                    keys_to_nodes[neighb] = neighb;
                    parent[neighb] = node;
                } else {
                    let cost = distance + edge_cost + heuristic(neighb)
                    if (cost < distances.get(neighb).priority) {
                    
                        distances.decrease_key(neighb, cost, distance + edge_cost);
                        parent[neighb] = node;
                    }
                }
            }
        }
    }


    function add_offset(point, offset) {
        let dx, dy;
        [dx, dy] = offset;
        return [point[0] + dx, point[1]+dy];
    }

    WIDTH = 200;
    HEIGHT = 200;
    function in_bounds(point) {
        return (point[0] >= 0 && point[0] < WIDTH && point[1] >=0 && point[1] < HEIGHT)
    }


    function add_box_coverage(element){
        box = boundingBox(element)
        for (let x = box.left; x <= box.right; x++) {
            for (let y = box.top; y <= box.bottom; y++) {
                COVERAGE_MAP[[x,y]] = 1;
            }
        }
        if (element.hasClass("frame")) {
            for (let x = box.left-2; x < box.left; x++) {
                for (let y = box.top+1; y <= box.top+3; y++) {
                    COVERAGE_MAP[[x,y]] = 1;
                }
            }
        }
    }

    function remove_box_coverage(element){
        box = boundingBox(element)
        for (let x = box.left; x <= box.right; x++) {
            for (let y = box.top; y <= box.bottom; y++) {
                delete COVERAGE_MAP[[x,y]];
            }
        }
        if (element.hasClass("frame")) {
            for (let x = box.left-2; x < box.left; x++) {
                for (let y = box.top+1; y <= box.top+3; y++) {
                    delete COVERAGE_MAP[[x,y]];
                }
            }
        }
    }

    function offset_to_direction(offset) {
        if (offset[0] === 0) {
            return "vert"
        }
        return "horiz"
    }



    function get_line_cost(point, direction) {
        // const direction = offset_to_direction(offset);
        if (point in LINE_COVERAGE) {
            // determine if perp or parallel to line
            if (LINE_COVERAGE[point].includes(direction)) {
                return LINE_PARALLEL_PENALTY;
            } else {
                return LINE_CROSS_PENALTY;
            }
        }
        return 0;
    }


    function get_offset(from, to) {
        return [to[0]-from[0], to[1]-from[1]];
    }

    function grid_neighbors(node) {
        let [x,y,direction] = node
        const output = [] // list of [neighb, distance]
        for ([dx, dy, new_direct] of [[0,1,DOWN], [0,-1,UP], [1, 0, RIGHT], [-1, 0, LEFT]]) {
            neighb = [x+dx, y+dy];
            if (OPPOSING_DIRECTION[direction] !== new_direct && in_bounds(neighb)){
                let cost = 1 + get_line_cost(neighb, new_direct);
                if (neighb in COVERAGE_MAP) {
                    cost = cost + BOX_CROSS_PENALTY;
                }
                if (direction !== null && direction !== new_direct) {
                    cost = cost + BEND_PENALTY
                }
                neighb.push(new_direct);
                output.push([neighb, cost]);
            }
        }
        return output;
    }


    function box_goal_maker(bounding_box) {
        function goal_test(point) {
            let [x,y,direction] = point;
            
            if (y <= bounding_box.bottom+1) {
                if (x === bounding_box.left-1 && direction === RIGHT && y >= bounding_box.top ) {
                    return true;
                } else if (x === bounding_box.right+1 && direction === LEFT && y >= bounding_box.top+1 ) {
                    return true;
                }
            }
            if (x >= bounding_box.left && x <= bounding_box.right) {
                if (y === bounding_box.top-1 && direction === DOWN) {
                    return true;
                } else if (y === bounding_box.bottom+1 && direction === UP) {
                    return true;
                }
            }
            return false;
        }
        return goal_test;
    }

    function manhattan_heuristic(bounding_box) {
        // currently broken since it underestimate the remaining distance.
        function heuristic(point) {
            let x,y;
            [x,y, direction] = point;
            
            dx = Math.max(bounding_box.left-x, x-bounding_box.right, 0);
            dy = Math.max(bounding_box.top-y, y-bounding_box.bottom, 0);
            score = dx + dy;

            if (bounding_box.right<x && direction === RIGHT) {
                score += BEND_PENALTY;
            }
            if (bounding_box.left>x && direction === LEFT) {
                score += BEND_PENALTY;
            }
            if (bounding_box.bottom<y && direction === DOWN) {
                score += BEND_PENALTY;
            }
            if (bounding_box.top>x && direction === UP) {
                score += BEND_PENALTY;
            }

            return score;
        }
        return heuristic;
    }

    function condense_path(path) {
        /*
        Returns a collapsed version of |points| so that there are no three consecutive
        collinear points.
        */
        condensed = [path[0]];
        for (let i=1; i < path.length-1; i++) {
            let x, y, x_, y_, _x, _y;
            [_x, _y] = condensed[condensed.length-1];
            [x, y] = path[i];
            [x_, y_] = path[i+1];
            if ((Math.sign(x - _x) !== Math.sign(x_ - x)) || (Math.sign(y - _y) !== Math.sign(y_ - y))) {
                condensed.push(path[i]);
            }
        }
        condensed.push(path[path.length-1]);
        return condensed;
    }


    QUESTION_STATE.redrawStoredLines = () => {
        CANVAS = QUESTION_STATE.CANVAS;
        CTX = QUESTION_STATE.CTX;
        CTX.clearRect(0, 0, CANVAS.width(), CANVAS.height());
        for (path_data of QUESTION_STATE.STORED_PATHS) {
            let [path, color, start, end] = [path_data.path, path_data.color, path_data.start, path_data.end];
            CTX.strokeStyle = color;
            CTX.lineWidth = 1;
            if (QUESTION_STATE.DRAG_OBJECTS.some(e => e.is(end) || e.is(start))) {
                CTX.strokeStyle = color;
                CTX.lineWidth = 1;
                CTX.beginPath();
                from = QUESTION_STATE.getDotXY(start);
                to = QUESTION_STATE.getDotXY(end);
                CTX.moveTo(...from);
                CTX.lineTo(...to);
                CTX.stroke();
            } else {
                CTX.beginPath();
                CTX.moveTo(path[0][0], path[0][1]);

                var from, xc, yc;
                if (path.length > 2) {
                    for (i = 1; i < path.length - 2; i ++)
                    {
                        xc = (path[i][0] + path[i + 1][0]) / 2;
                        yc = (path[i][1] + path[i + 1][1]) / 2;
                        from = [xc, yc];
                        CTX.quadraticCurveTo(path[i][0], path[i][1], xc, yc);
                        // CTX.arc(xc, yc, 4, 0, 2 * Math.PI, false);
                    }
                    // curve through the last two points

                    // if the last bend is 10 away then we should set the last_control to 
                    // if (Math.abs(path[i+1][0] - path[i][0]) + Math.abs(path[i+1][1] - path[i][1]) <= 10) {
                    //     last_control = [(path[i+1][0] + path[i][0])/2, (path[i+1][1] + path[i][1])/2]
                    //     if (path[i-1][0] !== path[i][0]) {
                    //         last_control[0] = last_control[0] + 5*sign(path[i-1][0] - path[i][0])
                    //     } else {
                    //         last_control[1] = last_control[1] + 5*sign(path[i-1][1] - path[i][1])
                    //     }
                    // } else {
                    //     last_control = path[i];
                    // }
                    i = path.length - 1;
                    xc = (path[i-2][0] + 3*path[i-1][0]) / 4;
                    yc = (path[i-2][1] + 3*path[i-1][1]) / 4;
                    from = [xc, yc];
                    CTX.quadraticCurveTo(xc, yc, path[i][0], path[i][1]);
                    // CTX.lineTo(path[i][0], path[i][1]);
                } else {
                    from = path[0];
                    CTX.lineTo(path[1][0], path[1][1]);
                }

                to = path[path.length-1];
            }
            // Finally we draw the arrow head on the line
            var dx = to[0] - from[0];
            var dy = to[1] - from[1];
            var angle = Math.atan2(dy, dx);
            CTX.lineTo(to[0] - HEADLEN * Math.cos(angle - Math.PI / 6), to[1] - HEADLEN * Math.sin(angle - Math.PI / 6));
            CTX.moveTo(to[0], to[1]);
            CTX.lineTo(to[0] - HEADLEN * Math.cos(angle + Math.PI / 6), to[1] - HEADLEN * Math.sin(angle + Math.PI / 6));
            CTX.stroke();
        }
    }

    
    QUESTION_STATE.recalculateLines = () => {
        loader = QUESTION_STATE.DROPZONE.find(".loader")
        console.log("start recalc for q", QUESTION_STATE.CSQ_NAME)
        loader.removeClass("hidden");
        setTimeout(function(){
            recalculateLinesHelper();
            // console.log("loader add hidden", loader)
            QUESTION_STATE.DROPZONE.find(".loader").addClass("hidden");
        }, 20);
        
    }

    function recalculateLinesHelper() {
        COVERAGE_MAP = {};
        LINE_COVERAGE = {};
        STORED_PATHS = QUESTION_STATE.STORED_PATHS;
        // console.log("stored lines", STORED_LINES)
        STORED_PATHS.length = 0
        STORED_LINES = QUESTION_STATE.STORED_LINES;
        QUESTION_STATE.DROPZONE.find(".box").each(function() {
          add_box_coverage($(this));
        });
    
    
        // recalculate each stored line
        for (var i = 0; i < STORED_LINES.length; i++) {
          let startObject = STORED_LINES[i].start;
          let parent_box = null;
          if (startObject.hasClass("set-entry")) {
            parent_box = getParentBox(startObject);
            remove_box_coverage(parent_box);
          }
    
          if (startObject.hasClass("vert-start")) {
            path = find_path_vertical(startObject, STORED_LINES[i].end);
          } else if (startObject.hasClass("any-start")) {
            path = find_path_any_direction(startObject, STORED_LINES[i].end);
          } else {
            path = find_path(startObject, STORED_LINES[i].end);
          }
    
          if (parent_box !== null) {
            add_box_coverage(parent_box);
          }
          
          if (startObject.hasClass("parent-frame-ptr")) {
            color = "purple";
          } else if (startObject.hasClass("frameSource")) {
            color = "red";
          } else if (startObject.hasClass("classSource")){
            color = "green";
          } else {
            color = "blue";
          }
          for (var j = 1; j < path.length; j++) {
            add_line_coverage([path[j-1], path[j]]);
          }
          
          STORED_PATHS.push({"path":path, "color":color, "start":startObject, "end":STORED_LINES[i].end});
          
        }
        QUESTION_STATE.redrawStoredLines();
        // mark SETUP_COMPLETE as True so that resize Observers can recalculate lines
        setTimeout(() => {QUESTION_STATE.SETUP_COMPLETE = true;}, 500);
        // console.log("finish recalc")
    }

    function add_line_coverage(line) {
        let start, end, x1, y1, x2, y2;
        [start, end] = line;
        [x1, y1] = start;
        x1 = round_to_grid(x1);
        y1 = round_to_grid(y1);
        [x2, y2] = end;
        x2 = round_to_grid(x2);
        y2 = round_to_grid(y2);
        let direction = "horiz";
        if (x1 === x2) {
            direction = "vert";
            for (j = Math.min(y1, y2); j <= Math.max(y1, y2); j++) {
                LINE_COVERAGE[[x1, j]] = direction;
            }
        } else {
            for (i = Math.min(x1, x2); i <= Math.max(x1, x2); i++) {
                LINE_COVERAGE[[i, y1]] = direction;
            }
        }
      }
      
      function find_path(start_object, end_object){
        end_box = QUESTION_STATE.boundingBox(end_object, GRID_SIZE);
        start_box = getParentBox(start_object)
        start_box_bounds = QUESTION_STATE.boundingBox(start_box)
        start_pos =  QUESTION_STATE.getDotXY(start_object)
        start_point = [round_to_grid(start_pos[0]),round_to_grid(start_pos[1])]
        
        if (start_object.hasClass("left-start")) {
          start_pos = [start_pos[0], round_to_grid(start_pos[1])*GRID_SIZE]
          next_point = [start_box_bounds.right, start_point[1], RIGHT]
        } else if (start_object.hasClass("bottom-start")) {
          next_point = [start_point[0], start_box_bounds.bottom + 1];
          initial_direction = "vert";
        } else {
          next_point = [start_point[0], start_box_bounds.top - 1];
          initial_direction = "vert";
        }
      
        // const neighb_func = grid_neighbors_init(initial_direction=initial_direction);
        path = a_star(next_point, box_goal_maker(end_box), grid_neighbors, heuristic=manhattan_heuristic(end_box));
        scale_path(path);
        path.unshift(start_pos);
        return condense_path(path);
      }
      
      function find_path_vertical(start_object, end_object) {
        end_box = boundingBox(end_object, GRID_SIZE);
        start_box = getParentBox(start_object)
        start_box_bounds = boundingBox(start_box)
        start_pos =  QUESTION_STATE.getDotXY(start_object)
        start_point = [round_to_grid(start_pos[0]),round_to_grid(start_pos[1])]
        const neighb_func = grid_neighbors_init(initial_direction="vert");
        next_point = [start_point[0], start_box_bounds.top - 1];
        extra_point = [start_point[0], start_box_bounds.bottom + 1];
        path = a_star(next_point, box_goal_maker(end_box), neighb_func, heuristic=manhattan_heuristic(end_box), extra_starts=[extra_point]);
        scale_path(path);
        path.unshift(start_pos);
        return condense_path(path);
      }
      
      function find_path_any_direction(start_object, end_object) {
        end_box = boundingBox(end_object, GRID_SIZE);
        start_box = getParentBox(start_object)
        start_box_bounds = boundingBox(start_box)
        start_pos =  QUESTION_STATE.getDotXY(start_object)
        start_point = [round_to_grid(start_pos[0]),round_to_grid(start_pos[1]), null]
        path = a_star(start_point, box_goal_maker(end_box), grid_neighbors, heuristic=manhattan_heuristic(end_box));
        scale_path(path);
        return condense_path(path);
      }
      
      function scale_path(path) {
        for (var j = 0; j < path.length; j++) {
          path[j] = [path[j][0]*GRID_SIZE, path[j][1]*GRID_SIZE];
        }
      }

})(QUESTION_STATE || {})