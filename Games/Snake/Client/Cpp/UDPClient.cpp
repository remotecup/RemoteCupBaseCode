#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string>
#include <iostream>
#include <cstring>
#include "Message.h"
#include <algorithm>

using namespace std;

int main() {

//    char * x = "{\"message_type\": \"MessageClientWorld\", \"value\": {\"cycle\": 638, \"score\": {\"team_name6599\": -1493, \"team_name3884\": -1354, \"team_name5381\": -1290, \"nader\": -3185}, \"world\": {\"board\": [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 5, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 1, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 1, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, -1, -1, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], [-1, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]], \"heads\": {\"team_name6599\": [9, 28], \"team_name3884\": [1, 26], \"team_name5381\": [27, 3], \"nader\": [28, 26]}}}}}";
//    Document d;
//    d.Parse(x);
//    std::cout<<"hear0"<<std::endl;

//    Value::MemberIterator M;
//    for (M=d.MemberBegin(); M!=d.MemberEnd(); M++)
//    {
//        std::cout<<M->name.GetString()<<std::endl;
//    }

//    return 0;
    int thisSocket;
    struct sockaddr_in destination;

    destination.sin_family = AF_INET;
    thisSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (thisSocket < 0)
    {
        printf("\nSocket Creation FAILED!");
        return 0;
    }

    destination.sin_port = htons(20002);
    destination.sin_addr.s_addr = inet_addr("0.0.0.0");
    if (connect(thisSocket,(struct sockaddr *)&destination,sizeof(destination))!=0){
        printf("\nSocket Connection FAILED!\n");
        //		if (thisSocket) close(thisSocket);
        return 0;
    }
    string msg = MessageClientConnectRequest(string("nader")).build();
    char buffer[4096];
    memcpy(buffer, msg.c_str(), msg.length());

    send(thisSocket, buffer, msg.length(), 0);
    socklen_t len;
    ssize_t newData;
    size_t maxr = 4096;
    char rcvb[4096];
    std::cout<<"rcvb"<<std::endl;
    newData = recvfrom(thisSocket, rcvb, 4096,
                       MSG_WAITALL, (struct sockaddr *) &destination,
                       &len);
    std::cout<<string(rcvb)<<std::endl;

    Message * Msg = pars(rcvb);
    if(Msg != nullptr){
        std::cout<<"msg is ok"<<std::endl;
        std::cout<<static_cast<MessageClientConnectResponse *>(Msg)->id<<std::endl;
        std::cout<<static_cast<MessageClientConnectResponse *>(Msg)->max_i<<std::endl;
        std::cout<<static_cast<MessageClientConnectResponse *>(Msg)->max_j<<std::endl;
        std::cout<<static_cast<MessageClientConnectResponse *>(Msg)->team_number<<std::endl;
        std::cout<<static_cast<MessageClientConnectResponse *>(Msg)->goal_id<<std::endl;
    }
    std::cout<<newData<<std::endl;
    //    close(thisSocket)

    while (true){
        char rcvb[8000];
        std::cout<<"rcvb"<<std::endl;
        socklen_t len;
        newData = recvfrom(thisSocket, rcvb, 8000,
                           MSG_WAITALL, (struct sockaddr *) &destination,
                           &len);

        std::cout<<rcvb<<std::endl;
        std::cout<<newData<<std::endl;
        rcvb[newData] = '\0';
        Message * Msg = pars(rcvb);
        if(Msg != nullptr){
            std::cout<<static_cast<MessageClientWorld *>(Msg)->score["nader"]<<std::endl;

        }



        string msg("{\"message_type\":\"MessageClientAction\" , \"value\": {\"action\": \"d\"}}");
        char action[4096];
        memcpy(action, msg.c_str(), msg.length());

        send(thisSocket, action, msg.length(), 0);
    }


    return 0;
}
