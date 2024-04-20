import os
import argparse

class Config(object):
    def __init__(self, iodir):
        self.filepath = os.path.abspath(os.path.join(iodir, "Config.txt"))
        self.parameters = {} # dictionary of parameter name: value as strings.

        try:
            with open(self.filepath, 'r') as conf:
                self.parameters = {line.split('=')[0].strip(): int(line.split('=')[1].split('#')[0].strip()) for line in conf.readlines() if not (line.startswith('#') or line.strip() == '')}
            print("Config - Parameters loaded from file:", self.filepath)
            print("Config parameters:", self.parameters)
        except:
            print("Config - ERROR: Couldn't open file in path:", self.filepath)
            raise

class IMEM(object):
    def __init__(self, iodir):
        self.size = pow(2, 16) # Can hold a maximum of 2^16 instructions.
        self.filepath = os.path.abspath(os.path.join(iodir, "CodeOP.asm"))
        self.instructions = []

        try:
            with open(self.filepath, 'r') as insf:
                self.instructions = [ins.split('#')[0].strip() for ins in insf.readlines() if not (ins.startswith('#') or ins.strip() == '')]
            print("IMEM - Instructions loaded from file:", self.filepath)
            # print("IMEM - Instructions:", self.instructions)
        except:
            print("IMEM - ERROR: Couldn't open file in path:", self.filepath)
            raise

    def Read(self, idx): # Use this to read from IMEM.
        if idx < self.size:
            return self.instructions[idx].split()
        else:
            print("IMEM - ERROR: Invalid memory access at index: ", idx, " with memory size: ", self.size)

class DMEM(object):
    # Word addressible - each address contains 32 bits.
    def __init__(self, name, iodir, addressLen):
        self.name = name
        self.size = pow(2, addressLen)
        self.min_value  = -pow(2, 31)
        self.max_value  = pow(2, 31) - 1
        self.ipfilepath = os.path.abspath(os.path.join(iodir, name + ".txt"))
        self.opfilepath = os.path.abspath(os.path.join(iodir, name + "OP.txt"))
        self.data = []

        try:
            with open(self.ipfilepath, 'r') as ipf:
                self.data = [int(line.strip()) for line in ipf.readlines()]
            print(self.name, "- Data loaded from file:", self.ipfilepath)
            # print(self.name, "- Data:", self.data)
            self.data.extend([0x0 for i in range(self.size - len(self.data))])
        except:
            print(self.name, "- ERROR: Couldn't open input file in path:", self.ipfilepath)
            raise

    def Read(self, idx): # Use this to read from DMEM.
        pass # Replace this line with your code here.

    def Write(self, idx, val): # Use this to write into DMEM.
        pass # Replace this line with your code here.

    def dump(self):
        try:
            with open(self.opfilepath, 'w') as opf:
                lines = [str(data) + '\n' for data in self.data]
                opf.writelines(lines)
            print(self.name, "- Dumped data into output file in path:", self.opfilepath)
        except:
            print(self.name, "- ERROR: Couldn't open output file in path:", self.opfilepath)
            raise

class RegisterFile(object):
    def __init__(self, name, count, length = 1, size = 32):
        self.name       = name
        self.reg_count  = count
        self.vec_length = length # Number of 32 bit words in a register.
        self.reg_bits   = size
        self.min_value  = -pow(2, self.reg_bits-1)
        self.max_value  = pow(2, self.reg_bits-1) - 1
        self.registers  = [[0x0 for e in range(self.vec_length)] for r in range(self.reg_count)] # list of lists of integers

    def Read(self, idx):
        pass # Replace this line with your code.

    def Write(self, idx, val):
        pass # Replace this line with your code.

    def dump(self, iodir):
        opfilepath = os.path.abspath(os.path.join(iodir, self.name + ".txt"))
        try:
            with open(opfilepath, 'w') as opf:
                row_format = "{:<13}"*self.vec_length
                lines = [row_format.format(*[str(i) for i in range(self.vec_length)]) + "\n", '-'*(self.vec_length*13) + "\n"]
                lines += [row_format.format(*[str(val) for val in data]) + "\n" for data in self.registers]
                opf.writelines(lines)
            print(self.name, "- Dumped data into output file in path:", opfilepath)
        except:
            print(self.name, "- ERROR: Couldn't open output file in path:", opfilepath)
            raise

class instruction():
    def __init__(self,instr_name,instr_queue,s_regs,v_regs,smem_ad,vmem_ad,instr_cycleCount):
        # Each instruction after decoding will contain the following metadata
        self.instr_name = instr_name
        self.instr_queue = instr_queue              # number indicating which queue to enter
                                                    # 0: VectorCompute Queue; 1: VectorData Queue; 2: ScalarOps Queue
        self.s_regs = s_regs                        # list of all scalar registers used
        self.v_regs = v_regs                        # likewise for vector registers
        self.smem_ad = smem_ad                      # list of all scalar memory addresses used
        self.vmem_ad = vmem_ad                      # likewise for vector memory addresses
        self.instr_cycleCount = instr_cycleCount    # Number of cycles instruction takes
    
    def __init__(self):
        # Constructor with default values
        self.instr_name = ""
        self.instr_queue = -1
        self.s_regs = []
        self.v_regs = []
        self.smem_ad = []
        self.vmem_ad = []
        self.instr_cycleCount = 0
class Core():
    def __init__(self, imem, sdmem, vdmem, config):
        self.IMEM = imem
        self.SDMEM = sdmem
        self.VDMEM = vdmem
        self.config = config
        self.PC = 0
        self.CycleCount = 0

        self.RFs = {"SRF": RegisterFile("SRF", 8),      # 8 registers of 32 bit integers
                    "VRF": RegisterFile("VRF", 8, 64),  # 8 registers of 64 elements; each of 32 bits
                    "VMR": RegisterFile("VMR", 1, 64),
                    "VLR": RegisterFile("VLR", 1)
                }  
        
        self.busyBoard = {"scalar": [0]*8,"vector": [0]*8}
        print(self.config.parameters)
        self.queues = {"vectorCompute":[None]*self.config.parameters["computeQueueDepth"],
                       "vectorData":[None]*self.config.parameters["dataQueueDepth"],
                       "scalarOps":[None]*self.config.parameters["computeQueueDepth"],
                       }
        
        self.fetched_instr_current = []
        self.fetched_instr_prev = []
        
        self.decoded_instr_current = instruction()
        self.decoded_instr_prev = instruction()
        
        # Your code here.

        # Execute functions here

        # Decode functions here 
    
    def decode(self,instr_list):
        # convert instuction list to instruction format
        # creating instruction object and loading default values
        ins = instruction()
        ins.instr_name = instr_list[0]

        if(ins.instr_name in ["ADDVV","SUBVV","MULVV","DIVVV","UNPACKLO","UNPACKHI","PACKLO","PACKHI"]):
            ins.instr_queue = 0
            ins.v_regs = [int(instr_list[1][2:]),int(instr_list[2][2:]),int(instr_list[3][2:])]
            print(ins.instr_name,ins.v_regs)

        elif(ins.instr_name in ["ADDVS","SUBVS","MULVS","DIVVS"]):
            ins.instr_queue = 0
            ins.v_regs = [int(instr_list[1][2:]),int(instr_list[2][2:])]
            ins.s_regs = [int(instr_list[3][2:])]
        
        elif(ins.instr_name in ["POP","MTCL","MFCL"]):
            ins.instr_queue = 2
            ins.s_regs = [int(instr_list[1][2:])]

        elif(ins.instr_name == "B"):
            # Dunno what to in branch
            # It goes to the scalar queue??
            continue

        else: 
            print("UNKNOWN INSTRUCTION")
            return -1
        
        return instruction
    
    def dispatch(self,instruction):
        # checks busy board and sends instructions to the queues if free
        return
       
        
    def run(self):
        self.PC = 0
        self.CycleCount = 0
        while(True):
            # instruction fetch phase
            self.fetched_instr_prev = self.fetched_instr_current
            self.fetched_instr_current = self.IMEM.Read(self.PC)

            # Decode phase
            self.decoded_instr_prev = self.decoded_instr_current

            # Confirm what to do when we have blank.....
            if(len(self.fetched_instr_prev)>0): 
                self.decoded_instr_current = self.decode(self.fetched_instr_prev)
                if self.decoded_instr_current == -1:
                    print("ERROR OCURRED WHILE DECODING")
                    return -1

            # Dispatch phase
            self.dispatch(self.decoded_instr_prev)
            

            self.PC = self.PC + 1

    def dumpregs(self, iodir):
        for rf in self.RFs.values():
            rf.dump(iodir)

if __name__ == "__main__":
    #parse arguments for input file location
    parser = argparse.ArgumentParser(description='Vector Core Functional Simulator')
    parser.add_argument('--iodir', default="", type=str, help='Path to the folder containing the input files - instructions and data.')
    args = parser.parse_args()

    iodir = os.path.abspath(args.iodir)
    print("IO Directory:", iodir)

    # Parse Config
    config = Config(iodir)

    # Parse IMEM
    imem = IMEM(iodir)  
    # Parse SMEM
    sdmem = DMEM("SDMEM", iodir, 13) # 32 KB is 2^15 bytes = 2^13 K 32-bit words.
    # Parse VMEM
    vdmem = DMEM("VDMEM", iodir, 17) # 512 KB is 2^19 bytes = 2^17 K 32-bit words. 

    # Create Vector Core
    vcore = Core(imem, sdmem, vdmem, config)

    # Run Core
    vcore.run()   
    vcore.dumpregs(iodir)

    sdmem.dump()
    vdmem.dump()

    # THE END