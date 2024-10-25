import asyncio
import aiohttp
import json

async def fetch_greeting():
    url = 'http://localhost:9001/'
    headers = {
        'Content-Type': 'application/json',
    }
    query = {
        'query': 'query { greeting }'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(query)) as response:
            if response.status == 200:
                data = await response.json()
                return data['data']['greeting']
            else:
                raise Exception(f"Failed to fetch greeting, status code: {response.status}")

# To run the async function and process the result:
async def main():
    greeting = await fetch_greeting()
    print(f"Greeting: {greeting}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
