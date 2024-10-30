#backend\tests\test_rate_limit.py
import asyncio
import httpx

async def get_access_token():
    url = "http://localhost:8000/auth/login"
    login_data = {
        "username": "testuser",  # replace with actual username
        "password": "testpass123",  # replace with actual password
        "grant_type": "password"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=login_data)
        response.raise_for_status()  # Ensure no HTTP errors
        return response.json()["access_token"]

async def test_rate_limit():
    access_token = await get_access_token()
    url = "http://localhost:8000/files/"  # Replace with an actual endpoint
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        for i in range(110):  # Try more than `max_requests` to trigger rate limiting
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                print(f"Request {i+1}: Success - Status Code {response.status_code}")
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 429:
                    print(f"Request {i+1}: Rate limit exceeded - Status Code {exc.response.status_code}")
                else:
                    print(f"Request {i+1}: Error {exc.response.status_code}: {exc.response.text}")

# Run the test function
asyncio.run(test_rate_limit())
