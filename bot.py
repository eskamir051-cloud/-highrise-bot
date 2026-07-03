import asyncio
from highrise import BaseBot
from highrise.models import Position

class Bot(BaseBot):
    welcome_text = "سلام {user} عزیز، به اتاق ما خوش اومدی! 🌟"
    leave_text = "خداحافظ {user} 😢 به امید دیدار مجدد"

    dances = [
        "dance-macarena",
        "dance-tiktok8",
        "dance-blackpink",
        "dance-russian",
        "dance-handsup",
        "dance-pennywise",
        "dance-weird",
        "dance-shoppingcart",
        "dance-lazy"
    ]

    async def on_user_join(self, user, position: Position):
        await self.highrise.chat(self.welcome_text.format(user=user.username))

    async def on_user_leave(self, user):
        await self.highrise.chat(self.leave_text.format(user=user.username))

    async def on_chat(self, user, message: str):
        text = message.strip()

        if text == "!help":
            await self.highrise.chat("دستورات: !spam [متن] | !tp [x y z] | !tip [username] [amount] | !dance | !dancelist")
            return

        if text == "!dance":
            await self.highrise.chat("شروع دنس... 💃")
            for emote_id in self.dances:
                try:
                    await self.highrise.perform_emote(emote_id)
                    await asyncio.sleep(2.5)
                except Exception:
                    pass
            return

        if text == "!dancelist":
            await self.highrise.chat(", ".join(self.dances))
            return

        if text.startswith("!spam "):
            spam_content = text.replace("!spam ", "", 1)
            await self.highrise.chat("شروع اسپم...")
            for _ in range(5):
                await self.highrise.chat(spam_content)
                await asyncio.sleep(0.6)
            return

        if text.startswith("!tp "):
            parts = text.split()
            if len(parts) == 4:
                try:
                    x = float(parts[1])
                    y = float(parts[2])
                    z = float(parts[3])
                    await self.highrise.teleport(user.id, Position(x=x, y=y, z=z))
                    await self.highrise.chat(f"{user.username} با موفقیت تلپورت شد ✔️")
                except ValueError:
                    await self.highrise.chat("فرمت اشتباه است! مثال: !tp 11.5 0 2.5")
            else:
                await self.highrise.chat("فرمت صحیح: !tp x y z")
            return

        if text.startswith("!tip "):
            parts = text.split()
            if len(parts) == 3:
                target_username = parts[1]
                try:
                    amount = int(parts[2])
                except ValueError:
                    await self.highrise.chat("مقدار گلد باید عدد باشد!")
                    return

                users = await self.highrise.get_room_users()
                target_user = None

                for room_user, _ in users.content:
                    if room_user.username.lower() == target_username.lower():
                        target_user = room_user
                        break

                if target_user:
                    try:
                        await self.highrise.tip_user(target_user.id, amount)
                        await self.highrise.chat(f"مقدار {amount} گلد به {target_user.username} انتقال یافت 🪙")
                    except Exception as e:
                        await self.highrise.chat("خطا در ارسال گلد! (شاید موجودی بات کافی نیست)")
                else:
                    await self.highrise.chat("کاربر در این اتاق پیدا نشد! ❌")
            else:
                await self.highrise.chat("فرمت صحیح: !tip username amount")
            return
