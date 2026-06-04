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

def obfuscate_to_mixed_math(target):
    current_val = target
    ops_pool = []
    for _ in range(random.randint(2, 4)):
        op = random.choice(['+', '-'])
        rand_num = random.randint(100000, 1500000)
        if op == '+':
            current_val = current_val - rand_num
            display_style = random.choice(['normal', 'negative', 'hex'])
            if display_style == 'normal': ops_pool.append(f"+{rand_num}")
            elif display_style == 'negative': ops_pool.append(f"-(-{rand_num})")
            else: ops_pool.append(f"+{hex(rand_num)}")
        elif op == '-':
            current_val = current_val + rand_num
            display_style = random.choice(['normal', 'negative', 'hex'])
            if display_style == 'normal': ops_pool.append(f"-{rand_num}")
            elif display_style == 'negative': ops_pool.append(f"+(-{rand_num})")
            else: ops_pool.append(f"-{hex(rand_num)}")
    start_style = random.choice(['normal', 'hex'])
    expr = hex(current_val) if start_style == 'hex' else str(current_val)
    for action in reversed(ops_pool):
        expr = f"({expr}{action})"
    return f"({expr})"

class RealLuaVM:
    def __init__(self):
        self.bytecode = []
        self.constants = []
        self.reg_map = {}
        self.reg_count = 1
        self.has_return = False
        self.return_value_reg = None
        
    def compile_to_bytecode(self, source_code):
        bytecode = []
        constants = []
        lines = source_code.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('return'):
                self.has_return = True
                match = re.match(r'return\s+(.+)', line)
                if match:
                    expr = match.group(1)
                    if expr in self.reg_map:
                        self.return_value_reg = self.reg_map[expr] - 1
                    elif expr.isdigit():
                        const_idx = len(constants)
                        constants.append(expr)
                        temp_reg = self.reg_count
                        self.reg_count += 1
                        bytecode.extend([1, temp_reg-1, const_idx])
                        self.return_value_reg = temp_reg - 1
                continue
            
            if line.startswith('print'):
                match = re.match(r'print\([\'"](.+)[\'"]\)', line) or re.match(r'print\((\w+)\)', line)
                if match:
                    text = match.group(1)
                    if text in self.reg_map:
                        bytecode.extend([80, self.reg_map[text]-1])
                    else:
                        const_idx = len(constants)
                        constants.append(text)
                        bytecode.extend([1, 0, const_idx, 80, 0])
                    continue
            
            match = re.match(r'local\s+(\w+)\s*=\s*(.+)', line)
            if match:
                var_name = match.group(1)
                value = match.group(2)
                if value in self.reg_map:
                    bytecode.extend([4, self.reg_count-1, self.reg_map[value]-1])
                elif value.isdigit() or value.startswith('"'):
                    const_idx = len(constants)
                    constants.append(value.strip('"'))
                    bytecode.extend([1, self.reg_count-1, const_idx])
                else:
                    const_idx = len(constants)
                    constants.append(value)
                    bytecode.extend([1, self.reg_count-1, const_idx])
                self.reg_map[var_name] = self.reg_count
                self.reg_count += 1
                continue
            
            match = re.match(r'(\w+)\s*=\s*(\w+)\s*([\+\-\*\/])\s*(\w+)', line)
            if match:
                target = match.group(1)
                left = match.group(2)
                op = match.group(3)
                right = match.group(4)
                op_map = {'+': 16, '-': 17, '*': 18, '/': 19}
                opcode = op_map.get(op, 16)
                left_reg = self.reg_map.get(left, 1) - 1
                right_reg = self.reg_map.get(right, 1) - 1
                if target not in self.reg_map:
                    self.reg_map[target] = self.reg_count
                    self.reg_count += 1
                target_reg = self.reg_map[target] - 1
                bytecode.extend([opcode, target_reg, left_reg, right_reg])
                continue
        
        if self.has_return and self.return_value_reg is not None:
            bytecode.extend([81, self.return_value_reg])
        
        bytecode.append(255)
        return bytecode, constants

    def build_vm_interpreter(self, bytecode, constants):
        key = random.randint(100, 200)
        enc_c = []
        for c in constants:
            if isinstance(c, str):
                enc_c.append("{" + ",".join([str(ord(x)^key) for x in c]) + "}")
            else:
                enc_c.append(str(c))
        
        return f"""
local _B={{{','.join(map(str,bytecode))}}}
local _EncC={{{','.join(enc_c)}}}
local _K={key}
local _C={{}}for i=1,#_EncC do local s=""for j=1,#_EncC[i] do s=s..string.char(_EncC[i][j]~_K)end _C[i]=s end
local reg={{}}local pc=1 local _return=nil
while true do
    local op=_B[pc]if op==255 then break end
    if op==1 then reg[_B[pc+1]+1]=_C[_B[pc+2]+1] pc=pc+3
    elseif op==4 then reg[_B[pc+1]+1]=reg[_B[pc+2]+1] pc=pc+3
    elseif op==16 then reg[_B[pc+1]+1]=reg[_B[pc+2]+1]+reg[_B[pc+3]+1] pc=pc+4
    elseif op==17 then reg[_B[pc+1]+1]=reg[_B[pc+2]+1]-reg[_B[pc+3]+1] pc=pc+4
    elseif op==18 then reg[_B[pc+1]+1]=reg[_B[pc+2]+1]*reg[_B[pc+3]+1] pc=pc+4
    elseif op==19 then reg[_B[pc+1]+1]=reg[_B[pc+2]+1]/reg[_B[pc+3]+1] pc=pc+4
    elseif op==80 then print(reg[_B[pc+1]+1]) pc=pc+2
    elseif op==81 then _return=reg[_B[pc+1]+1] break
    else pc=pc+1 end
end
return _return
"""

def ironbrew_total_wrapped_v10_6_noload(source_code):
    vm = RealLuaVM()
    bytecode, constants = vm.compile_to_bytecode(source_code)
    vm_core = vm.build_vm_interpreter(bytecode, constants)
    
    init_key = random.randint(100, 250)
    encrypted_hex_list = []
    current_key = init_key
    for idx, byte in enumerate(vm_core.encode('utf-8')):
        cipher_byte = byte ^ current_key
        encrypted_hex_list.append(f"{cipher_byte:02X}")
        current_key = (current_key + idx + 7) % 256
    
    hex_payload = "".join(encrypted_hex_list)
    v_buf = random_var()
    v_run = random_var()
    
    return f"""
(function(...)
    local _s = "{hex_payload}"
    local _k = {init_key}
    local {v_buf} = ""
    for i=1, #_s, 2 do
        {v_buf} = {v_buf} .. string.char(tonumber(string.sub(_s, i, i+1), 16) ~ ((_k + (i/2) + 7) % 256))
    end
    {v_buf}
end)(...)
"""

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
        final_script = ironbrew_total_wrapped_v10_6_noload(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done.", file=discord.File(file_stream, filename="message.txt"))
        await status_msg.delete()
    except Exception as e:
        await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
