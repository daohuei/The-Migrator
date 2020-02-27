import flask
import request

@app.route('/update_node', methods=['POST'])
def update_node():
    # Get latency from each server via request
    # Get system info of each server from OpenStack
    pass


@app.route('/get_server', methods=['GET'])
def get_server():
    # Return a list of active servers
    pass


@app.route('/register', methods=['POST'])
def register_node():
    # Get internal and external IP address from edges
    # Store it in a database
    pass


@app.route('/client_connect', methods=['POST'])
def client_connect():
    # Spawn an instance for the client
    get_server()
    pass


def main():
    # Initiate the controller object and server
    # Initiate scheduler thread
    pass


if __name__ == '__main__':
    main()
