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
    """
    Trình biên dịch cấu trúc (Compiler):
    Bóc tách các lệnh cơ bản thành tập tin Opcode nhị phân.
    """
    opcodes = []
    patterns = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*\"([^\"]*)\"\s*\)', source_code)
    
    if not patterns:
        opcodes.append({
            "op": 99,  # OP_NATIVE_EXEC
            "data": source_code
        })
    else:
        for func_name, str_arg in patterns:
            opcodes.append({
                "op": 10,  # OP_GET_GLOBAL
                "data": func_name
            })
            opcodes.append({
                "op": 20,  # OP_LOAD_CONST
                "data": str_arg
            })
            opcodes.append({
                "op": 30,  # OP_CALL_FUNCTION
                "data": 1   
            })
    return opcodes

def build_vm_interpreter(opcodes):
    """
    Xây dựng cấu trúc Trình thông dịch lõi VM kết hợp toán tử che giấu nâng cao.
    """
    v_pc, v_instructions, v_stack, v_env = [random_var() for _ in range(4)]
    v_instr, v_op, v_data = [random_var() for _ in range(3)]
    
    lua_opcodes_list = []
    for inst in opcodes:
        op_val = obfuscate_core_math(inst["op"])
        if isinstance(inst["data"], str):
            hex_data = "".join([f"\\x{ord(c):02X}" for c in inst["data"]])
            data_val = f'"{hex_data}"'
        else:
            data_val = obfuscate_core_math(inst["data"])
        lua_opcodes_list.append(f"{{{op_val}, {data_val}}}")
        
    lua_instructions_table = f"local {v_instructions} = {{{','.join(lua_opcodes_list)}}}"
    
    # Lõi thực thi hoàn toàn không chứa 'elif', thay bằng 'elseif' chuẩn 100% Lua
    vm_core = (
        f"{lua_instructions_table}; "
        f"local {v_pc} = 1; "
        f"local {v_stack} = {{}}; "
        f"local {v_env} = (getgenv and getgenv()) or _G or _ENV; "
        f"while {v_pc} <= #{v_instructions} do "
        f"local {v_instr} = {v_instructions}[{v_pc}]; "
        f"local {v_op} = {v_instr}[1]; "
        f"local {v_data} = {v_instr}[2]; "
        f"if {v_op} == 10 then "
        f"{v_stack}[#{v_stack}+1] = {v_env}[{v_data}]; "
        f"elseif {v_op} == 20 then "
        f"{v_stack}[#{v_stack}+1] = {v_data}; "
        f"elseif {v_op} == 30 then "
        f"local arg = {v_stack}[#{v_stack}]; "
        f"local func = {v_stack}[#{v_stack}-1]; "
        f"{v_stack}[#{v_stack}] = nil; {v_stack}[#{v_stack}-1] = nil; "
        f"if func then func(arg) end; "
        f"elseif {v_op} == 99 then "
        f"local func_native = (loadstring or load); "
        f"if func_native then "
        f"local run = func_native({v_data}); "
        f"if run then run(...) end; "
        f"end; "
        f"end; "
        f"{v_pc} = {v_pc} + 1; "
        f"end;"
    )
    return vm_core

def ironbrew_total_wrapped_v13_vm(source_code):
    # Sinh 5000 dòng biến rác toán học cực nặng bọc ngoài rìa như bản v12.1
    junk_pieces = []
    for _ in range(5000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
    half = len(junk_pieces) // 2
    junk_top, junk_bottom = ";".join(junk_pieces[:half]), ";".join(junk_pieces[half:])
    
    # Biên dịch mã nguồn sang tập chỉ thị Opcode nhị phân
    compiled_opcodes = simple_lexer_to_opcodes(source_code)
    
    # Tạo lõi xử lý VM Interpreter
    bit_and_interpreter_core = build_vm_interpreter(compiled_opcodes)
    
    # Đóng gói toàn bộ rác và lõi VM thành một khối chuỗi duy nhất
    total_payload = f"{junk_top};{bit_and_interpreter_core};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    
    return f"-- This file was protected by 8xms Architecture VM v13.0 --\nreturn(function(...) {clean_payload} end)(...)"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    if not source_code or not source_code.strip():
        return await ctx.reply("Please add file / code.")
    status_msg = await ctx.reply("<a:loading:1477881141678702603> Transpiling architecture into VM structures... ")
    try:
        final_script = ironbrew_total_wrapped_v13_vm(source_code)
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
        
