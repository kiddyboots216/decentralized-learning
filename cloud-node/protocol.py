import json

from autobahn.twisted.websocket import WebSocketServerProtocol

import state
from new_message import validate_new_message, process_new_message


class CloudNodeProtocol(WebSocketServerProtocol):
    """
    Class that implements part of the Cloud Node networking logic (what happens
    when a new node connects, sends a message, disconnects). The networking 
    here happens through Websockets using the autobahn library.
    """
    def onConnect(self, request):
        """
        Logs that a node has successfully connected.
        """
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        """
        Logs that a connection was opened.
        """
        print("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        """
        Deregisters a node upon websocket closure and logs it.
        """
        print("WebSocket connection closed: {}".format(reason))
        self.factory.unregister(self)

    def onMessage(self, payload, isBinary):
        """
        Processes the payload received by a connected node.

        Messages are ignored unless the message is of type "REGISTER" or the
        node has already been registered (by sending a "REGISTER" type message).

        """
        print("Got payload!")
        if isBinary:
            print("Binary message not supported.")
            return

        try:
            received_message = validate_new_message(payload)
        except Exception as e:
            if isinstance(e, json.decoder.JSONDecodeError):
                error_message = "Error while converting JSON."
            else:
                error_message = "Error deserializing message: {}"
                error_message = error_message.format(e)
            message = json.dumps({"error": True, "message": error_message})
            self.sendMessage(message.encode(), isBinary)
            print(error_message)
            return

        # Process message
        results = process_new_message(received_message, self.factory, self)

        if results["error"]:
            # If there was an error, just send the results.
            self.sendMessage(json.dumps(results).encode(), isBinary)
        elif results["action"] == "BROADCAST":
            # If there is no action to take, don't send any messages.
            self._broadcastMessage(
                payload=results["message"],
                client_list=results["client_list"],
                isBinary=isBinary,
            )

        new_message = json.dumps(last_message)
        self.sendMessage(message_json.encode(), isBinary)

        print("[[DEBUG] State: {}".format(state.state))

    def _broadcastMessage(self, payload, client_list, isBinary):
        """
        Broadcast message (`payload`) to a `client_list`.
        """
        for c in client_list:
            results_json = json.dumps(payload)
            c.sendMessage(results_json.encode(), isBinary)