cmake_minimum_required(VERSION 3.6)

project("TemplateCXXProj" VERSION 0.1 LANGUAGES CXX)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Debug")
endif()

message("Build ${PROJECT_NAME} with ${CMAKE_BUILD_TYPE}")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${CMAKE_BUILD_TYPE}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${CMAKE_BUILD_TYPE}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${CMAKE_BUILD_TYPE}")

function(add_3rdparty_proj proj_name)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/${proj_name})
endfunction()
# ######################################## Requirments Begin ########################################

# ######################################## Requirments End   ########################################

function(add_lib lib_name BIG_LIB_NAME libs)
  set(${BIG_LIB_NAME}_DIR "${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/${lib_name}")
  if(WIN32)
    set(${BIG_LIB_NAME}_LIBRARIES_DIR "${BIG_LIB_NAME}_DIR/lib/win")
  else()
    set(${BIG_LIB_NAME}_LIBRARIES_DIR "${BIG_LIB_NAME}_DIR/lib/linux")
  endif()
  set(${BIG_LIB_NAME}_LIBRARIES libs)
  set(${BIG_LIB_NAME}_INCLUDE "${BIG_LIB_NAME}_DIR/include")
  message(STATUS "Load ${lib_name}")
endfunction()
# ######################################## Library Begin ############################################

# ######################################## Library End   ############################################

file(GLOB
  SRC_FILES
  "${CMAKE_CURRENT_SOURCE_DIR}/src/${PROJECT_NAME}/*.cpp"
)

set(RBP_PROJ_LIBS
  ""
)
if(WIN32)
  list(APPEND RBP_PROJ_LIBS "")
elseif(LINUX)
  list(APPEND RBP_PROJ_LIBS "")
endif()

set(RBP_PROJ_INCLUDES
CACHE STRING
  ""
)

set(RBP_PROJ_LIB_DIRS
CACHE STRING
  ""
)

set(RBP_PROJ_NAME ${PROJECT_NAME})

add_executable(${RBP_PROJ_NAME} ${SRC_FILES} "src/main.cpp")
target_include_directories(${RBP_PROJ_NAME}
PRIVATE
  "${CMAKE_CURRENT_SOURCE_DIR}/src/include"
  ${RBP_PROJ_INCLUDES}
)
target_link_directories(${RBP_PROJ_NAME}
PRIVATE
  ${RBP_PROJ_LIB_DIRS}
)
target_link_libraries(${RBP_PROJ_NAME}
PRIVATE
  ${RBP_PROJ_LIBS}
)
target_compile_features(${RBP_PROJ_NAME}
PRIVATE
  cxx_std_17
)

add_subdirectory(tests)
add_subdirectory(examples)
