import discord
from discord.ext import commands
import random
import string
import io
import re
import threading
import os
from flask import Flask

# ----------------------------------------------------------------
# KHỞI TẠO WEB SERVER ĐỂ KEEP BOT ALIVE (Dành cho Replit/UptimeRobot)
# ----------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live"

def run_server():
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

# ----------------------------------------------------------------
# CẤU HÌNH DISCORD BOT
# ----------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# Hàm sinh tên biến ngẫu nhiên cho Lua VM
def random_var(length=6):
    first = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))
    return first + rest

# Bộ sinh toán học ẩn danh dành cho lõi VM và Key thật
def obfuscate_core_math(target):
    current_val = target
    ops_pool = []
    for _ in range(random.randint(2, 3)):
        op = random.choice(['+', '-'])
        rand_num = random.randint(100000, 500000)
        if op == '+':
            current_val = current_val - rand_num
            ops_pool.append(f"+{hex(rand_num)}" if random.choice([True, False]) else f"+{rand_num}")
        elif op == '-':
            current_val = current_val + rand_num
            ops_pool.append(f"-{hex(rand_num)}" if random.choice([True, False]) else f"-{rand_num}")
    start_style = random.choice(['normal', 'hex'])
    expr = hex(current_val) if start_style == 'hex' else str(current_val)
    for action in reversed(ops_pool):
        expr = f"({expr}{action})"
    return f"({expr})"

# Hàm sinh rác toán học siêu hỗn loạn dành riêng cho các dòng rác ngoài rìa
def generate_clean_advanced_junk(target):
    junk_mode = random.choice(['hex_ops_pool', 'negative_double', 'logical_inline', 'mixed_math_heavy'])
    
    if junk_mode == 'hex_ops_pool':
        current_val = target
        ops_pool = []
        for _ in range(random.randint(2, 4)):
            op = random.choice(['+', '-'])
            rand_num = random.randint(100000, 1500000)
            if op == '+':
                current_val -= rand_num
                ops_pool.append(f"+{hex(rand_num)}")
            else:
                current_val += rand_num
                ops_pool.append(f"-{hex(rand_num)}")
        expr = hex(current_val)
        for action in reversed(ops_pool):
            expr = f"({expr}{action})"
        return f"({expr})"
        
    elif junk_mode == 'negative_double':
        offset1 = random.randint(50000, 200000)
        offset2 = random.randint(10000, 40000)
        base = target + offset1 - offset2
        return f"(-(-{base}-{hex(offset1)})+{hex(offset2)})"
        
    elif junk_mode == 'logical_inline':
        rand_check = random.randint(100, 1000)
        rand_adder = random.randint(5000, 15000)
        if random.choice([True, False]):
            return f"({target - rand_adder} + ({rand_check} > 50 and {rand_adder} or 0))"
        else:
            return f"({target + rand_adder} - ({rand_check} < 50 and 0 or {rand_adder}))"
            
    else:
        return obfuscate_core_math(target)

# ----------------------------------------------------------------
# LÕI PHẦN MỀM MÃ HÓA V15.0 ULTIMATE GHOST ENGINE
# ----------------------------------------------------------------
def ironbrew_total_wrapped_v15_0(source_code):
    keys_count = random.randint(7, 12)
    keys_list = [random.randint(50, 255) for _ in range(keys_count)]
    
    # Mã hóa chuỗi nguồn bằng Multi-Key + Khóa cuộn động
    encrypted_hex_list = []
    current_keys = list(keys_list)
    for idx, byte in enumerate(source_code.encode('utf-8')):
        cipher_byte = byte
        for k in current_keys:
            cipher_byte = cipher_byte ^ k
        encrypted_hex_list.append(f"{cipher_byte:02X}")
        for k_idx in range(len(current_keys)):
            current_keys[k_idx] = (current_keys[k_idx] + idx + (k_idx + 3)) % 256

    hex_payload = "".join(encrypted_hex_list)
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    bytecode_string_block = f"[=[{fake_signature}:{hex_payload}]=]"
    
    # Mã hóa xáo trộn hàm nạp hệ thống loadstring và load
    hex_loadstring = "".join([f"{ord(c) ^ keys_list[0] ^ keys_list[-1]:02X}" for c in "loadstring"])
    hex_load = "".join([f"{ord(c) ^ keys_list[0] ^ keys_list[-1]:02X}" for c in "load"])
    len_ls, len_l = len(hex_loadstring), len(hex_load)
    
    # Tạo tên biến ngẫu nhiên cho lõi Lua VM
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_buffer, v_func, v_run = [random_var() for _ in range(4)]
    v_idx, v_pair, v_num, v_dec = [random_var() for _ in range(4)]
    v_loop_idx, v_env = random_var(), random_var()
    v_str1, v_str2, v_t_idx, v_t_pair = [random_var() for _ in range(4)]
    v_h_ls, v_h_l = random_var(), random_var()
    v_byte_idx = random_var()
    v_matrix, v_k_step, v_loop_k = random_var(), random_var(), random_var()
    
    # Biến phục vụ trích xuất vị trí biến ngẫu nhiên
    v_garbage, v_map_str, v_g_idx, v_pos, v_is_k = [random_var() for _ in range(5)]
    v_chunk, v_item = random_var(), random_var()
    v_temp_k, v_temp_o = random_var(), random_var() 

    total_junk_count = 2500
    junk_lines = []
    
    # Đảo ngược Key theo logic giải mã cấu trúc stack
    reversed_keys = list(enumerate(keys_list))
    reversed_keys.reverse()
    
    # Khởi tạo các cặp thực thể biến chứa thông tin Key và Hằng số cuộn
    secret_variables = []
    for k_idx, k_val in reversed_keys:
        var_k = random_var()
        var_o = random_var()
        secret_variables.append({"var": var_k, "val": obfuscate_core_math(k_val), "is_key": True})
        secret_variables.append({"var": var_o, "val": obfuscate_core_math(k_idx + 3), "is_key": False})
        
    # Tạo danh sách Pointer chỉ định vị trí ngẫu nhiên để trộn Key vào bãi rác (từ dòng 100 đến 2400)
    secret_positions = sorted(random.sample(range(100, total_junk_count - 100), len(secret_variables)))
    pointer_map_elements = []
    
    sec_idx = 0
    for i in range(total_junk_count):
        if sec_idx < len(secret_variables) and i == secret_positions[sec_idx]:
            sec_data = secret_variables[sec_idx]
            junk_lines.append(f"local {sec_data['var']}={sec_data['val']}")
            lua_index = i + 1
            pointer_map_elements.append(f"{lua_index:04X}")
            sec_idx += 1
        else:
            v_junk = random_var()
            rand_target = random.randint(50, 99999)
            # KỸ THUẬT PHÒNG THỦ AI: Trộn 30% rác toán học thuần túy trông giống hệt dòng chứa Key thật
            if random.random() < 0.3:
                junk_lines.append(f"local {v_junk}={obfuscate_core_math(rand_target)}")
            else:
                junk_lines.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
            
    flat_pointer_map = "-".join(pointer_map_elements)

    # Khởi tạo chuỗi thông dịch lõi ảo VM
    bit_and_interpreter_core = (
        f"local function {v_bit_func}({v_i},{v_j}) "
        f"local {v_x}=0; "
        f"for {v_m}=0,7 do "
        f"local {v_w}=({v_i}/({obfuscate_core_math(2)})^{v_m})%2; "
        f"local {v_res}=({v_j}/({obfuscate_core_math(2)})^{v_m})%2; "
        f"if {v_w}-{v_w}%1~={v_res}-{v_res}%1 then {v_x}={v_x}+({obfuscate_core_math(2)})^{v_m} end "
        f"end "
        f"return {v_x} "
        f"end; "
        f"local {v_bytecode}={bytecode_string_block}; "
        f"local {v_h_ls}=\"{hex_loadstring}\"; "
        f"local {v_h_l}=\"{hex_load}\"; "
        f"local {v_buffer}=\"\"; "
        f"for {v_loop_idx}={obfuscate_core_math(1)},{obfuscate_core_math(2)} do "
        f"if {v_loop_idx}=={obfuscate_core_math(1)} then "
        f"local h_clean=string.sub({v_bytecode},5); "
        f"local {v_matrix} = {{}}; "
        f"local {v_map_str} = \"{flat_pointer_map}\"; "
        f"local {v_is_k} = true; "
        f"local {v_temp_k}, {v_temp_o}; "
        f"for {v_chunk} in string.gmatch({v_map_str}, \"[^-]+\") do "
        f"local {v_pos} = tonumber({v_chunk}, 16); "
        f"local {v_item} = d_env_vars[{v_pos}]; " 
        f"if {v_is_k} then {v_temp_k} = {v_item}; {v_is_k} = false; else "
        f"{v_temp_o} = {v_item}; "
        f"{v_matrix}[(# {v_matrix}) + 1] = {{{v_temp_k}, {v_temp_o}}}; {v_is_k} = true; "
        f"end; "
        f"end; "
        f"local {v_byte_idx}=0; "
        f"for {v_idx}=1,#h_clean,2 do "
        f"local {v_pair}=string.sub(h_clean,{v_idx},{v_idx}+1); "
        f"local {v_num}=tonumber({v_pair},16); "
        f"local {v_dec}={v_num}; "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_dec}={v_bit_func}({v_dec},{v_matrix}[{v_loop_k}][1]); "
        f"end; "
        f"{v_buffer}={v_buffer}..string.char({v_dec}); "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_matrix}[{v_loop_k}][1]=({v_matrix}[{v_loop_k}][1]+{v_byte_idx}+{v_matrix}[{v_loop_k}][2])%256; "
        f"end; "
        f"{v_byte_idx}={v_byte_idx}+1; "
        f"end "
        f"elseif {v_loop_idx}=={obfuscate_core_math(2)} then "
        f"local {v_str1}, {v_str2} = \"\", \"\"; "
        f"local {v_matrix} = {{}}; "
        f"local {v_map_str} = \"{flat_pointer_map}\"; "
        f"local {v_is_k} = true; "
        f"local {v_temp_k}, {v_temp_o}; "
        f"for {v_chunk} in string.gmatch({v_map_str}, \"[^-]+\") do "
        f"local {v_pos} = tonumber({v_chunk}, 16); "
        f"local {v_item} = d_env_vars[{v_pos}]; "
        f"if {v_is_k} then {v_temp_k} = {v_item}; {v_is_k} = false; else "
        f"{v_temp_o} = {v_item}; "
        f"{v_matrix}[(# {v_matrix}) + 1] = {{{v_temp_k}, {v_temp_o}}}; {v_is_k} = true; "
        f"end; "
        f"end; "
        f"local {v_k_step}={v_bit_func}({v_matrix}[#{v_matrix}][1],{v_matrix}[1][1]); "
        f"for {v_t_idx}=1,{obfuscate_core_math(len_ls)},2 do "
        f"local {v_t_pair}=string.sub({v_h_ls},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then {v_str1}={v_str1}..string.char({v_bit_func}(tonumber({v_t_pair},16),{v_k_step})) end "
        f"end; "
        f"for {v_t_idx}=1,{obfuscate_core_math(len_l)},2 do "
        f"local {v_t_pair}=string.sub({v_h_l},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then {v_str2}={v_str2}..string.char({v_bit_func}(tonumber({v_t_pair},16),{v_k_step})) end "
        f"end; "
        f"local {v_env}=getfenv(); "
        f"local {v_func}={v_env}[{v_str1}] or {v_env}[{v_str2}]; "
        f"local {v_run}={v_func}({v_buffer}); "
        f"if {v_run} then {v_run}(...) end "
        f"end "
        f"end"
    )
    
    # Khai báo cấu trúc mảng ghi nhận thực thi động trong Lua game
    wrapped_payload = (
        f"local d_env_vars = {{}}; "
        f"local function register_env(idx, val) d_env_vars[idx] = val; return val; end; "
    )
    
    # Bọc cấu trúc theo dõi biến tự động cho toàn bộ khối rác và Key
    stealth_junk_list = []
    for idx, line in enumerate(junk_lines):
        fixed_line = line.replace("=", f"= register_env({idx+1}, ") + ")"
        stealth_junk_list.append(fixed_line)
        
    final_stealth_junk = ";".join(stealth_junk_list)
    
    # Lắp ghép hoàn chỉnh các khối payload phẳng
    total_payload = f"{wrapped_payload}{final_stealth_junk};{bit_and_interpreter_core}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    return f"-- This file was created by 8xms discord.gg/8mktK8HtT --\nreturn(function(...) {clean_payload} end)(...)"

# ----------------------------------------------------------------
# ĐỊNH NGHĨA LỆNH CHẠY BOT DISCORD
# ----------------------------------------------------------------
@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
        
    if not source_code or not source_code.strip():
        return await ctx.reply("Vui lòng cung cấp mã nguồn hợp lệ hoặc đính kèm file.")
        
    status_msg = await ctx.reply("Đang bảo mật mã nguồn bằng Ultimate Ghost Engine v15.0...")
    try:
        final_script = ironbrew_total_wrapped_v15_0(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done! Mã nguồn đã được bảo mật ngụy trang tàng hình hoàn tất.", file=discord.File(file_stream, filename="message.txt"))
        await status_msg.delete()
    except Exception as e:
        await status_msg.delete()
        await ctx.reply(f"Lỗi hệ thống trong quá trình mã hóa: {str(e)}")

# ----------------------------------------------------------------
# LUỒNG KHỞI CHẠY CHÍNH
# ----------------------------------------------------------------
if __name__ == "__main__":
    # Khởi động Web Server nền phụ trợ giữ kết nối bot
    threading.Thread(target=run_server, daemon=True).start()
    
    # Nạp Token từ biến môi trường hệ thống để khởi chạy bot
    bot.run(os.getenv("TOKEN"))

