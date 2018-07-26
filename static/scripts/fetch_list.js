// Create an event listener for the button
const button = document.querySelector('#getListButton');
button.addEventListener('click', () => {
  // Ask the server for the list of items
  const url = '/list_items';
  const options = {
    // Call the get method
    method: 'GET',
    // Need to tell App Engine that we're coming from the same place.
    credentials: 'same-origin',
  };

  // Create an HTTP request object
  const request = new Request(url, options);
  // Send our request to the server
  fetch(request).then((response) => {
    return response.json();
  }).then((itemList) => {
    // Create elements for all the list items
    // Add the list item elements to the html
    const listHolderElement = document.querySelector('#list');
    for (let i = 0; i < itemList.length; i++) {
      let itemText = itemList[i];
      let itemElement = document.createElement('li');
      itemElement.innerHTML = itemText;
      listHolderElement.append(itemElement);
    }
  });
});
