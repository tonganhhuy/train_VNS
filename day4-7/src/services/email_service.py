import asyncio
class EmailService:
    @staticmethod
    async def send_welcome_email(email: str, username: str):
        print(f"\n[BACKGROUND TASK] Bắt đầu gửi email chào mừng tới: {email}...")
        
        await asyncio.sleep(3) 
        
        print(f"[BACKGROUND TASK] ✅ Gửi thành công! {username} hãy kiểm tra hòm thư {email} nhé.\n")