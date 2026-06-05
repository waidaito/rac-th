import discord
from discord.ext import commands
import io
import re
import threading
import os
from flask import Flask

# KHỞI TẠO WEB SERVER CHO RENDER QUÉT PORT
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot đang chạy ổn định!"

def run_server():
    # Sử dụng cổng 8000 theo yêu cầu của bro (mặc định lấy từ biến môi trường PORT nếu có, nếu không sẽ là 8000)
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

def clean_lua_math(expr):
    return expr.replace(';', '').replace('{', '').replace('}', '').strip()

def dump_v12_6_pure_math_engine(obfuscated_code):
    try:
        hex_block_match = re.search(r'\[=\[[A-Z]{3}:([0-9A-Fa-f]+)\]=\]', obfuscated_code)
        if not hex_block_match:
            return "Error: Không tìm thấy khối Hex Payload hợp lệ."
        hex_payload = hex_block_match.group(1)

        matrix_match = re.search(r'\{\s*(\{[^{}]+\}\s*,\s*)*\{[^{}]+\}\s*\}', obfuscated_code)
        if not matrix_match:
            matrix_match = re.search(r'\{\s*(\(\s*[0-9xX_a-Fa-f\+\-\(\)]+\s*\)\s*,\s*\(\s*[0-9xX_a-Fa-f\+\-\(\)]+\s*\)\s*\,?\s*)+\}', obfuscated_code)
            
        if not matrix_match:
            return "Error: Không thể định vị được ma trận khóa (Matrix Anchor)."
            
        matrix_raw = matrix_match.group(0)
        pairs = re.findall(r'\{\s*([^\},]+)\s*,\s*([^\}]+)\s*\}', matrix_raw)
        if not pairs:
            return "Error: Mảng chứa các cặp khóa trống rỗng hoặc sai cú pháp."

        matrix = []
        for obf_key, obf_offset in pairs:
            try:
                cleaned_key = clean_lua_math(obf_key)
                cleaned_offset = clean_lua_math(obf_offset)
                key_val = int(eval(cleaned_key, {"__builtins__": None}, {}))
                offset_val = int(eval(cleaned_offset, {"__builtins__": None}, {}))
                matrix.append([key_val, offset_val])
            except:
                continue

        if not matrix:
            return "Error: Không thể giải mã hoặc tính toán được giá trị của bất kỳ tầng khóa nào."

        decoded_bytes = bytearray()
        byte_idx = 0
        payload_len = len(hex_payload)

        for i in range(0, payload_len, 2):
            if i + 2 > payload_len:
                break
            cipher_byte = int(hex_payload[i:i+2], 16)
            dec_byte = cipher_byte

            for k_layer in matrix:
                k_val = k_layer[0]
                v_x = 0
                for v_m in range(8):
                    if ((dec_byte >> v_m) & 1) != ((k_val >> v_m) & 1):
                        v_x |= (1 << v_m)
                dec_byte = v_x

            decoded_bytes.append(dec_byte)

            for k_layer in matrix:
                k_layer[0] = (k_layer[0] + byte_idx + k_layer[1]) % 256

            byte_idx += 1

        return decoded_bytes.decode('utf-8', errors='ignore')

    except Exception as e:
        return f"Lỗi trong quá trình xử lý giải mã: {str(e)}"

@bot.command(name="dump")
async def dump_command(ctx, *, text_code: str = None):
    target_code = None
    if ctx.message.attachments:
        try:
            target_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
        except:
            await ctx.reply("Error: Không thể đọc dữ liệu từ file đính kèm.")
            return
    elif text_code:
        target_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
        
    if not target_code:
        await ctx.reply("Error: Vui lòng cung cấp nội dung script hoặc đính kèm file cần dump.")
        return

    status_msg = await ctx.reply("⚡ Đang bóc tách ma trận toán học v12.6 (Pure Math-Gate)...")
    try:
        result = dump_v12_6_pure_math_engine(target_code)
        await status_msg.delete()
        
        if result.startswith("Error"):
            await ctx.reply(f"⚠️ {result}")
        else:
            file_stream = io.BytesIO(result.encode('utf-8'))
            await ctx.reply(
                content=f"{ctx.author.mention} **Dump thành công!** Source code gốc đã được khôi phục:",
                file=discord.File(file_stream, filename="dumped_pure_source.lua")
            )
    except Exception as e:
        if 'status_msg' in locals():
            await status_msg.delete()
        await ctx.reply(f"Lỗi hệ thống: {str(e)}")

if __name__ == "__main__":
    # Chạy Web Server Flask trên luồng phụ để Render không bị báo lỗi Port
    threading.Thread(target=run_server, daemon=True).start()
    
    # Khởi chạy bot bằng TOKEN lấy từ Environment Variables (Biến môi trường)
    bot.run(os.getenv("TOKEN"))
    
