// Add an event listener to listen for the button click
const addButton = document.querySelector('#addButton');
addButton.addEventListener('click', (event) => {
  event.preventDefault();

  const newItemInputEl = document.querySelector('#newListItem');

  // Call the server with the new item text
  saveNewItem(newItemInputEl.value);

  // Create a new list element
  const newListElement = createListElement(newItemInputEl.value);
  // Add it to the page
  const lastElement = document.querySelector('#last');
  lastElement.insertAdjacentElement('beforebegin', newListElement);
  // Clear old user input
  newItemInputEl.value = '';
});

function saveNewItem(newItem) {
  // URL is of the form '/<my_path>?<key1>=<value1>&<key2>=<value2>'
  const url = '/todo?list_item=' + newItem;
  const options = {
    method: 'POST',
    // Need to tell App Engine that we're coming from the same place.
    credentials: 'same-origin',
  };

  // Create an HTTP request object
  const request = new Request(url, options);
  // Send our request to the server
  fetch(request);
}

function createListElement(newItem) {
  const htmlText = '<span>' + newItem + '</span>' +
                   '<span class="spacer"></span>' +
                   '<span class="delete">' +
                     '<img src="static/images/noun_Delete_1272081.svg">' +
                   '</span>';
  const element = document.createElement('li');
  element.innerHTML = htmlText;
  return element;
}
