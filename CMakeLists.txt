cmake_minimum_required(VERSION 3.17)

function(add_binary_bundle BUNDLE_NAME)
    cmake_parse_arguments(PARSE_ARGV 1 ARG "" "" "NAME;PATH")
    foreach (BINARY_NAME BINARY_PATH IN ZIP_LISTS ARG_NAME ARG_PATH)
        get_filename_component(BINARY_PATH "${BINARY_PATH}" ABSOLUTE)
        list(APPEND BUNDLE_FILES "${BINARY_NAME}=\"${BINARY_PATH}\"")
    endforeach ()

    set(BUNDLE_INCLUDE_DIR ${CMAKE_CURRENT_BINARY_DIR}/include)
    set(BUNDLE_HEADER ${BUNDLE_INCLUDE_DIR}/${BUNDLE_NAME}.hpp)
    set(BUNDLE_SOURCE ${CMAKE_CURRENT_BINARY_DIR}/${BUNDLE_NAME}.cpp)

    find_package(Python3 REQUIRED)
    set(EMBEDDER_SCRIPT "${CMAKE_CURRENT_FUNCTION_LIST_DIR}/binary-embedder.py")
    file(MAKE_DIRECTORY ${BUNDLE_INCLUDE_DIR})
    add_custom_command(OUTPUT ${BUNDLE_SOURCE} ${BUNDLE_HEADER}
            COMMAND "${Python3_EXECUTABLE}" "${EMBEDDER_SCRIPT}" "${BUNDLE_HEADER}" "${BUNDLE_SOURCE}" ${BUNDLE_FILES}
            DEPENDS ${ARG_PATH})
    add_library(${BUNDLE_NAME} ${BUNDLE_SOURCE} ${BUNDLE_HEADER})
    target_include_directories(${BUNDLE_NAME} PUBLIC ${BUNDLE_INCLUDE_DIR})
endfunction()
