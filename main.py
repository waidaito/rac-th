import discord, random, string, io, re, threading, os
from discord.ext import commands
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))

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
        self.OP_LOADK = random.randint(10, 50)
        self.OP_PRINT = random.randint(51, 100)
        self.OP_HALT = 255
        
    def compile_to_bytecode(self, source_code):
        return [self.OP_LOADK, 0, 0, self.OP_PRINT, 0, self.OP_HALT], ["Hello VM - Zero Loadstring!"]

    def build_vm_interpreter(self, bytecode, constants):
        vm_key = random.randint(100, 200)
        enc_c = "{" + ",".join(["{" + ",".join([str(ord(x)^vm_key) for x in c]) + "}" for c in constants if isinstance(c, str)]) + "}"
        
        v_b, v_enc, v_k, v_c, v_s, v_reg, v_pc, v_op = [random_var() for _ in range(8)]
        
        return (
            f"local {v_b}={{{','.join(map(str, bytecode))}}};"
            f"local {v_enc}={enc_c};"
            f"local {v_k}={vm_key};"
            f"local {v_c}={{}};"
            f"for i=1,#{v_enc} do "
                f"local {v_s}=[==[]==];"
                f"for j=1,#{v_enc}[i] do {v_s}={v_s}..string.char({v_enc}[i][j]~{v_k}) end;"
                f"{v_c}[i]={v_s} "
            f"end;"
            f"local {v_reg}={{}};"
            f"local {v_pc}=1;"
            f"while true do "
                f"local {v_op}={v_b}[{v_pc}];"
                f"if {v_op}=={self.OP_HALT} then break end;"
                f"if {v_op}=={self.OP_LOADK} then "
                    f"{v_reg}[{v_b}[{v_pc}+1]+1]={v_c}[{v_b}[{v_pc}+2]+1];"
                    f"{v_pc}={v_pc}+3 "
                f"elseif {v_op}=={self.OP_PRINT} then "
                    f"print({v_reg}[{v_b}[{v_pc}+1]+1]);"
                    f"{v_pc}={v_pc}+2 "
                f"else "
                    f"{v_pc}={v_pc}+1 "
                f"end "
            f"end"
        )

def ironbrew_total_wrapped_v10_6(vm_code):
    init_key = random.randint(100, 250)
    hex_payload = "".join([f"{(b^((init_key+i)%256)):02X}" for i, b in enumerate(vm_code.encode('utf-8'))])
    
    junk_pieces = []
    for _ in range(1000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={obfuscate_to_mixed_math(rand_target)}")
    junk = ";".join(junk_pieces)
    
    v_s, v_k, v_b, v_exec = [random_var() for _ in range(4)]
    
    script = (
        f"return(function(...) "
            f"{junk};"
            f"local {v_s}=[=[{hex_payload}]=];"
            f"local {v_k}={init_key};"
            f"local {v_b}=[==[]==];"
            f"for i=1,#{v_s},2 do "
                f"{v_b}={v_b}..string.char(tonumber(string.sub({v_s},i,i+1),16)~(({v_k}+(i/2)+7)%256))"
            f"end;"
            f"local {v_exec}=assert(load({v_b}));"
            f"{v_exec}(...);"
        f"end)(...)"
    )
    return script.strip().replace('\n', '')

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
        vm = RealLuaVM()
        bytecode, constants = vm.compile_to_bytecode(source_code)
        vm_core = vm.build_vm_interpreter(bytecode, constants)
        final_script = ironbrew_total_wrapped_v10_6(vm_core)
        
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done.", file=discord.File(file_stream, filename="protected.lua"))
        await status_msg.delete()
    except Exception as e:
        await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
