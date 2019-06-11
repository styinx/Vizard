function v_index(number) {
  if (number % 10 === 1) {
    return number + 'st';
  } else if (number % 10 === 2) {
    return number + 'nd';
  } else if (number % 10 === 3) {
    return number + 'rd';
  } else {
    return number + 'th';
  }
}

function v_number(number, noun) {
  if (number === 1) {
    return number + ' ' + noun;
  } else {
    return number + ' ' + noun + 's';
  }
}

function v_capital(text, capital) {
  if (capital) {
    return text[0].toUpperCase() + text.substr(1);
  } else {
    return text;
  }
}

function v_tag(text, tag) {
  return '<' + tag + '>' + text + '</' + tag + '>';
}

function b(text) {
  return v_tag(text, 'b');
}

function i(text) {
  return v_tag(text, 'i');
}

function u(text) {
  return v_tag(text, 'u');
}

function s(text) {
  return v_tag(text, 's');
}