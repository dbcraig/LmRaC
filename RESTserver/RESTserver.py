
# Import user-functions
from DEGbasic import *

# Instantiate user-functions
DEGbasic = DEGbasic()

# Add user-functions to the functions dictionary
# this makes the named functions available to the REST interface below
functions = {}
functions.update( DEGbasic.functionsList() )


# Import Flask and setup the REST server
from flask import Flask, request

app = Flask(__name__)

@app.route('/lmrac/<function_name>', methods=['GET'])
def get_function(function_name):
    params = request.args
    function = functions.get(function_name)
    if function:
        if ( params['params'] == '{}' ):    # If no parameters are passed
            return function()
        else:
            return function(**params)
    else:
        return f"Function Error lmrac_{function_name}  Sorry. Function not found."  
        # IMPORTANT
        # the prefix "Function Error lmrac_" is necessary for LmRaC to handle the error

if __name__ == '__main__':
    print("\nLmRaC functions REST server starting...")
    # NOTE: although we can set the port, we can't set the IP address since that is managed by the Docker container
    #       When running in VS Code the start up message will show the IP address (e.g., http://172.17.0.2:5001)
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
