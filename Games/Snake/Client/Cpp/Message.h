#include <string>
#include "rapidjson/document.h"
#include "rapidjson/filereadstream.h"
#include "rapidjson/stringbuffer.h"
#include <rapidjson/writer.h>
#include <iostream>
#include <algorithm>
#include <map>

using namespace std;
using namespace rapidjson;
class Vector2D{
public:
    int i;
    int j;

};

class World{
public:
    int ** board;
    Vector2D * head;
    World(string world_msg){

    }
};

class Message{
public:
    string type;
};

class MessageClientConnectRequest : public Message{
public:
    string client_name;
    MessageClientConnectRequest(string name){
        type = string("ClientConnectRequest");
        client_name = name;
    }
    string build(){
        Document d;
        Value json_msg(kObjectType);

        Value json_type;
        json_type.SetString(type.c_str(), type.length(), d.GetAllocator());
        json_msg.AddMember("message_type", json_type, d.GetAllocator());

        Value json_name;
        json_name.SetString(client_name.c_str(), client_name.length(), d.GetAllocator());

        Value json_value;
        json_value.SetObject();
        json_value.AddMember("name", json_name, d.GetAllocator());
        json_msg.AddMember("value", json_value, d.GetAllocator());

        StringBuffer buffer;
        Writer<StringBuffer> writer(buffer);
        json_msg.Accept(writer);
        const char* output = buffer.GetString();
        string msg(output);
        return msg;
    }
};

class MessageClientConnectResponse : public Message{
public:
    int id;
    int max_i;
    int max_j;
    int team_number;
    int goal_id;
    MessageClientConnectResponse(int _id,int _max_i, int _max_j, int _team_number, int _goal_id){
        type = string("MessageClientConnectResponse");
        id = _id;
        max_i = _max_i;
        max_j = _max_j;
        team_number = _team_number;
        goal_id = _goal_id;
    }
    static std::pair<bool, Message *> parse(char * msg){
        std::cout<<msg<<std::endl;
        std::cout<<string(msg)<<std::endl;
        Document d;
        d.Parse(msg);
        std::cout<<"hear0"<<std::endl;

        Value::MemberIterator M;
        for (M=d.MemberBegin(); M!=d.MemberEnd(); M++)
        {
            std::cout<<M->name.GetString()<<std::endl;
        }
        std::cout<<"hear1"<<std::endl;
        string type = d["message_type"].GetString();
        std::cout<<"hear1"<<std::endl;
        if (type.compare(string("MessageClientConnectResponse")) == 0){
            std::cout<<"hear2"<<std::endl;
            Value & value = d["value"];
            int id = value["id"].GetInt();
            Value & ground_config = value["ground_config"];
            std::cout<<"hear3"<<std::endl;
            int max_i = ground_config["max_i"].GetInt();
            int max_j = ground_config["max_j"].GetInt();
            int team_number = ground_config["team_number"].GetInt();
            int goal_id = ground_config["goal_id"].GetInt();
            return std::make_pair(true, new MessageClientConnectResponse(id, max_i, max_j, team_number, goal_id));
        }
        return std::make_pair(false, nullptr);
    }
};
#include <vector>
class MessageClientWorld : public Message{
public:
    int cycle;
    map<string, int> score;
    vector<vector<int> > board;
    MessageClientWorld(int _cycle, map<string, int> _score, vector<vector<int> > _board){
        type = string("MessageClientWorld");
        cycle = _cycle;
        score = _score;
        board = _board;
    }
    static std::pair<bool, Message *> parse(char * msg){
        Document d;
        d.Parse(msg);
        std::cout<<"h1"<<std::endl;
        string type = d["message_type"].GetString();
        std::cout<<"h2"<<std::endl;
        if (type.compare(string("MessageClientWorld")) == 0){
            std::cout<<"h3"<<std::endl;
            Value & value = d["value"];
            int cycle = value["cycle"].GetInt();
            Value & score_value = value["score"];
            Value::MemberIterator M;
            map<string, int> score;
            std::cout<<"h4"<<std::endl;
            for (M=score_value.MemberBegin(); M!=score_value.MemberEnd(); M++)
            {
                std::cout<<"h5"<<std::endl;
                string team = M->name.GetString();
                int sc = M->value.GetInt();
                std::cout<<"h6"<<std::endl;
                score.insert(make_pair(team, sc));
            }
            std::cout<<"h7"<<std::endl;
            Value & world_value = value["world"];
            Value & board_value = world_value["board"];
            vector<vector<int> > board;
            for(auto& p : board_value.GetArray()){
                vector<int> iboard;
                for(auto& q : p.GetArray()){
                    iboard.push_back(q.GetInt());
                }
                board.push_back(iboard);
            }
            Value & heads_value = world_value["heads"];
            return std::make_pair(true, new MessageClientWorld(cycle, score, board));
        }
        return std::make_pair(false, nullptr);
    }
};

Message * pars(char * _msg){
    string str_msg = string(_msg);
    char a = '\'';
    char b = '\"';
    replace(str_msg.begin(), str_msg.end(), a, b);
    char msg[8000];
    memcpy(msg, str_msg.c_str(), str_msg.length());
    msg[str_msg.length()] = '\0';
    std::cout<<str_msg<<std::endl;
    std::pair<bool, Message *> ret;
    std::cout<<"start res"<<std::endl;
    ret = MessageClientConnectResponse::parse(msg);
    if (std::get<0>(ret)){
        return std::get<1>(ret);
    }
    std::cout<<"start world"<<std::endl;
    ret = MessageClientWorld::parse(msg);
    if (std::get<0>(ret)){
        return std::get<1>(ret);
    }
    return nullptr;
}
