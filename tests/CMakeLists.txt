enable_testing()

message(STATUS "Walking in TESTS")

function (add_xtest test_name test_file)
  set(GTEST_LIBS GTest::gtest_main GTest::gtest GTest::gmock_main GTest::gmock)
  file(GLOB
    SRC_FILES
    "../src/${PROJECT_NAME}/*.cpp"
  )
  add_executable(${test_name} ${test_file})
  target_include_directories(${test_name}
    PRIVATE
      "../include"
      "../src/include"
      "../3rdparty/googletest/googletest/include"
      "../3rdparty/googletest/googlemock/include"
  )
  target_link_libraries(${test_name}
    PRIVATE
      ${GTEST_LIBS}
  )
  target_compile_features(${test_name}
    PRIVATE
      cxx_std_17
  )

  add_test(NAME ${test_name} COMMAND ${test_name})
  message(STATUS "Add ${test_name} to test")
endfunction()
