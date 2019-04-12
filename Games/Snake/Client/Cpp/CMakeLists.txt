project(Cpp)
cmake_minimum_required(VERSION 2.8)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")

add_executable("snake_client" "main.cpp" "Message.cpp" "Math.cpp" "World.cpp" "Decision.cpp")
configure_file(config config)
