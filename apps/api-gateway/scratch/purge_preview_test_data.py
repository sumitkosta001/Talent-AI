import asyncio
from sqlalchemy import select
from app.database.session import SessionLocal
from app.models.user import User
from app.models.resume import Resume

async def purge():
    async with SessionLocal() as db:
        # Delete resume records that are left over from crashes
        res = await db.execute(select(Resume))
        resumes = res.scalars().all()
        deleted_resumes_count = 0
        deleted_users_count = 0
        for r in resumes:
            if r.stored_filename and ("stored_db_" in str(r.stored_filename) or "prev_" in str(r.original_filename) or "del_" in str(r.original_filename)):
                await db.delete(r)
                deleted_resumes_count += 1
                
        # Delete test users starting with prev_ or del_
        for prefix in ["prev_%", "del_%"]:
            res = await db.execute(select(User).where(User.email.like(prefix)))
            users = res.scalars().all()
            deleted_users_count += len(users)
            for u in users:
                await db.delete(u)
            
        await db.commit()
        print(f"Purged {deleted_resumes_count} leftover test resumes and {deleted_users_count} test users.")

if __name__ == "__main__":
    asyncio.run(purge())
