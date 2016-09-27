function Editor(input, preview) {
  this.update = function () {
    preview.innerHTML = markdown.toHTML(input.value);
  };
  input.editor = this;
  this.update();
}
var $ = function (id) { return document.getElementById(id); };
window.onload = function () {
  new Editor($("id_text"), $("id_preview"));
  $("id_text").oninput = function(){ this.editor.update(); };
}
