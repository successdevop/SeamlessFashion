import asyncio
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dispatcher.dispatch import EventDispatcher
from app.enums.user_enums import OutboxStatus
from app.repositories.outbox import OutboxRepository
from base_models.out_box import OutboxMessage


class OutboxWorker:
    def __init__(self, dispatcher: EventDispatcher, session_factory:async_sessionmaker[AsyncSession] ) -> None:
        self.session_factory = session_factory
        self.dispatch = dispatcher
        self.running = True
        self.max_attempts = 10

    async def process_batch(self) -> None:
        async with self.session_factory() as session:
            outbox_repo = OutboxRepository(session=session)
            messages = await outbox_repo.claim_messages(limit=10)

            for message in messages:
                await self.process_message(message)

    async def process_message(self, message: OutboxMessage) -> None:
        async with self.session_factory() as session:
            try:
                await self.dispatch.dispatch(event_type=message.event_type, event_id=message.id, payload=message.payload)

                stmt = select(OutboxMessage).where(OutboxMessage.id == message.id)
                result = await session.exec(stmt)
                current = result.one()

                current.status = OutboxStatus.PROCESSED
                current.processed_at = datetime.now(tz=timezone.utc)
                current.last_error = None
                await session.commit()
            except Exception as exc:
                await session.rollback()

                stmt = select(OutboxMessage).where(OutboxMessage.id == message.id)
                current = (await session.exec(stmt)).one()

                if current is None:
                    return None

                if current.attempts >= self.max_attempts:
                    current.status = OutboxStatus.FAILED
                else:
                    current.status = OutboxStatus.PENDING

                    retry_seconds = min(3600, 5 * (2 ** max(current.attempts -1, 0)))

                    current.available_at = datetime.now(tz=timezone.utc) + timedelta(seconds=retry_seconds)

                    current.last_error = str(exc)
                    await session.commit()

    async def run(self) -> None:
        print("Outbox worker started")
        while self.running:
            try:
                await self.process_batch()
            except Exception as exc:
                print(f"Worker error: {exc}")

            await asyncio.sleep(2)
