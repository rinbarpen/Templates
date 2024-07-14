message(STATUS "Walking in EXAMPLES")

function (add_xex ex_name ex_file)
  add_executable(${ex_name} ${ex_file})
  target_include_directories(${ex_name}
    PRIVATE
      "../include"
      "../src/include"
  )
  target_link_directories(${ex_name}
    PRIVATE
      
  )
  target_link_libraries(${ex_name}
    PRIVATE
      ${RBP_PROJ_LIBS}
  )
  target_compile_features(${ex_name}
    PRIVATE
      cxx_std_17
  )

  add_test(NAME ${test_name} COMMAND ${test_name})
  message(STATUS "Add ${test_name} to test")
endfunction()
