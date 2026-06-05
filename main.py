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

def encrypt_string_with_matrix(plain_text, keys_list):
    encrypted_list = []
    current_keys = list(keys_list)
    for idx, byte in enumerate(plain_text.encode('utf-8', errors='ignore')):
        cipher_byte = byte
        for k in current_keys:
            cipher_byte = cipher_byte ^ k
        encrypted_list.append(f"{cipher_byte:02X}")
        for k_idx in range(len(current_keys)):
            current_keys[k_idx] = (current_keys[k_idx] + idx + (k_idx + 3)) % 256
    return "".join(encrypted_list)

def ironbrew_total_wrapped_v12_1(source_code):
    keys_count = random.randint(7, 12)
    keys_list = [random.randint(50, 255) for _ in range(keys_count)]
    
    hex_payload = encrypt_string_with_matrix(source_code, keys_list)
    hex_loadstring = encrypt_string_with_matrix("loadstring", keys_list)
    hex_load = encrypt_string_with_matrix("load", keys_list)
    
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    bytecode_string_block = f"[===[{fake_signature}:{hex_payload}]===]"
    h_ls_string_block = f"[===[{fake_signature}:{hex_loadstring}]===]"
    h_l_string_block = f"[===[{fake_signature}:{hex_load}]===]"
    
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_buffer, v_func, v_run = [random_var() for _ in range(4)]
    v_idx, v_pair, v_num, v_dec = [random_var() for _ in range(4)]
    v_loop_idx, v_env = random_var(), random_var()
    v_str1, v_str2 = random_var(), random_var()
    v_h_ls, v_h_l = random_var(), random_var()
    v_byte_idx = random_var()
    v_matrix, v_loop_k = random_var(), random_var()
    v_succ, v_match = random_var(), random_var()
    v_next, v_key_nxt, v_val_nxt = random_var(), random_var(), random_var()
    v_clean_str, v_decrypt_func = random_var(), random_var()
    v_tab, v_concat = random_var(), random_var()

    # GIỮ NGUYÊN 5000 DÒNG MÃ RÁC SIÊU NẶNG
    junk_pieces = []
    for _ in range(5000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
    half = len(junk_pieces) // 2
    junk_top, junk_bottom = ";".join(junk_pieces[:half]), ";".join(junk_pieces[half:])
    
    matrix_elements = []
    for k_idx, k_val in enumerate(keys_list):
        obf_val = obfuscate_core_math(k_val)
        obf_offset = obfuscate_core_math(k_idx + 3)
        matrix_elements.append(f"{{{obf_val},{obf_offset}}}")
        
    lua_matrix_init = f"local {v_matrix} = {{{','.join(matrix_elements)}}};"

    # Đưa toàn bộ cấu trúc về lại thành 1 chuỗi liên tục không xuống dòng
    bit_and_interpreter_core = (
        f"local function {v_bit_func}({v_i},{v_j}) "
        f"local {v_x}=0; "
        f"for {v_m}=0,7 do "
        f"local {v_w}=({v_i}/2^{v_m})%2; "
        f"local {v_res}=({v_j}/2^{v_m})%2; "
        f"if {v_w}-{v_w}%1~={v_res}-{v_res}%1 then {v_x}={v_x}+2^{v_m} end "
        f"end "
        f"return {v_x} "
        f"end; "
        f"local {v_bytecode}={bytecode_string_block}; "
        f"local {v_h_ls}={h_ls_string_block}; "
        f"local {v_h_l}={h_l_string_block}; "
        f"local function {v_decrypt_func}({v_clean_str}) "
        f"local {v_tab}={{}}; "
        f"local {v_concat}=rawget(string, 'char') or string.char; "
        f"{lua_matrix_init} "
        f"local {v_byte_idx}=0; "
        f"for {v_idx}=1,#{v_clean_str},2 do "
        f"local {v_pair}=string.sub({v_clean_str},{v_idx},{v_idx}+1); "
        f"local {v_num}=tonumber({v_pair},16); "
        f"local {v_dec}={v_num}; "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_dec}={v_bit_func}({v_dec},{v_matrix}[{v_loop_k}][1]); "
        f"end; "
        f"{v_tab}[#{v_tab}+1]={v_concat}({v_dec}); "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_matrix}[{v_loop_k}][1]=({v_matrix}[{v_loop_k}][1]+{v_byte_idx}+{v_matrix}[{v_loop_k}][2])%256; "
        f"end; "
        f"{v_byte_idx}={v_byte_idx}+1; "
        f"end; "
        f"return table.concat({v_tab}); "
        f"end; "
        f"local {v_buffer} = {v_decrypt_func}(string.sub({v_bytecode},5)); "
        f"local {v_str1} = {v_decrypt_func}(string.sub({v_h_ls},5)); "
        f"local {v_str2} = {v_decrypt_func}(string.sub({v_h_l},5)); "
        f"local {v_env} = _ENV or _G or getfenv(); "
        f"local {v_func} = rawget({v_env}, {v_str1}) or rawget({v_env}, {v_str2}); "
        f"if not {v_func} then "
        f"local {v_next} = rawget({v_env}, 'next'); "
        f"if {v_next} then "
        f"local {v_key_nxt}, {v_val_nxt} = {v_next}({v_env}, nil); "
        f"while {v_key_nxt} ~= nil do "
        f"if type({v_val_nxt}) == 'function' then "
        f"local {v_succ}, {v_match} = pcall(function() return {v_val_nxt} == rawget({v_env}, {v_str1}) or {v_val_nxt} == rawget({v_env}, {v_str2}) end); "
        f"if {v_succ} and {v_match} then {v_func} = {v_val_nxt}; break; end "
        f"end; "
        f"{v_key_nxt}, {v_val_nxt} = {v_next}({v_env}, {v_key_nxt}); "
        f"end "
        f"end "
        f"end; "
        f"local {v_run}={v_func}({v_buffer}); "
        f"if {v_run} then {v_run}(...) end"
    )
    
    total_payload = f"{junk_top};{bit_and_interpreter_core};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    return f"-- This file was created by 8xms discord.gg/8mktK8HtT --\nreturn(function(...) {clean_payload} end)(...)"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode("utf-8", errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
        
    if not source_code or not source_code.strip():
        return await ctx.reply("Please add file / code.")
        
    status_msg = await ctx.reply("<a:loading:1477881141678702603> Processing ")
    try:
        final_script = ironbrew_total_wrapped_v12_1(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done", file=discord.File(file_stream, filename="message.txt"))
        
        try:
            await status_msg.delete()
        except:
            pass
            
    except Exception as e:
        try:
            await status_msg.delete()
        except:
            pass
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
    
