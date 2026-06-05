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

def simple_lexer_to_opcodes(source_code):
    opcodes = []
    patterns = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*\"([^\"]*)\"\s*\)', source_code)
    if not patterns:
        opcodes.append({"op": 99, "data": source_code})
    else:
        for func_name, str_arg in patterns:
            opcodes.append({"op": 10, "data": func_name})
            opcodes.append({"op": 20, "data": str_arg})
            opcodes.append({"op": 30, "data": 1})
    return opcodes

def ironbrew_ultimate_vm_v14_3(source_code):
    # 1. Sinh 5000 dòng rác toán học bọc ngoài rìa
    junk_pieces = []
    for _ in range(5000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
    half = len(junk_pieces) // 2
    junk_top, junk_bottom = ";".join(junk_pieces[:half]), ";".join(junk_pieces[half:])

    # 2. Biên dịch code sang dạng cấu trúc Opcode
    compiled_opcodes = simple_lexer_to_opcodes(source_code)
    
    # 3. Tạo hệ thống 7-12 tầng khóa XOR xoay vòng ngẫu nhiên
    keys_count = random.randint(7, 12)
    keys_list = [random.randint(50, 255) for _ in range(keys_count)]
    
    # CƠ CHẾ ĐÓNG GÓI MỚI: Định dạng nhị phân độ dài cố định (Không sợ lỗi dấu cách/ký tự dị)
    raw_bytes_stream = bytearray()
    for inst in compiled_opcodes:
        op_str = str(inst['op']).encode('utf-8')
        data_bytes = inst['data'].encode('utf-8') if isinstance(inst['data'], str) else str(inst['data']).encode('utf-8')
        
        # Cấu trúc: [Độ dài OP (1 byte)] + [Mã OP] + [Độ dài DATA (4 bytes)] + [Mã DATA]
        raw_bytes_stream.append(len(op_str))
        raw_bytes_stream.extend(op_str)
        
        len_data = len(data_bytes)
        raw_bytes_stream.extend([
            (len_data >> 24) & 0xFF,
            (len_data >> 16) & 0xFF,
            (len_data >> 8) & 0xFF,
            len_data & 0xFF
        ])
        raw_bytes_stream.extend(data_bytes)

    # Thực hiện XOR cuộn đa tầng trên chuỗi byte stream sạch
    encrypted_hex_list = []
    current_keys = list(keys_list)
    for idx, byte in enumerate(raw_bytes_stream):
        cipher_byte = byte
        for k in current_keys:
            cipher_byte = cipher_byte ^ k
        encrypted_hex_list.append(f"{cipher_byte:02X}")
        for k_idx in range(len(current_keys)):
            current_keys[k_idx] = (current_keys[k_idx] + idx + (k_idx + 3)) % 256

    hex_bytecode_stream = "".join(encrypted_hex_list)
    bytecode_string_block = f"[=[XORVM:{hex_bytecode_stream}]=]"

    # Tạo bảng ma trận khóa ẩn danh
    matrix_elements = []
    for k_idx, k_val in enumerate(keys_list):
        matrix_elements.append(f"{{{obfuscate_core_math(k_val)},{obfuscate_core_math(k_idx + 3)}}}")
    matrix_elements.reverse()

    # Tên biến ngẫu nhiên bảo mật cao cho VM
    v_bit_func, v_i, v_j, v_x, v_m, v_w, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_matrix, v_byte_idx, v_idx, v_pair, v_num, v_dec, v_loop_k = [random_var() for _ in range(8)]
    v_buffer, v_pc, v_instructions, v_stack, v_env, v_instr, v_op, v_data = [random_var() for _ in range(8)]
    v_ptr, v_op_len, v_dat_len, v_p_op, v_p_data, v_c_idx, v_hex_out = [random_var() for _ in range(7)]

    # 4. Lõi Trình thông dịch Máy ảo + Vòng giải mã dựa trên con trỏ Pointer di động
    bit_and_interpreter_core = (
        f"local function {v_bit_func}({v_i},{v_j}) "
        f"local {v_x}=0; for {v_m}=0,7 do "
        f"local {v_w}=({v_i}/2^{v_m})%2; local {v_res}=({v_j}/2^{v_m})%2; "
        f"if {v_w}-{v_w}%1~={v_res}-{v_res}%1 then {v_x}={v_x}+2^{v_m} end "
        f"end return {v_x} "
        f"end; "
        f"local {v_bytecode} = {bytecode_string_block}; "
        f"local h_clean = string.sub({v_bytecode}, 7); "
        f"local {v_matrix} = {{{','.join(matrix_elements)}}}; "
        f"local {v_byte_idx} = 0; "
        f"local {v_buffer} = {{}}; "
        f"for {v_idx}=1,#h_clean,2 do "
        f"local {v_pair} = string.sub(h_clean,{v_idx},{v_idx}+1); "
        f"local {v_num} = tonumber({v_pair},16); "
        f"local {v_dec} = {v_num}; "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_dec}={v_bit_func}({v_dec},{v_matrix}[{v_loop_k}][1]); "
        f"end; "
        f"{v_buffer}[#{v_buffer}+1] = string.char({v_dec}); "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_matrix}[{v_loop_k}][1]=({v_matrix}[{v_loop_k}][1]+{v_byte_idx}+{v_matrix}[{v_loop_k}][2])%256; "
        f"end; "
        f"{v_byte_idx} = {v_byte_idx} + 1; "
        f"end; "
        f"local unpacked_str = table.concat({v_buffer}); "
        # Sử dụng kỹ thuật Pointer đọc mảng nhị phân để dựng danh sách Opcode chuẩn xác tuyệt đối
        f"local {v_instructions} = {{}}; "
        f"local {v_ptr} = 1; "
        f"while {v_ptr} <= #unpacked_str do "
        f"local {v_op_len} = string.byte(unpacked_str, {v_ptr}); "
        f"{v_ptr} = {v_ptr} + 1; "
        f"local {v_p_op} = string.sub(unpacked_str, {v_ptr}, {v_ptr} + {v_op_len} - 1); "
        f"{v_ptr} = {v_ptr} + {v_op_len}; "
        f"local b1, b2, b3, b4 = string.byte(unpacked_str, {v_ptr}, {v_ptr} + 3); "
        f"local {v_dat_len} = b1*16777216 + b2*65536 + b3*256 + b4; "
        f"{v_ptr} = {v_ptr} + 4; "
        f"local {v_p_data} = string.sub(unpacked_str, {v_ptr}, {v_ptr} + {v_dat_len} - 1); "
        f"{v_ptr} = {v_ptr} + {v_dat_len}; "
        f"local n_op = tonumber({v_p_op}); "
        f"if n_op ~= 99 then "
        f"local {v_hex_out} = \"\"; "
        f"for {v_c_idx}=1,#{v_p_data} do "
        f"{v_hex_out} = {v_hex_out} .. string.format(\"\\\\x%02X\", string.byte({v_p_data}, {v_c_idx})); "
        f"end; "
        f"{v_p_data} = {v_hex_out}; "
        f"end; "
        f"{v_instructions}[#{v_instructions}+1] = {{n_op, {v_p_data}}}; "
        f"end; "
        # Vòng lặp Dispatcher Máy ảo thực thi ngầm chống Hook
        f"local {v_pc} = 1; local {v_stack} = {{}}; "
        f"local {v_env} = (getgenv and getgenv()) or _G or _ENV; "
        f"while {v_pc} <= #{v_instructions} do "
        f"local {v_instr} = {v_instructions}[{v_pc}]; "
        f"local {v_op} = {v_instr}[1]; local {v_data} = {v_instr}[2]; "
        f"if {v_op} == 10 then {v_stack}[#{v_stack}+1] = {v_env}[{v_data}]; "
        f"elseif {v_op} == 20 then {v_stack}[#{v_stack}+1] = {v_data}; "
        f"elseif {v_op} == 30 then "
        f"local arg = {v_stack}[#{v_stack}]; local func = {v_stack}[#{v_stack}-1]; "
        f"{v_stack}[#{v_stack}] = nil; {v_stack}[#{v_stack}-1] = nil; "
        f"if func then func(arg) end; "
        f"elseif {v_op} == 99 then "
        f"local func_native = (loadstring or load); "
        f"if func_native then local run = func_native({v_data}); if run then run(...) end end; "
        f"end; "
        f"{v_pc} = {v_pc} + 1; "
        f"end;"
    )

    total_payload = f"{junk_top};{bit_and_interpreter_core};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    return f"-- Protected by 8xms Ultimate XOR-VM Architecture v14.3 --\nreturn(function(...) {clean_payload} end)(...)"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    if not source_code or not source_code.strip():
        return await ctx.reply("Please add file / code.")
    status_msg = await ctx.reply("<a:loading:1477881141678702603> Transpiling into Pointer-based XOR-VM structures... ")
    try:
        final_script = ironbrew_ultimate_vm_v14_3(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done", file=discord.File(file_stream, filename="message.txt"))
        await status_msg.delete()
    except Exception as e:
        try:
            await status_msg.delete()
        except:
            pass
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
        
