import discord
from discord.ext import commands
import io
import re

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

def dump_v12_6_large_file_engine(obfuscated_code):
    try:
        # 1. Định vị và cắt trực tiếp khối Hex Payload (né việc dùng Regex quét toàn bộ file 500KB)
        start_marker = "[=["
        end_marker = "]=]"
        
        start_idx = obfuscated_code.find(start_marker)
        end_idx = obfuscated_code.find(end_marker, start_idx)
        
        if start_idx == -1 or end_idx == -1:
            return "Error: Không tìm thấy khối Hex Payload block [=[...]=]"
            
        hex_block = obfuscated_code[start_idx + 3 : end_idx]
        # Bỏ 4 ký tự đầu (ví dụ "ABC:") để lấy chuỗi Hex thuần túy
        if ":" in hex_block:
            hex_payload = hex_block.split(":", 1)[1]
        else:
            hex_payload = hex_block

        # 2. Tìm kiếm chính xác khu vực chứa ma trận khóa (v_matrix)
        # Bản v12.6 luôn khởi tạo ma trận ngay sau khối Hex Payload hoặc gần cụm mã dịch
        matrix_start_idx = obfuscated_code.find("{{", end_idx)
        if matrix_start_idx == -1:
            # Tìm kiếm diện rộng nếu cấu trúc bị đảo
            matrix_start_idx = obfuscated_code.find("{{")
            
        if matrix_start_idx == -1:
            return "Error: Không thể định vị được vùng chứa Ma trận khóa."

        # Trích xuất phân đoạn chứa ma trận dựa trên đóng mở ngoặc nhọn
        level = 0
        matrix_end_idx = -1
        for i in range(matrix_start_idx, len(obfuscated_code)):
            if obfuscated_code[i] == '{':
                level += 1
            elif obfuscated_code[i] == '}':
                level -= 1
                if level == 0:
                    matrix_end_idx = i + 1
                    break

        if matrix_end_idx == -1:
            return "Error: Cấu trúc ma trận khóa bị lỗi cú pháp hoặc cắt cụt."

        matrix_raw = obfuscated_code[matrix_start_idx:matrix_end_idx]
        
        # Bóc tách các cặp tính toán số học
        pairs = re.findall(r'\{\s*([^\},]+)\s*,\s*([^\}]+)\s*\}', matrix_raw)
        if not pairs:
            return "Error: Không bóc tách được các cặp khóa con."

        matrix = []
        for obf_key, obf_offset in pairs:
            try:
                # Làm sạch ký tự lạ của Lua
                k_str = obf_key.replace(';', '').replace('{', '').replace('}', '').strip()
                o_str = obf_offset.replace(';', '').replace('{', '').replace('}', '').strip()
                
                # Tính toán giá trị số trong môi trường cô lập an toàn
                key_val = int(eval(k_str, {"__builtins__": None}, {}))
                offset_val = int(eval(o_str, {"__builtins__": None}, {}))
                matrix.append([key_val, offset_val])
            except:
                continue

        if not matrix:
            return "Error: Quá trình giải toán ma trận khóa thất bại."

        # 3. CHUYỂN ĐỔI CHUỖI HEX THÀNH ARRAY SỐ NGUYÊN (Tối ưu hóa tốc độ cực hạn)
        # Thay vì xử lý cắt chuỗi Hex trong vòng lặp, ta biến nó thành mảng byte ngay từ đầu
        try:
            cipher_bytes = bytearray.fromhex(hex_payload)
        except Exception:
            return "Error: Chuỗi mã hóa Hex chứa ký tự lỗi, không thể chuyển đổi."

        decoded_bytes = bytearray(len(cipher_bytes))
        byte_idx = 0

        # 4. VÒNG LẶP KHÔI PHỤC SIÊU TỐC (Bitwise Loop Optimization)
        for idx in range(len(cipher_bytes)):
            dec_byte = cipher_bytes[idx]

            # Đi ngược qua bộ lọc mô phỏng cổng XOR/AND
            for k_layer in matrix:
                k_val = k_layer[0]
                v_x = 0
                # Tối ưu hóa biểu thức Bitwise thay thế cho vòng lặp toán của Lua
                for v_m in range(8):
                    if ((dec_byte >> v_m) & 1) != ((k_val >> v_m) & 1):
                        v_x |= (1 << v_m)
                dec_byte = v_x

            decoded_bytes[idx] = dec_byte

            # Tiến hành xoay ma trận khóa liên hoàn
            for k_layer in matrix:
                k_layer[0] = (k_layer[0] + byte_idx + k_layer[1]) % 256

            byte_idx += 1

        return decoded_bytes.decode('utf-8', errors='ignore')

    except Exception as e:
        return f"Error trong quá trình xử lý file lớn: {str(e)}"

@bot.command(name="dump")
async def dump_command(ctx, *, text_code: str = None):
    target_code = None
    if ctx.message.attachments:
        try:
            # Tăng giới hạn đọc file lớn không bị ngắt quãng dòng dữ liệu
            target_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
        except:
            return await ctx.reply("⚠️ Không thể tải hoặc đọc file đính kèm từ Discord.")
    elif text_code:
        target_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
        
    if not target_code or not target_code.strip():
        return await ctx.reply("⚠️ Vui lòng đính kèm file hoặc dán đoạn mã cần dump.")

    status_msg = await ctx.reply("🚀 **Engine v12.6 [Large-File Mode]**: Đang xử lý cấu trúc file lớn...")
    try:
        result = dump_v12_1_large_file_engine(target_code) if len(target_code) < 50000 else dump_v12_6_pure_math_engine_large(target_code)
        
        # Chạy hàm xử lý tối ưu
        result = dump_v12_6_large_file_engine(target_code)
        await status_msg.delete()
        
        if result.startswith("Error"):
            await ctx.reply(f"⚠️ {result}")
        else:
            file_stream = io.BytesIO(result.encode('utf-8'))
            await ctx.reply(
                content=f"{ctx.author.mention} ✅ **Dump thành công file lớn!**",
                file=discord.File(file_stream, filename="dumped_large_source.lua")
            )
    except Exception as e:
        if 'status_msg' in locals():
            try: await status_msg.delete()
            except: pass
        await ctx.reply(f"❌ Hệ thống quá tải: {str(e)}")

bot.run("YOUR_BOT_TOKEN_HERE")
