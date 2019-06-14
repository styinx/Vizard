function toggleVisibility(el, timeout = 0, soft = false) {
  let e = $(el);

  if (timeout === 0) {
    if (e.is(":hidden")) {
      e.show();
      if (soft)
        e.css('display', 'inline-block');
    } else
      e.hide();
  } else {
    if (e.is(":hidden"))
      e.delay(timeout).show();
    else
      e.delay(timeout).hide();
  }
}

function validate(what, el) {
  let patterns = {
    "url": /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi
  };

  let result = patterns[what].test($(el).val());

  $(el).css('padding', '0.1em 0.4em');

  if (result)
    $(el).css('border', 'calc(1px + 0.1em) solid green');
  else
    $(el).css('border', 'calc(1px + 0.1em) solid red');
}

function pad(val) {
  if (Math.log10(val) < 1) {
    return "0" + val;
  }
  return val;
}

function dec(val, decimals=2) {
  return val.toFixed(decimals);
}

function padT(text, width = 5) {
  let space = " ";
  let t = text + "";
  if (t.length < width)
    return space.repeat(width - t.length) + t + space;
  return text;
}

function time(val, format = "%d.%m.%Y %H:%M:%S.%f") {
  let d = new Date(val);
  let D = pad(d.getDate());
  let M = pad(d.getMonth() + 1);
  let Y = d.getFullYear();
  let h = pad(d.getHours());
  let m = pad(d.getMinutes());
  let s = pad(d.getSeconds());
  let ms = Math.round(d.getMilliseconds() / 10);
  return format
    .replace("%d", D)
    .replace("%m", M)
    .replace("%Y", Y)
    .replace("%H", h)
    .replace("%M", m)
    .replace("%S", s)
    .replace("%f", ms);
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