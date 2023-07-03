document.addEventListener('DOMContentLoaded', function() {
    var addButton = document.getElementById('add-button');
    var inputField = document.getElementById('input-field');
    var displayArea = document.getElementById('display-area');
    var submitForm = document.getElementById('submit-form');
    var formDataInput = document.getElementById('sources-to-add');
    var textList = [];

    addToSource = () => {
        var text = inputField.value;
        if (text) {
            text = text.split(" ")
            text.forEach(function(source, index) {
                textList.push(source);
                displayArea.innerHTML += '<p>' + source + '</p>';
                inputField.value = '';
            });
        }
    }

    addButton.addEventListener('click', function(event) {
        event.preventDefault();
        addToSource();
    });

    inputField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
          event.preventDefault();
          addToSource();
        }
      });

    submitForm.addEventListener('submit', function(event) {
        event.preventDefault();
        formDataInput.value = JSON.stringify(textList);
        submitForm.submit();
    });
});