/**
 * @class SocketFDProvider
 *
 * Opens a file descriptor on a specified TCP port.
 *
 */


#pragma once

#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string>
#include "OutProvider.h"

namespace common {
namespace io {

class SocketOutProvider : public OutProvider {

public:
    SocketOutProvider(short port) : port(port), is_open(false) {
    }

    virtual ~SocketOutProvider() {
        close(file_descriptor);
    }

    virtual std::string debugInfo() const {
        return "TCP socket port: " + port;
    }

    void createSocket() {
        file_descriptor = socket(AF_INET, SOCK_STREAM, 0);

        if (file_descriptor < 0) {
            std::cout << "Could not create socket! " << debugInfo() << std::endl;
            file_descriptor = -1;
        }
    }

    void bindSocket() {
        my_address.sin_family = AF_INET;
        my_address.sin_port = htons(port);
        my_address.sin_addr.s_addr = htonl(INADDR_ANY);
        if (bind(file_descriptor, reinterpret_cast<sockaddr *>(&my_address),
                sizeof(my_address)) < 0) {
            std::cout << "Could not bind socket! " << debugInfo() << std::endl;
        }
    }

    void listenOnSocket() {
        if (listen(file_descriptor, 2) < 0) {
            std::cout << "Could not listen on socket! " << debugInfo()
                                                        << std::endl;
        }
    }

    //blocking!
    void acceptConnections() {
        file_descriptor = accept(file_descriptor,
                                 &client_address, &client_address_len);
        if (file_descriptor < 0) {
            std::cout << "Could not accept connections ! " << debugInfo()
                                                           << std::endl;
        }
    }

    void openCommunicationChannel() {
        createSocket();
        bindSocket();
        listenOnSocket();
        acceptConnections();
        is_open = true;
    }

    bool opened() const {
        return is_open;
    }

private:
    short port;
    sockaddr_in my_address;
    sockaddr client_address;
    socklen_t client_address_len;
    bool is_open;
};

}
}
