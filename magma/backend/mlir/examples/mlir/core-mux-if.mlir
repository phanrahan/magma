hw.module @Top2to1(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
  %_0 = sv.wire : !hw.inout<i4>

  %const_0 = hw.constant 0 : i1
  %S_0 = comb.icmp eq %S, %const_0 : i1

  sv.alwayscomb {
    sv.if %S_0 {
      sv.bpassign %_0, %I0 : i4
    } else {
      sv.bpassign %_0, %I1 : i4
    }
  }

  %0 = sv.read_inout %_0 : !hw.inout<i4>

  hw.output %0 : i4
}

hw.module @Top8to1(%I0: i4, %I1: i4, %I2: i4, %I3: i4, %I4: i4, %I5: i4, %I6: i4, %I7: i4, %S: i3) -> (%O: i4) {
  %_0 = sv.wire : !hw.inout<i4>

  %const_0 = hw.constant 0 : i3
  %const_1 = hw.constant 1 : i3
  %const_2 = hw.constant 2 : i3
  %const_3 = hw.constant 3 : i3
  %const_4 = hw.constant 4 : i3
  %const_5 = hw.constant 5 : i3
  %const_6 = hw.constant 6 : i3
  %S_0 = comb.icmp eq %S, %const_0 : i3
  %S_1 = comb.icmp eq %S, %const_1 : i3
  %S_2 = comb.icmp eq %S, %const_2 : i3
  %S_3 = comb.icmp eq %S, %const_3 : i3
  %S_4 = comb.icmp eq %S, %const_4 : i3
  %S_5 = comb.icmp eq %S, %const_5 : i3
  %S_6 = comb.icmp eq %S, %const_6 : i3

  sv.alwayscomb {
    sv.if %S_0 {
      sv.bpassign %_0, %I0 : i4
    } else {
      sv.if %S_1 {
        sv.bpassign %_0, %I1 : i4
      } else {
        sv.if %S_2 {
          sv.bpassign %_0, %I2 : i4
        } else {
          sv.if %S_3 {
            sv.bpassign %_0, %I3 : i4
          } else {
            sv.if %S_4 {
              sv.bpassign %_0, %I4 : i4
            } else {
              sv.if %S_5 {
                sv.bpassign %_0, %I5 : i4
              } else {
                sv.if %S_6 {
                  sv.bpassign %_0, %I6 : i4
                } else {
                  sv.bpassign %_0, %I7 : i4
                }
              }
            }
          }
        }
      }
    }
  }

  %0 = sv.read_inout %_0 : !hw.inout<i4>

  hw.output %0 : i4
}
