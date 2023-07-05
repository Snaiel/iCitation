var textarea = document.getElementById('input-text');
var button = document.getElementById('input-text-button');

textarea.addEventListener('input', function() {
  button.disabled = textarea.value.trim() === '';
});