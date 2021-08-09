hw.module @Top2to1(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
  %_0 = sv.wire : !hw.inout<i4>

  sv.alwayscomb {
    sv.casez %S : i1
    case b0: {
      sv.bpassign %_0, %I0 : i4
    }
    case b1: {
      sv.bpassign %_0, %I1 : i4
    }
  }

  %0 = sv.read_inout %_0 : !hw.inout<i4>

  hw.output %0 : i4
}

hw.module @Top8to1(%I0: i4, %I1: i4, %I2: i4, %I3: i4, %I4: i4, %I5: i4, %I6: i4, %I7: i4, %S: i3) -> (%O: i4) {
  %_0 = sv.wire : !hw.inout<i4>

  sv.alwayscomb {
    sv.casez %S : i3
    case b000: {
      sv.bpassign %_0, %I0 : i4
    }
    case b001: {
      sv.bpassign %_0, %I1 : i4
    }
    case b010: {
      sv.bpassign %_0, %I2 : i4
    }
    case b011: {
      sv.bpassign %_0, %I3 : i4
    }
    case b100: {
      sv.bpassign %_0, %I4 : i4
    }
    case b101: {
      sv.bpassign %_0, %I5 : i4
    }
    case b110: {
      sv.bpassign %_0, %I6 : i4
    }
    case b111: {
      sv.bpassign %_0, %I7 : i4
    }
  }

  %0 = sv.read_inout %_0 : !hw.inout<i4>

  hw.output %0 : i4
}
