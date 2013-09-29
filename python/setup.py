from setuptools import setup

setup(
  name = "xively-currentcost",
  version = "0.0.1",
  author = "JDCockrill",
  author_email = "jamiecockrill@hotmail.com",
  description = ("Some code hacked together that I use with a Raspberry Pi to read a CurrentCost energy monitor's serial output and post to Xively"),
  license = "MIT",
  keywords = "currentcost xively raspberrypi",
  scripts = ["cc_xively.py"],
  data_files = [('/etc/init.d',['init.d/cc_xively']),
                ('/etc/xively-currentcost', ['logging.conf', 'xively.conf']),
               ],
  install_requires = ['xively-python>=0.1.0-rc1','pyserial>=2.5', 'pyyaml>=3.10'],
  classifiers = [
    "Development Status :: 3 - Alpha",
    "Topic :: Utilities",
  ],
)
