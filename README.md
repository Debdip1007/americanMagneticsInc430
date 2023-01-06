# americanMagneticsInc430
Python driver for the AMI model 430 magnet power supply controller

# Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Requirements
numpy  
pyvisa  
pyvisa-py

# Usage
To connect to the device, you must pass the address as implemented by pyvisa as the first argument.
Many queries and write functions are accessed as attributes (as opposed to functions).

Example code:
```
from ami430 import AMI430
import pyvisa as visa

rm = visa.ResourceManager() 
resources = rm.list_resources()
for resource in resources:
    print('address: {}:\nname: {}'.format(resource, rm.open_resource(resource).query('*IDN?')))


mag = AMI430("TCPIP0::192.168.0.41::7180::SOCKET") # The string should be the same as the address printed in the last loop.
mag.target_current = 5
mag.ramp_rate_current = 0.03
mag.ramp()
while mag.state != "HOLDING":
    sleep(5)
print('Target field reached')
mag.target_current = 0
mag.ramp()
while mag.state != "HOLDING":
    sleep(5)

print('Magnet turned off')

```
