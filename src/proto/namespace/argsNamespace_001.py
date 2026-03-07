from argparse import Namespace

args = Namespace(
    name="alice",
    count=5,
    verbose=True,
)

print(f"{args.name}")

args = Namespace(
    command = "start",
    vm = "macOS",
    hypervisor = "utm",
    headless = False,
    hard = True,
)

print(str(args))
    

