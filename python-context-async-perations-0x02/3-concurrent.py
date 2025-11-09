import asyncio
import aiosqlite


# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        print("[INFO] Fetching all users...")
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("[INFO] Fetched all users.")
            return users


# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        print("[INFO] Fetching users older than 40...")
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("[INFO] Fetched older users.")
            return older_users


# Function to run both queries concurrently
async def fetch_concurrently():
    print("[INFO] Running queries concurrently...")
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("\n✅ Concurrent Query Results:")
    print("All Users:", users)
    print("Older Users (>40):", older_users)


# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

