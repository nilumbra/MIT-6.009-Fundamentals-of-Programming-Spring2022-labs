var QUESTION_STATE = (function (QUESTION_STATE) {

  QUESTION_STATE.Node = (val, priority, distance) => {
    return {
      distance:distance,
      val:val,
      priority:priority,
    }
  }

  QUESTION_STATE.MinHeap = (values = [], pointers = {}) => {

    const length = () => {
      return values.length;
    }

    const has = (value) => {
      return (value in pointers);
    }

    const get = (value) => {
        return pointers[value];
    }

    const insert = (val, priority, distance) => {
      let newNode = QUESTION_STATE.Node(val, priority, distance);
        values.push(newNode);
      let index =   values.length - 1;
        pointers[val] = index;
      const current =   values[index];

      while (index > 0) {
        let parentIndex = Math.floor((index - 1) / 2);
        let parent =   values[parentIndex];

        if (parent.priority > current.priority) {
            values[parentIndex] = current;
            pointers[current.val] = parentIndex;
            values[index] = parent;
            pointers[parent.val] = index;
          index = parentIndex;
        } else break;
      }
    }

    const extract_min = () => {
      if (values.length === 1) {
          const end = values.pop();
          delete pointers[end.index];
          return end;
      }
      const min = values[0];
      const end = values.pop();
      values[0] = end;
      delete pointers[min.val];

      let index = 0;
      const length = values.length;
      const current = values[0];
      while (true) {
        let leftChildIndex = 2 * index + 1;
        let rightChildIndex = 2 * index + 2;
        let leftChild, rightChild;
        let swap = null;

        if (leftChildIndex < length) {
          leftChild =   values[leftChildIndex];
          if (leftChild.priority < current.priority) swap = leftChildIndex;
        }
        if (rightChildIndex < length) {
          rightChild =   values[rightChildIndex];
          if (
            (swap === null && rightChild.priority < current.priority) ||
            (swap !== null && rightChild.priority < leftChild.priority)
          )
            swap = rightChildIndex;
        }

        if (swap === null) break;
          values[index] =   values[swap];
          pointers[  values[swap].val] = index;
          values[swap] = current;
          pointers[current.val] = swap;
        index = swap;
      }

      return min;
    }

    const decrease_key = (val, priority, distance) => {
      let index =   pointers[val];
      const current =   values[index];
      current.distance = distance;
      current.priority = priority;


      while (index > 0) {
        let parentIndex = Math.floor((index - 1) / 2);
        let parent =   values[parentIndex];

        if (parent.priority > current.priority) {
            values[parentIndex] = current;
            pointers[current.val] = parentIndex;
            values[index] = parent;
            pointers[parent.val] = index;
          index = parentIndex;
        } else break;
      }
    }
  

    return {
      length,
      has,
      get,
      insert,
      extract_min,
      decrease_key
    }
  }

  return QUESTION_STATE;

})(QUESTION_STATE || {})