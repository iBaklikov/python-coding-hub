# Import necessary modules for asynchronous operations and HTTP requests
import asyncio  # Provides tools for writing asynchronous code in Python
import aiohttp  # A library for making asynchronous HTTP requests
import json  # For encoding and decoding JSON data

# Define an asynchronous function to fetch the 'greeting' from the GraphQL server
async def fetch_greeting():
    # The URL of the GraphQL server (assumed to be running on localhost at port 9001)
    url = 'http://localhost:9001/'
    
    # Headers to specify that the request body will be in JSON format
    headers = {
        'Content-Type': 'application/json',
    }
    
    # The GraphQL query as a Python dictionary. This query requests the 'greeting' field.
    query = {
        'query': 'query { greeting }'
    }

    # Create an asynchronous HTTP session using aiohttp
    async with aiohttp.ClientSession() as session:
        # Send a POST request to the server with the query in the request body
        async with session.post(url, headers=headers, data=json.dumps(query)) as response:
            # Check if the request was successful (HTTP status code 200)
            if response.status == 200:
                # Parse the response as JSON and await its completion
                data = await response.json()
                
                # Return the 'greeting' field from the server's response
                return data['data']['greeting']
            else:
                # Raise an exception if the server response status is not 200
                raise Exception(f"Failed to fetch greeting, status code: {response.status}")

# Define an asynchronous function to run the fetch_greeting function and handle the result
async def main():
    # Await the result of the fetch_greeting function
    greeting = await fetch_greeting()
    
    # Print the fetched greeting to the console
    print(f"Greeting: {greeting}")

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Run the main function using asyncio's event loop
    asyncio.run(main())