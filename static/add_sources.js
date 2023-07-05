document.addEventListener('DOMContentLoaded', function() {
    let addButton = document.getElementById('add-button');
    let inputField = document.getElementById('input-field');
    let displayArea = document.getElementById('display-area-inner');
    let submitForm = document.getElementById('submit-form');
    let submitButton = document.getElementById('submit-button');

    let formDataSources = document.getElementById('sources-to-add');
    let formDataCitations = document.getElementById('sources-citations');

    let textList = [];

    addToSource = () => {
        var text = inputField.value;
        if (text) {
            text = text.split(" ")
            text.forEach(function(source) {
                textList.push(source);
                displayArea.innerHTML += '' +
                    '<div style="display: flex; margin-bottom: 0.5rem">' +
                    '<input type="text" class="add-source-input citation-input" placeholder="Author, Date">' +
                    '<span>' + source + '</span>' +
                    '</div>'
                inputField.value = '';
            });

            if (submitButton.disabled) {
                submitButton.disabled = false;
            }
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
        
        let citations = [];
        let citation_inputs = displayArea.querySelectorAll("input");
        console.log(citation_inputs);
        citation_inputs.forEach((val) => {
            citations.push(val.value)
        })
        
        formDataSources.value = JSON.stringify(textList);
        formDataCitations.value = JSON.stringify(citations);
        submitForm.submit();
    });
});