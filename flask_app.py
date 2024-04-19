import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request
import glob
import importlib

app = Flask(__name__)

def call_function(function_name, function_data):
  files = glob.glob("./s0*_*.py")[::-1]

  for file in files:
    base_name = os.path.basename(file)
    module_name = base_name.split('.')[0]

    # Import the module
    module = importlib.import_module(module_name)
    # Reload to get the latest version
    module = importlib.reload(module)

    # Check if the module has the desired function
    function_scv_name = "func_"+function_name
    if not hasattr(module, function_scv_name): continue

  try:
    function = getattr(module, function_scv_name)
    return function(function_data)
  except AttributeError as e:
    pass
  # If the function is not found in any of the modules, return None
  return {"data":f"[{function_name}] not defined", "status":"fail"}


@app.route('/', methods=['GET', 'POST'])
def main():
  if request.method == 'POST':
    data = request.form.to_dict()
  else:
    data = request.args.to_dict()

  #check func
  func = data.get('func', '')

  os.chdir(os.path.dirname(__file__))
  
  if func != '':
    response = call_function(func, data)
  else:
    response = {"data":"No function specified", "status":"fail"}

  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8051)