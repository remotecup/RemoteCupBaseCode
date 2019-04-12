#include <iostream>
using namespace std;
class Vector2D{
public:
    int i;
    int j;
    bool is_valid;
    Vector2D(int _i, int _j){
        i = _i;
        j = _j;
        is_valid = true;
    }
    Vector2D(){
        i = 0;
        j = 0;
        is_valid = true;
    }
    static Vector2D invalid(){
        Vector2D res;
        res.is_valid = false;
        return res;
    }
    bool isvalid(){
        return is_valid;
    }
    friend ostream& operator<<(ostream& os, const Vector2D& dt){
        os << "("<<dt.i<<","<<dt.j<<")";
        return os;
    }


};
