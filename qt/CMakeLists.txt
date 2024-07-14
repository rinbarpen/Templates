cmake_minimum_required(VERSION 3.6)

project("TemplateCXXProj" VERSION 0.1 LANGUAGES CXX)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Debug")
endif()

message("Build ${PROJECT_NAME} with ${CMAKE_BUILD_TYPE}")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${CMAKE_BUILD_TYPE}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${CMAKE_BUILD_TYPE}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${CMAKE_BUILD_TYPE}")

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


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

find_package(Qt6 COMPONENTS Widgets Sql OpenglWidgets Opengl)

file(GLOB SRC_FILES "${CMAKE_CURRENT_SOURCE_DIR}/src/${PROJECT_NAME}")
file(GLOB UI_FILES "${CMAKE_CURRENT_SOURCE_DIR}/ui/${PROJECT_NAME}")
file(GLOB RC_FILES "${CMAKE_CURRENT_SOURCE_DIR}/assets")

file(GLOB
  SRC_FILES
  "${CMAKE_CURRENT_SOURCE_DIR}/src/${PROJECT_NAME}/*.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/include/${PROJECT_NAME}/*.hpp"
)

if(ENABLE_TEST)
  add_subdirectory(tests)
endif()

set(PROJECT_LIBS
  ""
)
if(WIN32)
  list(APPEND PROJECT_LIBS "")
elseif(LINUX)
  list(APPEND PROJECT_LIBS "")
endif()

set(PROJECT_INCLUDES
  ""
)

set(PROJECT_LIB_DIRS
  ""
)

add_executable(${PROJECT_NAME} ${SRC_FILES} "src/main.cpp")
target_include_directories(${PROJECT_NAME}
PRIVATE
  "${CMAKE_CURRENT_SOURCE_DIR}/src/include"
  ${PROJECT_INCLUDES}
  ${QT_INCLUDES}
)
target_link_directories(${PROJECT_NAME}
PRIVATE
  ${PROJECT_LIB_DIRS}
)
target_link_libraries(${PROJECT_NAME}
PRIVATE
  ${PROJECT_LIBS}
  Qt::Widget
)
target_compile_features(${PROJECT_NAME}
PRIVATE
  cxx_std_17
)
