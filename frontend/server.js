const updateData = (imageLink, callback) => {
    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    // Open a connection to the server
    xhr.open('POST', 'https://classificationofnumberbackend.onrender.com/', true);

    // Set the request headers
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Send the request
    xhr.send({ "imageLink": imageLink });

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let response = JSON.parse(xhr.responseText)
            callback(response);
        }
    }
};

export { updateData };