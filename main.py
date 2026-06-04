import discord, random, string, io, re, threading, os
from discord.ext import commands

# --- [PHẦN 1: BỘ BIÊN DỊCH VM CORE] ---
class RealLuaVM:
    def __init__(self):
        # Bảng Opcode ngẫu nhiên mỗi lần build để chống dump
        self.OP_LOADK = random.randint(10, 50)
        self.OP_PRINT = random.randint(51, 100)
        self.OP_HALT = 255
        
    def compile_to_bytecode(self, source_code):
        # Đây là ví dụ compile đơn giản, bro có thể mở rộng logic tại đây
        # Output: Bytecode mảng số và bảng hằng số
        return [self.OP_LOADK, 0, 0, self.OP_PRINT, 0, self.OP_HALT], ["Hello VM"]

    def build_vm_interpreter(self, bytecode, constants):
        key = random.randint(100, 200)
        enc_c = "{" + ",".join(["{" + ",".join([str(ord(x)^key) for x in c]) + "}" for c in constants if isinstance(c, str)]) + "}"
        
        return f"""
        local _B = {{{','.join(map(str, bytecode))}}}
        local _EncC = {enc_c}
        local _K = {key}
        local _C = {{}}
        for i=1, #_EncC do 
            local s="" for j=1, #_EncC[i] do s=s..string.char(_EncC[i][j]~_K) end 
            _C[i]=s 
        end
        local reg={{}}
        local pc=1
        while true do
            local op = _B[pc]
            if op=={self.OP_HALT} then break end
            if op=={self.OP_LOADK} then reg[_B[pc+1]+1]=_C[_B[pc+2]+1] pc=pc+3
            elseif op=={self.OP_PRINT} then print(reg[_B[pc+1]+1]) pc=pc+2
            else pc=pc+1 end
        end
        """

# --- [PHẦN 2: WRAPPER (LỚP VỎ ĐÓNG GÓI)] ---
def get_final_script(vm_code):
    init_key = random.randint(100, 250)
    # Mã hóa VM Code thành Hex rác
    hex_payload = "".join([f"{(b^((init_key+i)%256)):02X}" for i,b in enumerate(vm_code.encode())])
    
    # Tạo rác ngẫu nhiên
    junk = "".join([f"local {random_var()}={random.randint(1,9999)};" for _ in range(500)])
    
    return f"""
    -- PROTECTED BY 8xMS VM REAL
    (function(...)
        {junk}
        local _s = "{hex_payload}"
        local _k = {init_key}
        local _buf = ""
        for i=1, #_s, 2 do
            _buf = _buf .. string.char(tonumber(string.sub(_s, i, i+1), 16) ~ ((_k + (i/2) + 7)%256))
        end
        -- Chạy thẳng vào lõi VM mà không cần loadstring
        local _f = assert(load(_buf))
        _f()
    end)(...)
    """

def random_var():
    return ''.join(random.choices(string.ascii_letters, k=6))

# --- [PHẦN 3: BOT DISCORD] ---
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.command()
async def obf(ctx, *, code):
    vm = RealLuaVM()
    b, c = vm.compile_to_bytecode(code)
    vm_core = vm.build_vm_interpreter(b, c)
    final = get_final_script(vm_core)
    
    file = io.BytesIO(final.encode())
    await ctx.send(file=discord.File(file, "protected.lua"))

bot.run("TOKEN")
