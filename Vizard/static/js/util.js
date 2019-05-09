function time(val) {
  let d = new Date(val);
  let D = d.getDate();
  let M = d.getMonth() + 1;
  let h = d.getHours();
  let m = d.getMinutes();
  let s = d.getSeconds();
  let ms = Math.round(d.getMilliseconds() / 10);
  return D + "." + M + " " + h + ":" + m + ":" + s + "." + ms;
}

function range(start, end, step) {
  let step_val = step;
  let step_index = 0;
  if (isNaN(start)) {
    let el = start.split(/[:\-]/);
    start = el[0];
    end = el[1];
    step = step || 1;
    return range(parseInt(start), parseInt(end), parseInt(step));
  } else if (!isNaN(start) && !isNaN(end)) {
    if (step.length > 1 && step_index < step.length) {
      step_val = step[Math.min(step.length, step_index)];
    }
    let range = [];
    if (end < start) {
      for (let i = start; i > end; i -= step_val) {
        range.push(i);
        if (step.length > 1 && step_index < step.length) {
          step_val = step[Math.min(step.length, step_index++)];
        }
      }
    } else {
      for (let i = start; i < end; i += step_val) {
        range.push(i);
        if (step.length > 1 && step_index < step.length) {
          step_val = step[Math.min(step.length, step_index++)];
        }
      }
    }
    return range;
  }

  return [];
}

function merge(first, second) {
  let cpy = Object.assign({}, first);
	for (var prop in second) {
		if (second.hasOwnProperty(prop)) {
			cpy[prop] = second[prop];
		}
	}
	return cpy;
}