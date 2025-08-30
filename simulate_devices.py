import os, sys, subprocess, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--count", type=int, default=10)
args = parser.parse_args()

root = os.path.dirname(os.path.abspath(__file__))
client = os.path.join(root, "client", "device.py")
python = sys.executable  # uses the current venv interpreter

procs = []
for i in range(1, args.count + 1):
    dev_id = f"SIM-DEVICE-{i}"
    print(f"🚀 Starting {dev_id}")
    procs.append(subprocess.Popen([python, client, dev_id], cwd=root))

for p in procs:
    p.wait()

print(f"✅ All {args.count} devices finished")
