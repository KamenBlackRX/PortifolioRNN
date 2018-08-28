#Add src folder to project
set(CMAKE_C_FLAGS "-Wall")
file( GLOB SRCS *.c *.h)
add_executable( trasmutation ${SRCS} )