import pyvisa

from InstVirtualLib.osciloscopios import RIGOL_DS2202

if __name__ == "__main__":
    scope_handler = pyvisa.ResourceManager().open_resource("TCPIP::192.168.0.101::INSTR", timeout=10000)  # TODO: parametrizar IP
    scope = RIGOL_DS2202(scope_handler)
    idn = scope.print_ID()
    scope.close()
    print(f"EL IDN es: {idn}")