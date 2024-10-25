// Define an asynchronous function that fetches the 'greeting' from the GraphQL server.
async function fetchGreeting() {
    // Use the 'fetch' API to send a POST request to the GraphQL server running on localhost at port 9001.
    const response = await fetch('http://localhost:9001/', {
        method: 'POST',  // Specifies that this is a POST request.
        headers: {
            // Set the request header to indicate that the request body contains JSON data.
            'Content-Type': 'application/json',
        },
        // The 'body' contains the GraphQL query serialized as a JSON string.
        // This query asks for the 'greeting' field from the server's 'Query' type.
        body: JSON.stringify({
            query: 'query { greeting }',  // This is a simple GraphQL query requesting the 'greeting' field.
        }),
    });

    // Wait for the response, and parse it as JSON.
    // The response should contain the 'data' object, which holds the result of the query.
    const { data } = await response.json();

    // Return the value of the 'greeting' field from the server's response.
    return data.greeting;
}

// Call the 'fetchGreeting' function and handle the promise it returns.
fetchGreeting().then((greeting) => {
    // Once the greeting is fetched, find the HTML element with the ID 'greeting' 
    // and update its text content with the value of 'greeting' from the server.
    document.getElementById('greeting').textContent = greeting;
});
