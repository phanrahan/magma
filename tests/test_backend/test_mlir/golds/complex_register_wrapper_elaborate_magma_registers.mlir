module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Register(%I: !hw.struct<x: i8, y: i1>, %CE: i1, %CLK: i1, %ASYNCRESET: i1) -> (O: !hw.struct<x: i8, y: i1>) {
        %1 = comb.extract %0 from 1 : (i9) -> i1
        %2 = comb.extract %0 from 2 : (i9) -> i1
        %3 = comb.extract %0 from 3 : (i9) -> i1
        %4 = comb.extract %0 from 4 : (i9) -> i1
        %5 = comb.extract %0 from 5 : (i9) -> i1
        %6 = comb.extract %0 from 6 : (i9) -> i1
        %7 = comb.extract %0 from 7 : (i9) -> i1
        %9 = comb.concat %7, %6, %5, %4, %3, %2, %1, %8 : i1, i1, i1, i1, i1, i1, i1, i1
        %10 = comb.extract %0 from 8 : (i9) -> i1
        %11 = hw.struct_create (%9, %10) : !hw.struct<x: i8, y: i1>
        %13 = hw.array_create %I, %11 : !hw.struct<x: i8, y: i1>
        %12 = hw.array_get %13[%CE] : !hw.array<2x!hw.struct<x: i8, y: i1>>, i1
        %14 = hw.struct_extract %12["x"] : !hw.struct<x: i8, y: i1>
        %15 = comb.extract %14 from 0 : (i8) -> i1
        %16 = comb.extract %14 from 1 : (i8) -> i1
        %17 = comb.extract %14 from 2 : (i8) -> i1
        %18 = comb.extract %14 from 3 : (i8) -> i1
        %19 = comb.extract %14 from 4 : (i8) -> i1
        %20 = comb.extract %14 from 5 : (i8) -> i1
        %21 = comb.extract %14 from 6 : (i8) -> i1
        %22 = comb.extract %14 from 7 : (i8) -> i1
        %23 = hw.struct_extract %12["y"] : !hw.struct<x: i8, y: i1>
        %24 = comb.concat %23, %22, %21, %20, %19, %18, %17, %16, %15 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %25 = sv.reg {name = "reg_PR9_inst0"} : !hw.inout<i9>
        sv.alwaysff(posedge %CLK) {
            sv.passign %25, %24 : i9
        } (asyncreset : posedge %ASYNCRESET) {
            sv.passign %25, %26 : i9
        }
        %26 = hw.constant 266 : i9
        sv.initial {
            sv.bpassign %25, %26 : i9
        }
        %0 = sv.read_inout %25 : !hw.inout<i9>
        %8 = comb.extract %0 from 0 : (i9) -> i1
        %27 = comb.concat %7, %6, %5, %4, %3, %2, %1, %8 : i1, i1, i1, i1, i1, i1, i1, i1
        %28 = hw.struct_create (%27, %10) : !hw.struct<x: i8, y: i1>
        hw.output %28 : !hw.struct<x: i8, y: i1>
    }
    hw.module @Register_unq1(%I: !hw.array<6xi16>, %CLK: i1) -> (O: !hw.array<6xi16>) {
        %1 = hw.constant 0 : i3
        %0 = hw.array_get %I[%1] : !hw.array<6xi16>, i3
        %2 = comb.extract %0 from 0 : (i16) -> i1
        %3 = comb.extract %0 from 1 : (i16) -> i1
        %4 = comb.extract %0 from 2 : (i16) -> i1
        %5 = comb.extract %0 from 3 : (i16) -> i1
        %6 = comb.extract %0 from 4 : (i16) -> i1
        %7 = comb.extract %0 from 5 : (i16) -> i1
        %8 = comb.extract %0 from 6 : (i16) -> i1
        %9 = comb.extract %0 from 7 : (i16) -> i1
        %10 = comb.extract %0 from 8 : (i16) -> i1
        %11 = comb.extract %0 from 9 : (i16) -> i1
        %12 = comb.extract %0 from 10 : (i16) -> i1
        %13 = comb.extract %0 from 11 : (i16) -> i1
        %14 = comb.extract %0 from 12 : (i16) -> i1
        %15 = comb.extract %0 from 13 : (i16) -> i1
        %16 = comb.extract %0 from 14 : (i16) -> i1
        %17 = comb.extract %0 from 15 : (i16) -> i1
        %19 = hw.constant 1 : i3
        %18 = hw.array_get %I[%19] : !hw.array<6xi16>, i3
        %20 = comb.extract %18 from 0 : (i16) -> i1
        %21 = comb.extract %18 from 1 : (i16) -> i1
        %22 = comb.extract %18 from 2 : (i16) -> i1
        %23 = comb.extract %18 from 3 : (i16) -> i1
        %24 = comb.extract %18 from 4 : (i16) -> i1
        %25 = comb.extract %18 from 5 : (i16) -> i1
        %26 = comb.extract %18 from 6 : (i16) -> i1
        %27 = comb.extract %18 from 7 : (i16) -> i1
        %28 = comb.extract %18 from 8 : (i16) -> i1
        %29 = comb.extract %18 from 9 : (i16) -> i1
        %30 = comb.extract %18 from 10 : (i16) -> i1
        %31 = comb.extract %18 from 11 : (i16) -> i1
        %32 = comb.extract %18 from 12 : (i16) -> i1
        %33 = comb.extract %18 from 13 : (i16) -> i1
        %34 = comb.extract %18 from 14 : (i16) -> i1
        %35 = comb.extract %18 from 15 : (i16) -> i1
        %37 = hw.constant 2 : i3
        %36 = hw.array_get %I[%37] : !hw.array<6xi16>, i3
        %38 = comb.extract %36 from 0 : (i16) -> i1
        %39 = comb.extract %36 from 1 : (i16) -> i1
        %40 = comb.extract %36 from 2 : (i16) -> i1
        %41 = comb.extract %36 from 3 : (i16) -> i1
        %42 = comb.extract %36 from 4 : (i16) -> i1
        %43 = comb.extract %36 from 5 : (i16) -> i1
        %44 = comb.extract %36 from 6 : (i16) -> i1
        %45 = comb.extract %36 from 7 : (i16) -> i1
        %46 = comb.extract %36 from 8 : (i16) -> i1
        %47 = comb.extract %36 from 9 : (i16) -> i1
        %48 = comb.extract %36 from 10 : (i16) -> i1
        %49 = comb.extract %36 from 11 : (i16) -> i1
        %50 = comb.extract %36 from 12 : (i16) -> i1
        %51 = comb.extract %36 from 13 : (i16) -> i1
        %52 = comb.extract %36 from 14 : (i16) -> i1
        %53 = comb.extract %36 from 15 : (i16) -> i1
        %55 = hw.constant 3 : i3
        %54 = hw.array_get %I[%55] : !hw.array<6xi16>, i3
        %56 = comb.extract %54 from 0 : (i16) -> i1
        %57 = comb.extract %54 from 1 : (i16) -> i1
        %58 = comb.extract %54 from 2 : (i16) -> i1
        %59 = comb.extract %54 from 3 : (i16) -> i1
        %60 = comb.extract %54 from 4 : (i16) -> i1
        %61 = comb.extract %54 from 5 : (i16) -> i1
        %62 = comb.extract %54 from 6 : (i16) -> i1
        %63 = comb.extract %54 from 7 : (i16) -> i1
        %64 = comb.extract %54 from 8 : (i16) -> i1
        %65 = comb.extract %54 from 9 : (i16) -> i1
        %66 = comb.extract %54 from 10 : (i16) -> i1
        %67 = comb.extract %54 from 11 : (i16) -> i1
        %68 = comb.extract %54 from 12 : (i16) -> i1
        %69 = comb.extract %54 from 13 : (i16) -> i1
        %70 = comb.extract %54 from 14 : (i16) -> i1
        %71 = comb.extract %54 from 15 : (i16) -> i1
        %73 = hw.constant 4 : i3
        %72 = hw.array_get %I[%73] : !hw.array<6xi16>, i3
        %74 = comb.extract %72 from 0 : (i16) -> i1
        %75 = comb.extract %72 from 1 : (i16) -> i1
        %76 = comb.extract %72 from 2 : (i16) -> i1
        %77 = comb.extract %72 from 3 : (i16) -> i1
        %78 = comb.extract %72 from 4 : (i16) -> i1
        %79 = comb.extract %72 from 5 : (i16) -> i1
        %80 = comb.extract %72 from 6 : (i16) -> i1
        %81 = comb.extract %72 from 7 : (i16) -> i1
        %82 = comb.extract %72 from 8 : (i16) -> i1
        %83 = comb.extract %72 from 9 : (i16) -> i1
        %84 = comb.extract %72 from 10 : (i16) -> i1
        %85 = comb.extract %72 from 11 : (i16) -> i1
        %86 = comb.extract %72 from 12 : (i16) -> i1
        %87 = comb.extract %72 from 13 : (i16) -> i1
        %88 = comb.extract %72 from 14 : (i16) -> i1
        %89 = comb.extract %72 from 15 : (i16) -> i1
        %91 = hw.constant 5 : i3
        %90 = hw.array_get %I[%91] : !hw.array<6xi16>, i3
        %92 = comb.extract %90 from 0 : (i16) -> i1
        %93 = comb.extract %90 from 1 : (i16) -> i1
        %94 = comb.extract %90 from 2 : (i16) -> i1
        %95 = comb.extract %90 from 3 : (i16) -> i1
        %96 = comb.extract %90 from 4 : (i16) -> i1
        %97 = comb.extract %90 from 5 : (i16) -> i1
        %98 = comb.extract %90 from 6 : (i16) -> i1
        %99 = comb.extract %90 from 7 : (i16) -> i1
        %100 = comb.extract %90 from 8 : (i16) -> i1
        %101 = comb.extract %90 from 9 : (i16) -> i1
        %102 = comb.extract %90 from 10 : (i16) -> i1
        %103 = comb.extract %90 from 11 : (i16) -> i1
        %104 = comb.extract %90 from 12 : (i16) -> i1
        %105 = comb.extract %90 from 13 : (i16) -> i1
        %106 = comb.extract %90 from 14 : (i16) -> i1
        %107 = comb.extract %90 from 15 : (i16) -> i1
        %108 = comb.concat %107, %106, %105, %104, %103, %102, %101, %100, %99, %98, %97, %96, %95, %94, %93, %92, %89, %88, %87, %86, %85, %84, %83, %82, %81, %80, %79, %78, %77, %76, %75, %74, %71, %70, %69, %68, %67, %66, %65, %64, %63, %62, %61, %60, %59, %58, %57, %56, %53, %52, %51, %50, %49, %48, %47, %46, %45, %44, %43, %42, %41, %40, %39, %38, %35, %34, %33, %32, %31, %30, %29, %28, %27, %26, %25, %24, %23, %22, %21, %20, %17, %16, %15, %14, %13, %12, %11, %10, %9, %8, %7, %6, %5, %4, %3, %2 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %110 = sv.reg {name = "reg_P96_inst0"} : !hw.inout<i96>
        sv.alwaysff(posedge %CLK) {
            sv.passign %110, %108 : i96
        }
        %111 = hw.constant 12089405771787748463738880 : i96
        sv.initial {
            sv.bpassign %110, %111 : i96
        }
        %109 = sv.read_inout %110 : !hw.inout<i96>
        %112 = comb.extract %109 from 0 : (i96) -> i1
        %113 = comb.extract %109 from 1 : (i96) -> i1
        %114 = comb.extract %109 from 2 : (i96) -> i1
        %115 = comb.extract %109 from 3 : (i96) -> i1
        %116 = comb.extract %109 from 4 : (i96) -> i1
        %117 = comb.extract %109 from 5 : (i96) -> i1
        %118 = comb.extract %109 from 6 : (i96) -> i1
        %119 = comb.extract %109 from 7 : (i96) -> i1
        %120 = comb.extract %109 from 8 : (i96) -> i1
        %121 = comb.extract %109 from 9 : (i96) -> i1
        %122 = comb.extract %109 from 10 : (i96) -> i1
        %123 = comb.extract %109 from 11 : (i96) -> i1
        %124 = comb.extract %109 from 12 : (i96) -> i1
        %125 = comb.extract %109 from 13 : (i96) -> i1
        %126 = comb.extract %109 from 14 : (i96) -> i1
        %127 = comb.extract %109 from 15 : (i96) -> i1
        %128 = comb.concat %127, %126, %125, %124, %123, %122, %121, %120, %119, %118, %117, %116, %115, %114, %113, %112 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %129 = comb.extract %109 from 16 : (i96) -> i1
        %130 = comb.extract %109 from 17 : (i96) -> i1
        %131 = comb.extract %109 from 18 : (i96) -> i1
        %132 = comb.extract %109 from 19 : (i96) -> i1
        %133 = comb.extract %109 from 20 : (i96) -> i1
        %134 = comb.extract %109 from 21 : (i96) -> i1
        %135 = comb.extract %109 from 22 : (i96) -> i1
        %136 = comb.extract %109 from 23 : (i96) -> i1
        %137 = comb.extract %109 from 24 : (i96) -> i1
        %138 = comb.extract %109 from 25 : (i96) -> i1
        %139 = comb.extract %109 from 26 : (i96) -> i1
        %140 = comb.extract %109 from 27 : (i96) -> i1
        %141 = comb.extract %109 from 28 : (i96) -> i1
        %142 = comb.extract %109 from 29 : (i96) -> i1
        %143 = comb.extract %109 from 30 : (i96) -> i1
        %144 = comb.extract %109 from 31 : (i96) -> i1
        %145 = comb.concat %144, %143, %142, %141, %140, %139, %138, %137, %136, %135, %134, %133, %132, %131, %130, %129 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %146 = comb.extract %109 from 32 : (i96) -> i1
        %147 = comb.extract %109 from 33 : (i96) -> i1
        %148 = comb.extract %109 from 34 : (i96) -> i1
        %149 = comb.extract %109 from 35 : (i96) -> i1
        %150 = comb.extract %109 from 36 : (i96) -> i1
        %151 = comb.extract %109 from 37 : (i96) -> i1
        %152 = comb.extract %109 from 38 : (i96) -> i1
        %153 = comb.extract %109 from 39 : (i96) -> i1
        %154 = comb.extract %109 from 40 : (i96) -> i1
        %155 = comb.extract %109 from 41 : (i96) -> i1
        %156 = comb.extract %109 from 42 : (i96) -> i1
        %157 = comb.extract %109 from 43 : (i96) -> i1
        %158 = comb.extract %109 from 44 : (i96) -> i1
        %159 = comb.extract %109 from 45 : (i96) -> i1
        %160 = comb.extract %109 from 46 : (i96) -> i1
        %161 = comb.extract %109 from 47 : (i96) -> i1
        %162 = comb.concat %161, %160, %159, %158, %157, %156, %155, %154, %153, %152, %151, %150, %149, %148, %147, %146 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %163 = comb.extract %109 from 48 : (i96) -> i1
        %164 = comb.extract %109 from 49 : (i96) -> i1
        %165 = comb.extract %109 from 50 : (i96) -> i1
        %166 = comb.extract %109 from 51 : (i96) -> i1
        %167 = comb.extract %109 from 52 : (i96) -> i1
        %168 = comb.extract %109 from 53 : (i96) -> i1
        %169 = comb.extract %109 from 54 : (i96) -> i1
        %170 = comb.extract %109 from 55 : (i96) -> i1
        %171 = comb.extract %109 from 56 : (i96) -> i1
        %172 = comb.extract %109 from 57 : (i96) -> i1
        %173 = comb.extract %109 from 58 : (i96) -> i1
        %174 = comb.extract %109 from 59 : (i96) -> i1
        %175 = comb.extract %109 from 60 : (i96) -> i1
        %176 = comb.extract %109 from 61 : (i96) -> i1
        %177 = comb.extract %109 from 62 : (i96) -> i1
        %178 = comb.extract %109 from 63 : (i96) -> i1
        %179 = comb.concat %178, %177, %176, %175, %174, %173, %172, %171, %170, %169, %168, %167, %166, %165, %164, %163 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %180 = comb.extract %109 from 64 : (i96) -> i1
        %181 = comb.extract %109 from 65 : (i96) -> i1
        %182 = comb.extract %109 from 66 : (i96) -> i1
        %183 = comb.extract %109 from 67 : (i96) -> i1
        %184 = comb.extract %109 from 68 : (i96) -> i1
        %185 = comb.extract %109 from 69 : (i96) -> i1
        %186 = comb.extract %109 from 70 : (i96) -> i1
        %187 = comb.extract %109 from 71 : (i96) -> i1
        %188 = comb.extract %109 from 72 : (i96) -> i1
        %189 = comb.extract %109 from 73 : (i96) -> i1
        %190 = comb.extract %109 from 74 : (i96) -> i1
        %191 = comb.extract %109 from 75 : (i96) -> i1
        %192 = comb.extract %109 from 76 : (i96) -> i1
        %193 = comb.extract %109 from 77 : (i96) -> i1
        %194 = comb.extract %109 from 78 : (i96) -> i1
        %195 = comb.extract %109 from 79 : (i96) -> i1
        %196 = comb.concat %195, %194, %193, %192, %191, %190, %189, %188, %187, %186, %185, %184, %183, %182, %181, %180 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %197 = comb.extract %109 from 80 : (i96) -> i1
        %198 = comb.extract %109 from 81 : (i96) -> i1
        %199 = comb.extract %109 from 82 : (i96) -> i1
        %200 = comb.extract %109 from 83 : (i96) -> i1
        %201 = comb.extract %109 from 84 : (i96) -> i1
        %202 = comb.extract %109 from 85 : (i96) -> i1
        %203 = comb.extract %109 from 86 : (i96) -> i1
        %204 = comb.extract %109 from 87 : (i96) -> i1
        %205 = comb.extract %109 from 88 : (i96) -> i1
        %206 = comb.extract %109 from 89 : (i96) -> i1
        %207 = comb.extract %109 from 90 : (i96) -> i1
        %208 = comb.extract %109 from 91 : (i96) -> i1
        %209 = comb.extract %109 from 92 : (i96) -> i1
        %210 = comb.extract %109 from 93 : (i96) -> i1
        %211 = comb.extract %109 from 94 : (i96) -> i1
        %212 = comb.extract %109 from 95 : (i96) -> i1
        %213 = comb.concat %212, %211, %210, %209, %208, %207, %206, %205, %204, %203, %202, %201, %200, %199, %198, %197 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %214 = hw.array_create %213, %196, %179, %162, %145, %128 : i16
        hw.output %214 : !hw.array<6xi16>
    }
    hw.module @Register_unq2(%I: i8, %CE: i1, %CLK: i1) -> (O: i8) {
        %2 = hw.array_create %I, %0 : i8
        %1 = hw.array_get %2[%CE] : !hw.array<2xi8>, i1
        %3 = sv.reg {name = "reg_P8_inst0"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : i8
        }
        %4 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %3, %4 : i8
        }
        %0 = sv.read_inout %3 : !hw.inout<i8>
        hw.output %0 : i8
    }
    hw.module @complex_register_wrapper(%a: !hw.struct<x: i8, y: i1>, %b: !hw.array<6xi16>, %CLK: i1, %CE: i1, %ASYNCRESET: i1) -> (y: !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>) {
        %0 = hw.instance "Register_inst0" @Register(I: %a: !hw.struct<x: i8, y: i1>, CE: %CE: i1, CLK: %CLK: i1, ASYNCRESET: %ASYNCRESET: i1) -> (O: !hw.struct<x: i8, y: i1>)
        %1 = hw.instance "Register_inst1" @Register_unq1(I: %b: !hw.array<6xi16>, CLK: %CLK: i1) -> (O: !hw.array<6xi16>)
        %2 = hw.struct_create (%0, %1) : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
        %3 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i1>
        %4 = hw.instance "Register_inst2" @Register_unq2(I: %3: i8, CE: %CE: i1, CLK: %CLK: i1) -> (O: i8)
        hw.output %2 : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
    }
}
