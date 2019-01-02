#!/bin/sh
# restart using tclsh \
exec tclsh $0 $@

################################################################################
#
################################################################################

# Modification History
#
# Date    : 4th October 2012
# Author  : Ross Alexander
# Changes : new file
#
# Date    :
# Author  :
# Changes :
#

proc Usage { } {

    puts {
Usage:
    portListener [-t <timeout>] <port1> <port2> ...

Arguments:
  <timeout>    - Timeout in minutes
  <port1,2...> - Port to listen on

}
}

proc Accept { lport sock addr port } {
    puts ""Connection accepted on port $lport from $addr""
    close $sock
}

proc Listen { port } {
    set result 0

    if { [ catch ""socket -server {Accept $port} $port"" op ] } {
        puts ""ERROR listening on port $port: $op""
        set result 0
    } else {
        puts ""Listening for connections on port $port""
        set result 1
    }

    return $result
}

proc Timeout { } {
    puts ""Timeout reached, exiting...""
    exit 0
}

proc Main { } {
    global argc argv

    set timeout 120

    set p 0
    while { [ string match ""-*"" [ lindex $argv $p ] ] } {
        switch -- [ lindex $argv $p ] {
            -t {
                incr p
                set timeout [ lindex $argv $p ]
                incr p
            }
            default {
                Usage
                puts ""ERROR: Unknown parameter '[ lindex $argv $p ]'
                exit 1
            }
        }
    }

    set ports [list]
    foreach port [ lrange $argv $p end ] {
        if { [ regexp {^[0-9]+$} $port ] } {
            lappend ports $port
        } else {
            Usage
            puts ""ERROR: argument '$port' should be a port number.""
            exit
        }
    }

    if { [ llength $ports ] == 0 } {
        Usage
        exit 1
    }

    set count 0
    foreach port $ports {
        if { [ Listen $port ] } {
            incr count
        }
    }

    if { $count } {
        puts ""Script will timout in $timeout minutes.""
        after [ expr $timeout * 60 * 1000 ] Timeout
        vwait forever
    } else {
        puts ""Failed to listen on any ports, exiting...""
        exit 1
    }
}

Main

