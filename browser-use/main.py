from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task="""
        1. go to  https://fp.trafikverket.se/Boka/ng/
        2. Click on the "Logga in" button
        3. Select "Mobilt BankID" as the authentication method
        4. Wait for the QR code to appear
        5. Take a screenshot of the QR code
        """,
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    await agent.run()

asyncio.run(main())