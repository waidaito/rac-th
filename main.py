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

def generate_vm_math(target):
    """Sinh biểu thức toán học ngẫu nhiên để che giấu hằng số trong lõi VM"""
    current_val = target
    ops_pool = []
    for _ in range(random.randint(1, 2)):
        op = random.choice(['+', '-'])
        rand_num = random.randint(1000, 5000)
        if op == '+':
            current_val -= rand_num
            ops_pool.append(f"+{rand_num}")
        else:
            current_val += rand_num
            ops_pool.append(f"-{rand_num}")
    expr = str(current_val)
    for action in reversed(ops_pool):
        expr = f"({expr}{action})"
    return f"({expr})"

def simple_lexer_to_opcodes(source_code):
    """
    Trình biên dịch cấu trúc thô (Basic Compiler):
    Chuyển đổi một số câu lệnh Lua cơ bản thành chuỗi cấu trúc Opcode nhị phân giả lập.
    Cơ chế này minh họa cách chuyển câu lệnh chuỗi thành chỉ thị số của VM.
    """
    opcodes = []
    # Phân tích các hàm in hoặc gọi hàm cơ bản dạng global_name("string_literal")
    patterns = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*\"([^\"]*)\"\s*\)', source_code)
    
    if not patterns:
        # Nếu mã nguồn phức tạp nằm ngoài tầm xử lý của Lexer cơ bản này, 
        # cấu trúc sẽ mặc định đóng gói toàn bộ đoạn mã để thông dịch qua một hàm Opcode đặc biệt
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
                "data": 1   # Số lượng đối số
            })
    return opcodes

def build_vm_interpreter(opcodes):
    """
    Xây dựng trình thông dịch (Interpreter) bằng Lua.
    Bao gồm cấu trúc mảng Opcodes và vòng lặp thực thi (Execution Loop).
    """
    v_pc, v_instructions, v_stack, v_env = [random_var() for _ in range(4)]
    v_instr, v_op, v_data = [random_var() for _ in range(3)]
    
    # Mã hóa dữ liệu Opcode thành dạng danh sách có cấu trúc ngẫu nhiên trong Table
    lua_opcodes_list = []
    for inst in opcodes:
        op_val = generate_vm_math(inst["op"])
        if isinstance(inst["data"], str):
            # Mã hóa Hex chuỗi ký tự trong hằng số Opcode để chống quét chuỗi tĩnh
            hex_data = "".join([f"\\x{ord(c):02X}" for c in inst["data"]])
            data_val = f'"{hex_data}"'
        else:
            data_val = generate_vm_math(inst["data"])
        lua_opcodes_list.append(f"{{{op_val}, {data_val}}}")
        
    lua_instructions_table = f"local {v_instructions} = {{{','.join(lua_opcodes_list)}}}"
    
    # Xây dựng vòng lặp lệnh (Dispatcher Loop) xử lý Opcode nội bộ
    vm_core = (
        f"{lua_instructions_table}; "
        f"local {v_pc} = 1; "
        f"local {v_stack} = {{}}; "
        f"local {v_env} = (getgenv and getgenv()) or _G or _ENV; "
        f"while {v_pc} <= #{v_instructions} do "
        f"local {v_instr} = {v_instructions}[{v_pc}]; "
        f"local {v_op} = {v_instr}[1]; "
        f"local {v_data} = {v_instr}[2]; "
        
        # Nhánh rẽ Opcode (Instruction Branching)
        f"if {v_op} == 10 then "  # OP_GET_GLOBAL
        f"{v_stack}[#{v_stack}+1] = {v_env}[{v_data}]; "
        f"elif {v_op} == 20 then " # OP_LOAD_CONST
        f"{v_stack}[#{v_stack}+1] = {v_data}; "
        f"elif {v_op} == 30 then " # OP_CALL_FUNCTION
        f"local arg = {v_stack}[#{v_stack}]; "
        f"local func = {v_stack}[#{v_stack}-1]; "
        f"{v_stack}[#{v_stack}] = nil; {v_stack}[#{v_stack}] = nil; " # Clear stack
        f"if func then func(arg) end; "
        f"elif {v_op} == 99 then " # OP_NATIVE_EXEC (Khối cô lập bảo mật)
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

def ironbrew_vm_v13_0(source_code):
    # Phân tích cú pháp và trích xuất danh sách Opcode nhị phân từ mã nguồn
    compiled_opcodes = simple_lexer_to_opcodes(source_code)
    
    # Sinh lõi trình thông dịch Virtual Machine tùy biến cho tập Opcode vừa tạo
    vm_interpreter_payload = build_vm_interpreter(compiled_opcodes)
    
    # Đóng gói và loại bỏ khoảng trắng dư thừa nhằm tối ưu hóa kích thước tệp xuất ra
    clean_payload = " ".join(vm_interpreter_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    return f"-- Protected by 8xms Virtual Machine Architecture v13.0 --\nreturn (function(...) {clean_payload} end)(...)"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    if not source_code or not source_code.strip():
        return await ctx.reply("Please attach a valid file or code block.")
    status_msg = await ctx.reply("<a:loading:1477881141678702603> Transpiling architecture into VM structures... ")
    try:
        final_script = ironbrew_vm_v13_0(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done", file=discord.File(file_stream, filename="vm_obfuscated.txt"))
        await status_msg.delete()
    except Exception as e:
        try:
            await status_msg.delete()
        except:
            pass
        await ctx.reply(f"Error during compilation: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
    
