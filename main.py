import discord
from discord.ext import commands
import random
import string
import io
import re
import threading
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live"

def run_server():
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

def random_var(length=6):
    first = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))
    return first + rest

def generate_advanced_junk(target):
    """
    Hàm sinh rác đa thể loại: Trộn lẫn toán học chuỗi #, số âm lồng nhau,
    hex liên chuỗi và toán tử logic điều kiện. Đảm bảo an toàn cú pháp 100%.
    """
    skid_quotes = [
        "go learn lua instead of skidding my script",
        "ez",
        "xhider on top",
        "Ctrl+C and Ctrl+V is not a personality trait",
        "stop pasting and start learning bro",
        "protected by hopes, dreams and your lack of skill",
        "reading this won't make you a better scripter",
        "touching grass is highly recommended right now",
        "nice try skid, but this won't deobfuscate itself",
        "error 404: skid brain cells not found",
        "imagine spending hours reversing a script"
    ]
    
    junk_mode = random.choice(['skid_string_math', 'negative_math', 'hex_ops_pool', 'logical_inline'])
    
    # Kiểu 1: Rác toán học chuỗi chửi skid (Bọc nháy đơn để tránh lỗi xung đột dòng)
    if junk_mode == 'skid_string_math':
        quote = random.choice(skid_quotes)
        q_len = len(quote)
        if random.choice([True, False]):
            return f"({target + q_len}-#'{quote}')"
        else:
            return f"({target - q_len}+#'{quote}')"
            
    # Kiểu 2: Toán học số âm lồng nhau đảo dấu liên tục
    elif junk_mode == 'negative_math':
        rand_num = random.randint(2000, 8000)
        return f"(-(-{target} - {rand_num}) + {rand_num})"
        
    # Kiểu 3: Chuỗi toán tử cộng trừ Hex ngẫu nhiên
    elif junk_mode == 'hex_ops_pool':
        current_val = target
        ops_pool = []
        for _ in range(random.randint(2, 3)):
            op = random.choice(['+', '-'])
            rand_num = random.randint(50000, 200000)
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
        
    # Kiểu 4: Biến đổi logic điều kiện inline
    else:
        rand_num = random.randint(100, 500)
        return f"({target} + ({rand_num} > 50 and 0 or 0))"

def ironbrew_total_wrapped_v10_6(source_code):
    # Khóa gốc ban đầu sinh ngẫu nhiên
    init_key = random.randint(100, 250)
    
    encrypted_hex_list = []
    current_key = init_key
    for idx, byte in enumerate(source_code.encode('utf-8')):
        cipher_byte = byte ^ current_key
        encrypted_hex_list.append(f"{cipher_byte:02X}")
        current_key = (current_key + idx + 7) % 256

    # GIỮ NGUYÊN: Khối Hex Payload chính xác nằm ở giữa cấu trúc tệp
    hex_payload = "".join(encrypted_hex_list)
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    bytecode_string_block = f"[=[{fake_signature}:{hex_payload}]=]"
    
    # Mã hóa chuỗi từ khóa hệ thống "loadstring" và "load"
    hex_loadstring = "".join([f"{ord(c) ^ init_key:02X}" for c in "loadstring"])
    hex_load = "".join([f"{ord(c) ^ init_key:02X}" for c in "load"])
    len_ls, len_l = len(hex_loadstring), len(hex_load)
    
    # Sinh tên biến ngẫu nhiên
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_buffer, v_func, v_run = [random_var() for _ in range(4)]
    v_idx, v_pair, v_num, v_dec = [random_var() for _ in range(4)]
    v_loop_idx, v_env = random_var(), random_var()
    v_str1, v_str2, v_t_idx, v_t_pair = [random_var() for _ in range(4)]
    v_h_ls, v_h_l = random_var(), random_var()
    v_rolling_key, v_byte_idx = random_var(), random_var()

    # Sinh 2500 dòng biến rác đa dạng thể loại ở hai đầu tệp
    junk_pieces = []
    for _ in range(2500):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={generate_advanced_junk(rand_target)}")
    half = len(junk_pieces) // 2
    junk_top, junk_bottom = ";".join(junk_pieces[:half]), ";".join(junk_pieces[half:])
    
    # Lõi VM áp dụng bộ sinh rác hỗn hợp và mã hóa (obf) hoàn toàn init_key bên trong
    bit_and_interpreter_core = (
        f"local function {v_bit_func}({v_i},{v_j}) "
        f"local {v_x}=0; "
        f"for {v_m}=0,7 do "
        f"local {v_w}=({v_i}/{generate_advanced_junk(2)}^{v_m})%2; "
        f"local {v_res}=({v_j}/{generate_advanced_junk(2)}^{v_m})%2; "
        f"if {v_w}-{v_w}%1~={v_res}-{v_res}%1 then {v_x}={v_x}+{generate_advanced_junk(2)}^{v_m} end "
        f"end "
        f"return {v_x} "
        f"end; "
        f"local {v_bytecode}={bytecode_string_block}; "
        f"local {v_h_ls}=\"{hex_loadstring}\"; "
        f"local {v_h_l}=\"{hex_load}\"; "
        f"local {v_buffer}=\"\"; "
        f"for {v_loop_idx}={generate_advanced_junk(1)},{generate_advanced_junk(2)} do "
        f"if {v_loop_idx}=={generate_advanced_junk(1)} then "
        f"local h_clean=string.sub({v_bytecode},5); "
        f"local {v_rolling_key}={generate_advanced_junk(init_key)}; "  # Mã hóa init_key ở đây
        f"local {v_byte_idx}=0; "
        f"for {v_idx}=1,#h_clean,2 do "
        f"local {v_pair}=string.sub(h_clean,{v_idx},{v_idx}+1); "
        f"local {v_num}=tonumber({v_pair},16); "
        f"local {v_dec}={v_bit_func}({v_num},{v_rolling_key}); "
        f"{v_buffer}={v_buffer}..string.char({v_dec}); "
        f"{v_rolling_key}=({v_rolling_key}+{v_byte_idx}+{generate_advanced_junk(7)})%256; "
        f"{v_byte_idx}={v_byte_idx}+1; "
        f"end "
        f"elseif {v_loop_idx}=={generate_advanced_junk(2)} then "
        f"local {v_str1}, {v_str2} = \"\", \"\"; "
        f"for {v_t_idx}=1,{generate_advanced_junk(len_ls)},2 do "
        f"local {v_t_pair}=string.sub({v_h_ls},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then {v_str1}={v_str1}..string.char({v_bit_func}(tonumber({v_t_pair},16),{generate_advanced_junk(init_key)})) end " # Mã hóa init_key
        f"end; "
        f"for {v_t_idx}=1,{generate_advanced_junk(len_l)},2 do "
        f"local {v_t_pair}=string.sub({v_h_l},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then {v_str2}={v_str2}..string.char({v_bit_func}(tonumber({v_t_pair},16),{generate_advanced_junk(init_key)})) end " # Mã hóa init_key
        f"end; "
        f"local {v_env}=getfenv(); "
        f"local {v_func}={v_env}[{v_str1}] or {v_env}[{v_str2}]; "
        f"local {v_run}={v_func}({v_buffer}); "
        f"if {v_run} then {v_run}(...) end "
        f"end "
        f"end"
    )
    
    total_payload = f"{junk_top};{bit_and_interpreter_core};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    return f"-- This file was created by 8xms discord.gg/8mktK8HtT --\nreturn(function(...) {clean_payload} end)(...)"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    if not source_code or not source_code.strip():
        return await ctx.reply("Please provide a valid file or code.")
    status_msg = await ctx.reply("Processing...")
    try:
        final_script = ironbrew_total_wrapped_v10_6(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done.", file=discord.File(file_stream, filename="message.txt"))
        await status_msg.delete()
    except Exception as e:
        await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))

