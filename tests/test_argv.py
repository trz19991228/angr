import nose
import angr, claripy

import logging
l = logging.getLogger("angr_tests")

import os
test_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'binaries', 'tests')

plate={
    'mips':0x400768,
    'mipsel':0x400768,
    'i386':0x804845B,
    'amd64':0x400571,
    'arm':0x1048c,
    'ppc32':0x10000498
}

def test(arch):
    proj = angr.Project(os.path.join(test_location, arch, 'argv_test'))
    r_addr = plate[arch]

    s = proj.factory.entry_state(args = ['aaa', "Yan is a noob"], env ={"HOME": "/home/angr"})
    xpl = proj.factory.simulation_manager(s).explore(find=r_addr)

    nose.tools.assert_equal(len(xpl.found), 1)

    s = proj.factory.entry_state(args = ['aaa', 'Yan is not a noob'], env ={"HOME": "/home/angr"})
    xpl = proj.factory.simulation_manager(s).explore(find=r_addr)

    nose.tools.assert_equal(len(xpl.found), 0)

    # symbolic command line argument
    arg = claripy.BVS('arg_2', 50*8)
    s = proj.factory.entry_state(args = ['aaa', arg], env ={"HOME": "/home/angr"})
    xpl = proj.factory.simulation_manager(s).explore(find=r_addr)

    found = xpl.found[0]
    conc = found.solver.eval(found.memory.load(found.registers.load('sp'), 400), cast_to=bytes)

    nose.tools.assert_equal(b"Yan is a noob" in conc, True)
    
    
if __name__ == "__main__":
    for i in plate
        test(i)
