PROJECT(myfix)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")

FIND_PACKAGE(OpenSSL REQUIRED)
INCLUDE_DIRECTORIES(${OPENSSL_INCLUDE_DIR})
ADD_EXECUTABLE(myfix myfix.cpp  myfix.hpp
    Myfix_classes.cpp  Myfix_classes.hpp  Myfix_router.hpp  Myfix_traits.cpp  Myfix_types.cpp  Myfix_types.hpp)

target_link_libraries(myfix fix8)
target_link_libraries(myfix PocoFoundation)
target_link_libraries(myfix PocoNet)
TARGET_LINK_LIBRARIES(myfix ${OPENSSL_LIBRARIES})
target_link_libraries(myfix pthread)
target_link_libraries(myfix rt)

ADD_EXECUTABLE(hf_test hftest.cpp  hftest.hpp Perf_classes.cpp  Perf_classes.hpp  Perf_router.hpp  Perf_traits.cpp  Perf_types.cpp  Perf_types.hpp)
target_link_libraries(hf_test fix8)
target_link_libraries(hf_test PocoFoundation)
target_link_libraries(hf_test PocoNet)
TARGET_LINK_LIBRARIES(hf_test ${OPENSSL_LIBRARIES})
target_link_libraries(hf_test pthread)
target_link_libraries(hf_test rt)


