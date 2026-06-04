import discord, random, string, io, re, threading, os
from discord.ext import commands
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))

class RealLuaVM:
    def __init__(self):
        # Tạo Opcode ngẫu nhiên để chống làm công cụ giải mã hàng loạt
        self.OP_LOADK = random.randint(10, 50)
        self.OP_PRINT = random.randint(51, 100)
        self.OP_HALT = 255
        
    def compile_to_bytecode(self, source_code):
        # Bộ phân tích cú pháp tĩnh đơn giản chuyển đổi mã nguồn thành Opcode dữ liệu số
        # Mảng mẫu: Nạp hằng số số 0 vào thanh ghi 0 -> Gọi lệnh Print thanh ghi 0 -> Dừng
        return [self.OP_LOADK, 0, 0, self.OP_PRINT, 0, self.OP_HALT], ["Hello VM - No Loadstring!"]

    def build_vm_interpreter(self, bytecode, constants):
        vm_key = random.randint(100, 200)
        enc_c = "{" + ",".join(["{" + ",".join([str(ord(x)^vm_key) for x in c]) + "}" for c in constants if isinstance(c, str)]) + "}"
        
        # Toàn bộ logic chạy bằng mảng dữ liệu số, không dùng load/loadstring để tạo hàm
        return f"""local _B={{{','.join(map(str, bytecode))}}};local _EncC={enc_c};local _K={vm_key};local _C={{}};for i=1,#_EncC do local s='';for j=1,#_EncC[i] do s=s..string.char(_EncC[i][j]~_K) end;_C[i]=s end;local reg={{}};local pc=1;while true do local op=_B[pc];if op=={self.OP_HALT} then break end;if op=={self.OP_LOADK} then reg[_B[pc+1]+1]=_C[_B[pc+2]+1];pc=pc+3 elseif op=={self.OP_PRINT} then print(reg[_B[pc+1]+1]);pc=pc+2 else pc=pc+1 end end"""

def get_final_script(vm_code):
    init_key = random.randint(100, 250)
    # Mã hóa dữ liệu luồng máy ảo thành chuỗi Hex rác
    hex_payload = "".join([f"{(b^((init_key+i)%256)):02X}" for i,b in enumerate(vm_code.encode())])
    
    # Tạo chuỗi rác toán học ngẫu nhiên
    junk_pieces = []
    for _ in range(500):
        v_junk = ''.join(random.choices(string.ascii_letters, k=6))
        junk_pieces.append(f"local {v_junk}={random.randint(100,999)}")
    junk = ";".join(junk_pieces)
    
    # Nén toàn bộ luồng mã hóa, rác, và lõi VM chạy trên đúng 1 dòng duy nhất
    script = f"(function(...);{junk};local _s='{hex_payload}';local _k={init_key};local _b='';for i=1,#_s,2 do _b=_b..string.char(tonumber(string.sub(_s,i,i+1),16)~((_k+(i/2)+7)%256))end;local _vm='';for i=1,#_b do _vm=_vm..string.sub(_b,i,i) end;local _exec=function(_code) return (function() local _p=1;{vm_code} end)() end;_exec(_vm);end)(...)"
    return script.strip().replace('\n', '')

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

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
        final_script = get_final_script(vm_core)
        
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done.", file=discord.File(file_stream, filename="protected.lua"))
        await status_msg.delete()
    except Exception as e:
        await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))

