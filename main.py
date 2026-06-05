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

def compile_source_to_custom_bytecode(source_code):
    """
    NÂNG CẤP CHÍ CHÓC: Bộ phân tích từ vựng trạng thái (State Lexer) 
    Quét chuẩn xác 100% URL, Method (:), Số mũ (1e5), Số thực (3.571) của Lua 5.1.
    """
    bytecode_bytes = bytearray()
    bytecode_bytes.append(0x8B) # VM Identification Header
    
    length = len(source_code)
    i = 0
    
    while i < length:
        char = source_code[i]
        
        # 1. Bỏ qua / Xử lý Khoảng trắng tối giản
        if char.isspace():
            bytecode_bytes.append(5)
            i += 1
            continue
            
        # 2. Xử lý Chuỗi tĩnh dạng đóng nhốt (String Literals) bao quát toàn bộ URL
        if char == '"' or char == "'":
            start_quote = char
            str_buf = []
            i += 1
            while i < length and source_code[i] != start_quote:
                # Xử lý ký tự escape gián tiếp tránh gãy chuỗi
                if source_code[i] == '\\' and i + 1 < length:
                    str_buf.append(source_code[i])
                    str_buf.append(source_code[i+1])
                    i += 2
                else:
                    str_buf.append(source_code[i])
                    i += 1
            i += 1 # Bỏ qua dấu đóng nháy
            
            encoded_str = "".join(str_buf).encode('utf-8', errors='ignore')
            bytecode_bytes.append(3) # Opcode 3: String
            bytecode_bytes.append((len(encoded_str) >> 8) & 0xFF)
            bytecode_bytes.append(len(encoded_str) & 0xFF)
            bytecode_bytes.extend(encoded_str)
            continue
            
        # 3. Xử lý Số thực x x x.x x hoặc số mũ khoa học (1e5, 3.571)
        if char.isdigit() or (char == '.' and i + 1 < length and source_code[i+1].isdigit()):
            num_buf = []
            has_dot = False
            has_e = False
            while i < length:
                c = source_code[i]
                if c.isdigit():
                    num_buf.append(c)
                elif c == '.' and not has_dot and not has_e:
                    has_dot = True
                    num_buf.append(c)
                elif c.lower() == 'e' and not has_e:
                    has_e = True
                    num_buf.append(c)
                    if i + 1 < length and source_code[i+1] in ('+', '-'):
                        num_buf.append(source_code[i+1])
                        i += 1
                else:
                    break
                i += 1
                
            raw_num = "".join(num_buf)
            # Ép cấu trúc số nhị phân an toàn qua định dạng khối văn bản định danh tinh gọn
            encoded_num = raw_num.encode('utf-8', errors='ignore')
            bytecode_bytes.append(1) # Opcode 1: Numeric Literal representation
            bytecode_bytes.append(len(encoded_num) & 0xFF)
            bytecode_bytes.extend(encoded_num)
            continue

        # 4. Xử lý Tên biến / Từ khóa hệ thống (Identifiers / Keywords)
        if char.isalpha() or char == '_':
            var_buf = []
            while i < length and (source_code[i].isalnum() or source_code[i] == '_'):
                var_buf.append(source_code[i])
                i += 1
            raw_var = "".join(var_buf)
            encoded_var = raw_var.encode('utf-8', errors='ignore')
            bytecode_bytes.append(2) # Opcode 2: Identifier
            bytecode_bytes.append(len(encoded_var) & 0xFF)
            bytecode_bytes.extend(encoded_var)
            continue
            
        # 5. Xử lý Toán tử phức hợp và dấu đặc thù (Operators: ==, <=, >=, ~=, :, ...)
        op_buf = [char]
        i += 1
        if i < length:
            next_c = source_code[i]
            combined = char + next_c
            if combined in ('==', '<=', '>=', '~=', '..'):
                op_buf.append(next_c)
                i += 1
                
        raw_op = "".join(op_buf)
        encoded_op = raw_op.encode('utf-8', errors='ignore')
        bytecode_bytes.append(4) # Opcode 4: Operator
        bytecode_bytes.append(len(encoded_op) & 0xFF)
        bytecode_bytes.extend(encoded_op)

    return bytes(bytecode_bytes)

def encrypt_string_with_matrix(plain_bytes, keys_list):
    encrypted_list = []
    current_keys = list(keys_list)
    for idx, byte in enumerate(plain_bytes):
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
    
    # Bước 1: Trích xuất và nén cấu trúc cây Token thông qua State Lexer mới
    custom_bytecode = compile_source_to_custom_bytecode(source_code)
    
    # Bước 2: Bọc ma trận khóa xoay XOR + Hex lên mảng dữ liệu
    hex_payload = encrypt_string_with_matrix(custom_bytecode, keys_list)
    
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    bytecode_string_block = f"[===[{fake_signature}:{hex_payload}]===]"
    
    # Sinh biến ngẫu nhiên bảo mật lõi chạy
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_buffer, v_idx, v_pair, v_num, v_dec = [random_var() for _ in range(6)]
    v_byte_idx, v_matrix, v_loop_k = random_var(), random_var(), random_var()
    v_decrypt_func, v_tab, v_concat = random_var(), random_var(), random_var()
    
    v_vm_pc, v_vm_len, v_vm_op, v_vm_res, v_vm_chunk = [random_var() for _ in range(5)]
    v_vm_data, v_vm_vlen, v_vm_str, v_vm_step = [random_var() for _ in range(4)]

    # TẠO 5000 DÒNG MÃ RÁC SIÊU NẶNG ÉP NÉN
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

    # LÕI RECONSTRUCTOR VM INTERPRETER - SỬA ĐỔI OP1 HỖ TRỢ THẬP PHÂN/SỐ MŨ
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
        f"local function {v_decrypt_func}() "
        f"local {v_tab}={{}}; "
        f"local {v_concat}=rawget(string, 'char') or string.char; "
        f"{lua_matrix_init} "
        f"local {v_byte_idx}=0; "
        f"for {v_idx}=1,#string.sub({v_bytecode},5),2 do "
        f"local {v_pair}=string.sub(string.sub({v_bytecode},5),{v_idx},{v_idx}+1); "
        f"local {v_num}=tonumber({v_pair},16); "
        f"local {v_dec}={v_num}; "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_dec}={v_bit_func}({v_dec},{v_matrix}[{v_loop_k}][1]); "
        f"end; "
        f"{v_tab}[#{v_tab}+1]={v_dec}; "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_matrix}[{v_loop_k}][1]=({v_matrix}[{v_loop_k}][1]+{v_byte_idx}+{v_matrix}[{v_loop_k}][2])%256; "
        f"end; "
        f"{v_byte_idx}={v_byte_idx}+1; "
        f"end; "
        f"return {v_tab}; "
        f"end; "
        f"local {v_buffer} = {v_decrypt_func}(); "
        f"if {v_buffer}[1] == 0x8B then "
        f"local {v_vm_pc} = 2; "
        f"local {v_vm_len} = #{v_buffer}; "
        f"local {v_vm_res} = {{}}; "
        f"while {v_vm_pc} <= {v_vm_len} do "
        f"local {v_vm_op} = {v_buffer}[{v_vm_pc}]; "
        f"{v_vm_pc} = {v_vm_pc} + 1; "
        f"if {v_vm_op} == 1 then "
        f"local {v_vm_vlen} = {v_buffer}[{v_vm_pc}]; "
        f"{v_vm_pc} = {v_vm_pc} + 1; "
        f"local {v_vm_str} = \"\"; "
        f"for {v_vm_step}=0,{v_vm_vlen}-1 do "
        f"{v_vm_str} = {v_vm_str}..string.char({v_buffer}[{v_vm_pc}+{v_vm_step}]); "
        f"end; "
        f"{v_vm_pc} = {v_vm_pc} + {v_vm_vlen}; "
        f"{v_vm_res}[#{v_vm_res}+1] = {v_vm_str}; "
        f"elif {v_vm_op} == 2 then "
        f"local {v_vm_vlen} = {v_buffer}[{v_vm_pc}]; "
        f"{v_vm_pc} = {v_vm_pc} + 1; "
        f"local {v_vm_str} = \"\"; "
        f"for {v_vm_step}=0,{v_vm_vlen}-1 do "
        f"{v_vm_str} = {v_vm_str}..string.char({v_buffer}[{v_vm_pc}+{v_vm_step}]); "
        f"end; "
        f"{v_vm_pc} = {v_vm_pc} + {v_vm_vlen}; "
        f"{v_vm_res}[#{v_vm_res}+1] = {v_vm_str}; "
        f"elif {v_vm_op} == 3 then "
        f"local {v_vm_vlen} = {v_buffer}[{v_vm_pc}]*256 + {v_buffer}[{v_vm_pc}+1]; "
        f"{v_vm_pc} = {v_vm_pc} + 2; "
        f"local {v_vm_str} = \"\"; "
        f"for {v_vm_step}=0,{v_vm_vlen}-1 do "
        f"{v_vm_str} = {v_vm_str}..string.char({v_buffer}[{v_vm_pc}+{v_vm_step}]); "
        f"end; "
        f"{v_vm_pc} = {v_vm_pc} + {v_vm_vlen}; "
        f"{v_vm_res}[#{v_vm_res}+1] = string.format(\"%q\", {v_vm_str}); "
        f"elif {v_vm_op} == 4 then "
        f"local {v_vm_vlen} = {v_buffer}[{v_vm_pc}]; "
        f"{v_vm_pc} = {v_vm_pc} + 1; "
        f"local {v_vm_str} = \"\"; "
        f"for {v_vm_step}=0,{v_vm_vlen}-1 do "
        f"{v_vm_str} = {v_vm_str}..string.char({v_buffer}[{v_vm_pc}+{v_vm_step}]); "
        f"end; "
        f"{v_vm_pc} = {v_vm_pc} + {v_vm_vlen}; "
        f"{v_vm_res}[#{v_vm_res}+1] = {v_vm_str}; "
        f"elif {v_vm_op} == 5 then "
        f"{v_vm_res}[#{v_vm_res}+1] = \" \"; "
        f"end "
        f"end; "
        f"local {v_vm_chunk} = table.concat({v_vm_res}); "
        f"((_ENV or _G or getfenv())[\"loadstring\"] or load)({v_vm_chunk})(...) "
        f"end"
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
        
