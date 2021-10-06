import os,hashlib
import time
import sys
import argparse

cache={}
detailed={}

def driver(start_path):
   sc=open("2rm2.sh","w+")
   os.chmod("2rm2.sh",0755)
   print time.ctime(time.time())
   print "building cache..."
   for root,dirs,files in os.walk(start_path):
      for name in files:
         if os.path.basename(name).startswith('.'):
            continue
         fpath=os.path.join(root,name)
         md5=hashlib.md5(open(fpath,"rb").read(10)).hexdigest()
         if md5 in cache:
            cache[md5].append(fpath)
         else:
            cache[md5]=[fpath]
   print time.ctime(time.time())
   print "searching for duplicates..."
   for h, flist in cache.items():
      if len(flist)>1:
         for fl in flist:
            fullmd5=hashlib.md5(open(fl,"rb").read()).hexdigest()
            if fullmd5 in detailed:
               detailed[fullmd5].append(fl)
            else:
               detailed[fullmd5]=[fl]
   print time.ctime(time.time())
   print "generating a remove script"
   for k,v in detailed.items():
      if len(v)>1:
         sc.write("echo original: %s" % (v[0]))
         sc.write("\n")
         for f in v[1:]:
            sc.write('rm -f "%s"' % (f))
            sc.write("\n")
               
   sc.close()
   print time.ctime(time.time())
   print "done."

if __name__=='__main__':
    if sys.platform not in ["darwin", "linux"]:
        print("WARNING: Generated script may not work on your system")
    example=str(sys.argv[0]) + " --path /apps/"
    argp=argparse.ArgumentParser(description="Duplicate files finder", epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter)
    argp.add_argument('--path', '-p', help="Path from which to start scanning")
    parsed=argp.parse_args()
    if os.path.isdir(parsed.path):
        print(driver(parsed.path))
    else:
        raise ValueError( str(parsed.path) + " doesn't exist or not a directory")

