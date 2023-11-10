module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Main(in %I_x: i1, in %I_y: i1, out O_x: i1, out O_y: i1) {
        %2 = sv.wire sym @Main.x_x name "x_x" : !hw.inout<i1>
        sv.assign %2, %I_x : i1
        %0 = sv.read_inout %2 : !hw.inout<i1>
        %3 = sv.wire sym @Main.x_y name "x_y" : !hw.inout<i1>
        sv.assign %3, %I_y : i1
        %1 = sv.read_inout %3 : !hw.inout<i1>
        hw.output %0, %1 : i1, i1
    }
}
