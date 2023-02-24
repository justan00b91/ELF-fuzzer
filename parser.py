import random
import os

def flip_byte(in_bytes):
	i = int(random.randint(0,len(in_bytes)))
	c = bytes(chr(random.randint(0,0xFF)),encoding='utf8')
	return in_bytes[:i] + c + in_bytes[i+1:]

def copy_binary():
	with open("a.out","rb") as orig_f, open("a_f.out", "wb") as new_f:
		new_f.write(flip_byte(orig_f.read()))

def compare(fn1, fn2):
	with open(fn1) as f1, open(fn2) as f2:
		return f1.read()==f2.read()

def check_output():
	os.system("chmod +x a_f.out && ./a_f.out > fuzz_out")
	return compare("orig_out","fuzz_out")

def check_gdb():
	os.system("echo disassemble main| gdb a_f.out > fuzz_gdb")
	return compare("orig_gdb", "fuzz_out")

def prep():
	os.system("mkdir tmp ; cd tmp ; ./a.out > orig_out ; echo disassemble main | gdb a.out > orig_fuzz")

def main():
	while True:
		prep()
		copy_binary()
		if check_output() and not check_gdb():
			os.system("clear")
			print("FOUND POSSIBLE FAIL\n\n\n")
			os.system("tail fuzz_out")
			os.system("tail fuzz_gdb")
			input()

if __name__ == '__main__':
	main()
