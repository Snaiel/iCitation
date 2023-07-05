var citationButtons = document.getElementsByClassName('citation');

function copyToClipboard(text) {
  navigator.clipboard.writeText(text);
}

// Add click event listeners to citation buttons
for (var i = 0; i < citationButtons.length; i++) {
  citationButtons[i].addEventListener('click', function(event) {
    var citationText = event.target.textContent.trim();
    copyToClipboard(citationText);
  });
}
