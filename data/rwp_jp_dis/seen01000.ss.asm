include ini "resources/seen01000.ini"
include strings "resources/seen01000.strings.txt"

; Start:
0x00000000   LINE 2

#Z00:
LABEL_0:
0x00000005   LINE 5
0x0000000A   OPEN
0x0000000B   PUSH Int 5
0x00000014   PUSH Str 5 ; sys10_mh00
0x0000001D   PUSH Int 4
0x00000026   CALL farcall 1 (Str, Int) ():Int
0x0000003F   POP Int
0x00000044   LINE 5
0x00000049   OPEN
0x0000004A   PUSH Int 5
0x00000053   PUSH Str 6 ; sys10_mh00
0x0000005C   PUSH Int 11
0x00000065   PUSH Int 10
0x0000006E   PUSH Int 10
0x00000077   PUSH Int 0
0x00000080   CALL farcall_with 1 (Str, Int, Int, Int, Int) ():Int
0x000000A5   POP Int
0x000000AA   LINE 5
0x000000AF   OPEN
0x000000B0   PUSH Int 2130706432 ; global var $ax
0x000000B9   PUSH Int 4294967295
0x000000C2   PUSH Int 0
0x000000CB   OPEN
0x000000CC   PUSH Int 5
0x000000D5   PUSH Str 7 ; sys10_mh00
0x000000DE   PUSH Int 12
0x000000E7   PUSH Int 0
0x000000F0   CALL farcall_with 1 (Str, Int, Int) ():Int
0x0000010D   MOV 13 Int 1
0x0000011A   LINE 5
0x0000011F   OPEN
0x00000120   PUSH Int 5
0x00000129   PUSH Str 8 ; sys10_mh00
0x00000132   PUSH Int 15
0x0000013B   PUSH Int 0
0x00000144   CALL farcall_with 1 (Str, Int, Int) ():Int
0x00000161   POP Int
0x00000166   LINE 5
0x0000016B   OPEN
0x0000016C   PUSH Int 5
0x00000175   PUSH Str 9 ; sys10_mh00
0x0000017E   PUSH Int 16
0x00000187   PUSH Int 0
0x00000190   CALL farcall_with 1 (Str, Int, Int) ():Int
0x000001AD   POP Int
0x000001B2   LINE 5
0x000001B7   OPEN
0x000001B8   PUSH Int 5
0x000001C1   PUSH Str 10 ; sys10_mh00
0x000001CA   PUSH Int 1
0x000001D3   PUSH Int 1
0x000001DC   CALL farcall_with 1 (Str, Int, Int) ():Int
0x000001F9   POP Int
0x000001FE   LINE 5
0x00000203   OPEN
0x00000204   PUSH Int 5
0x0000020D   PUSH Str 11 ; sys10_mh00
0x00000216   PUSH Int 3
0x0000021F   CALL farcall 1 (Str, Int) ():Int
0x00000238   POP Int
0x0000023D   LINE 8
0x00000242   OPEN
0x00000243   PUSH Int 32
0x0000024C   PUSH Int 4294967295
0x00000255   PUSH Int 200
0x0000025E   PUSH Int 1
0x00000267   MOV 13 Int 1
0x00000274   LINE 8
0x00000279   OPEN
0x0000027A   PUSH Int 32
0x00000283   PUSH Int 4294967295
0x0000028C   PUSH Int 210
0x00000295   PUSH Int 0
0x0000029E   MOV 13 Int 1
0x000002AB   LINE 8
0x000002B0   OPEN
0x000002B1   PUSH Int 32
0x000002BA   PUSH Int 3
0x000002C3   PUSH Int 4294967295
0x000002CC   PUSH Int 960
0x000002D5   PUSH Int 1
0x000002DE   BEXPR Int Int ADD
0x000002E8   CLOSE
0x000002E9   PUSH Int 0
0x000002F2   BEXPR Int Int EQ
0x000002FC   OPEN
0x000002FD   PUSH Int 32
0x00000306   PUSH Int 5
0x0000030F   PUSH Int 4294967295
0x00000318   PUSH Int 480
0x00000321   PUSH Int 1
0x0000032A   BEXPR Int Int ADD
0x00000334   CLOSE
0x00000335   PUSH Int 0
0x0000033E   BEXPR Int Int LT
0x00000348   BEXPR Int Int OR
0x00000352   JZ LABEL_2
0x00000357   LINE 8
0x0000035C   OPEN
0x0000035D   PUSH Int 32
0x00000366   PUSH Int 4
0x0000036F   PUSH Int 4294967295
0x00000378   PUSH Int 1920
0x00000381   PUSH Int 1
0x0000038A   BEXPR Int Int ADD
0x00000394   PUSH Int 0
0x0000039D   MOV 13 Int 1
0x000003AA   LINE 8
0x000003AF   OPEN
0x000003B0   PUSH Int 32
0x000003B9   PUSH Int 5
0x000003C2   PUSH Int 4294967295
0x000003CB   PUSH Int 480
0x000003D4   PUSH Int 1
0x000003DD   BEXPR Int Int ADD
0x000003E7   CLOSE
0x000003E8   PUSH Int 0
0x000003F1   BEXPR Int Int LT
0x000003FB   JZ LABEL_4
0x00000400   LINE 8
0x00000405   OPEN
0x00000406   PUSH Int 32
0x0000040F   PUSH Int 4
0x00000418   PUSH Int 4294967295
0x00000421   PUSH Int 1920
0x0000042A   PUSH Int 1
0x00000433   BEXPR Int Int ADD
0x0000043D   PUSH Int 2
0x00000446   MOV 13 Int 1
0x00000453   JMP LABEL_3
LABEL_3:
LABEL_4:
0x00000458   LINE 8
0x0000045D   OPEN
0x0000045E   PUSH Int 32
0x00000467   PUSH Int 3
0x00000470   PUSH Int 4294967295
0x00000479   PUSH Int 960
0x00000482   PUSH Int 1
0x0000048B   BEXPR Int Int ADD
0x00000495   CLOSE
0x00000496   PUSH Int 0
0x0000049F   BEXPR Int Int EQ
0x000004A9   JZ LABEL_6
0x000004AE   LINE 8
0x000004B3   OPEN
0x000004B4   PUSH Int 32
0x000004BD   PUSH Int 4
0x000004C6   PUSH Int 4294967295
0x000004CF   PUSH Int 1920
0x000004D8   PUSH Int 1
0x000004E1   BEXPR Int Int ADD
0x000004EB   PUSH Int 1
0x000004F4   MOV 13 Int 1
0x00000501   JMP LABEL_5
LABEL_5:
LABEL_6:
0x00000506   LINE 8
0x0000050B   OPEN
0x0000050C   PUSH Int 32
0x00000515   PUSH Int 3
0x0000051E   PUSH Int 4294967295
0x00000527   PUSH Int 960
0x00000530   PUSH Int 1
0x00000539   BEXPR Int Int ADD
0x00000543   PUSH Int 1
0x0000054C   MOV 13 Int 1
0x00000559   LINE 8
0x0000055E   OPEN
0x0000055F   PUSH Int 32
0x00000568   PUSH Int 5
0x00000571   PUSH Int 4294967295
0x0000057A   PUSH Int 480
0x00000583   PUSH Int 1
0x0000058C   BEXPR Int Int ADD
0x00000596   PUSH Int 0
0x0000059F   MOV 13 Int 1
0x000005AC   LINE 8
0x000005B1   OPEN
0x000005B2   PUSH Int 32
0x000005BB   PUSH Int 3
0x000005C4   PUSH Int 4294967295
0x000005CD   PUSH Int 4800
0x000005D6   PUSH Int 1
0x000005DF   BEXPR Int Int ADD
0x000005E9   PUSH Int 0
0x000005F2   MOV 13 Int 1
0x000005FF   LINE 8
0x00000604   OPEN
0x00000605   PUSH Int 92
0x0000060E   PUSH Int 11
0x00000617   PUSH Str 0 ; ■友達■　ID:
0x00000620   OPEN
0x00000621   PUSH Int 39
0x0000062A   PUSH Int 11
0x00000633   PUSH Int 1
0x0000063C   PUSH Int 3
0x00000645   CALL UNK 0 (Int, Int) ():Str
0x0000065E   BEXPR Str Str ADD
0x00000668   PUSH Str 1 ; 　NO:
0x00000671   BEXPR Str Str ADD
0x0000067B   OPEN
0x0000067C   PUSH Int 39
0x00000685   PUSH Int 1
0x0000068E   PUSH Int 0
0x00000697   CALL UNK 0 (Int) ():Str
0x000006AC   BEXPR Str Str ADD
0x000006B6   CALL UNK 1 (Str) ():Void
0x000006CB   POP Void
0x000006D0   JMP LABEL_1
LABEL_1:
LABEL_2:
0x000006D5   LINE 8
0x000006DA   OPEN
0x000006DB   PUSH Int 5
0x000006E4   PUSH Str 12 ; sys10_mm02
0x000006ED   PUSH Int 38
0x000006F6   CALL farcall 1 (Str, Int) ():Int
0x0000070F   POP Int
0x00000714   LINE 9
0x00000719   OPEN
0x0000071A   PUSH Int 32
0x00000723   PUSH Int 4294967295
0x0000072C   PUSH Int 200
0x00000735   PUSH Int 1
0x0000073E   MOV 13 Int 1
0x0000074B   LINE 9
0x00000750   OPEN
0x00000751   PUSH Int 32
0x0000075A   PUSH Int 4294967295
0x00000763   PUSH Int 210
0x0000076C   PUSH Int 0
0x00000775   MOV 13 Int 1
0x00000782   LINE 9
0x00000787   OPEN
0x00000788   PUSH Int 32
0x00000791   PUSH Int 3
0x0000079A   PUSH Int 4294967295
0x000007A3   PUSH Int 960
0x000007AC   PUSH Int 8
0x000007B5   BEXPR Int Int ADD
0x000007BF   CLOSE
0x000007C0   PUSH Int 0
0x000007C9   BEXPR Int Int EQ
0x000007D3   OPEN
0x000007D4   PUSH Int 32
0x000007DD   PUSH Int 5
0x000007E6   PUSH Int 4294967295
0x000007EF   PUSH Int 480
0x000007F8   PUSH Int 8
0x00000801   BEXPR Int Int ADD
0x0000080B   CLOSE
0x0000080C   PUSH Int 0
0x00000815   BEXPR Int Int LT
0x0000081F   BEXPR Int Int OR
0x00000829   JZ LABEL_8
0x0000082E   LINE 9
0x00000833   OPEN
0x00000834   PUSH Int 32
0x0000083D   PUSH Int 4
0x00000846   PUSH Int 4294967295
0x0000084F   PUSH Int 1920
0x00000858   PUSH Int 8
0x00000861   BEXPR Int Int ADD
0x0000086B   PUSH Int 0
0x00000874   MOV 13 Int 1
0x00000881   LINE 9
0x00000886   OPEN
0x00000887   PUSH Int 32
0x00000890   PUSH Int 5
0x00000899   PUSH Int 4294967295
0x000008A2   PUSH Int 480
0x000008AB   PUSH Int 8
0x000008B4   BEXPR Int Int ADD
0x000008BE   CLOSE
0x000008BF   PUSH Int 0
0x000008C8   BEXPR Int Int LT
0x000008D2   JZ LABEL_10
0x000008D7   LINE 9
0x000008DC   OPEN
0x000008DD   PUSH Int 32
0x000008E6   PUSH Int 4
0x000008EF   PUSH Int 4294967295
0x000008F8   PUSH Int 1920
0x00000901   PUSH Int 8
0x0000090A   BEXPR Int Int ADD
0x00000914   PUSH Int 2
0x0000091D   MOV 13 Int 1
0x0000092A   JMP LABEL_9
LABEL_9:
LABEL_10:
0x0000092F   LINE 9
0x00000934   OPEN
0x00000935   PUSH Int 32
0x0000093E   PUSH Int 3
0x00000947   PUSH Int 4294967295
0x00000950   PUSH Int 960
0x00000959   PUSH Int 8
0x00000962   BEXPR Int Int ADD
0x0000096C   CLOSE
0x0000096D   PUSH Int 0
0x00000976   BEXPR Int Int EQ
0x00000980   JZ LABEL_12
0x00000985   LINE 9
0x0000098A   OPEN
0x0000098B   PUSH Int 32
0x00000994   PUSH Int 4
0x0000099D   PUSH Int 4294967295
0x000009A6   PUSH Int 1920
0x000009AF   PUSH Int 8
0x000009B8   BEXPR Int Int ADD
0x000009C2   PUSH Int 1
0x000009CB   MOV 13 Int 1
0x000009D8   JMP LABEL_11
LABEL_11:
LABEL_12:
0x000009DD   LINE 9
0x000009E2   OPEN
0x000009E3   PUSH Int 32
0x000009EC   PUSH Int 3
0x000009F5   PUSH Int 4294967295
0x000009FE   PUSH Int 960
0x00000A07   PUSH Int 8
0x00000A10   BEXPR Int Int ADD
0x00000A1A   PUSH Int 1
0x00000A23   MOV 13 Int 1
0x00000A30   LINE 9
0x00000A35   OPEN
0x00000A36   PUSH Int 32
0x00000A3F   PUSH Int 5
0x00000A48   PUSH Int 4294967295
0x00000A51   PUSH Int 480
0x00000A5A   PUSH Int 8
0x00000A63   BEXPR Int Int ADD
0x00000A6D   PUSH Int 0
0x00000A76   MOV 13 Int 1
0x00000A83   LINE 9
0x00000A88   OPEN
0x00000A89   PUSH Int 32
0x00000A92   PUSH Int 3
0x00000A9B   PUSH Int 4294967295
0x00000AA4   PUSH Int 4800
0x00000AAD   PUSH Int 8
0x00000AB6   BEXPR Int Int ADD
0x00000AC0   PUSH Int 0
0x00000AC9   MOV 13 Int 1
0x00000AD6   LINE 9
0x00000ADB   OPEN
0x00000ADC   PUSH Int 92
0x00000AE5   PUSH Int 11
0x00000AEE   PUSH Str 2 ; ■友達■　ID:
0x00000AF7   OPEN
0x00000AF8   PUSH Int 39
0x00000B01   PUSH Int 11
0x00000B0A   PUSH Int 8
0x00000B13   PUSH Int 3
0x00000B1C   CALL UNK 0 (Int, Int) ():Str
0x00000B35   BEXPR Str Str ADD
0x00000B3F   PUSH Str 3 ; 　NO:
0x00000B48   BEXPR Str Str ADD
0x00000B52   OPEN
0x00000B53   PUSH Int 39
0x00000B5C   PUSH Int 1
0x00000B65   PUSH Int 0
0x00000B6E   CALL UNK 0 (Int) ():Str
0x00000B83   BEXPR Str Str ADD
0x00000B8D   CALL UNK 1 (Str) ():Void
0x00000BA2   POP Void
0x00000BA7   JMP LABEL_7
LABEL_7:
LABEL_8:
0x00000BAC   LINE 9
0x00000BB1   OPEN
0x00000BB2   PUSH Int 5
0x00000BBB   PUSH Str 13 ; sys10_mm02
0x00000BC4   PUSH Int 38
0x00000BCD   CALL farcall 1 (Str, Int) ():Int
0x00000BE6   POP Int
0x00000BEB   LINE 13
0x00000BF0   OPEN
0x00000BF1   PUSH Int 5
0x00000BFA   PUSH Str 14 ; sys50_ef00_ev10
0x00000C03   PUSH Int 0
0x00000C0C   CALL farcall 1 (Str, Int) ():Int
0x00000C25   POP Int
0x00000C2A   LINE 78
0x00000C2F   OPEN
0x00000C30   PUSH Int 4
0x00000C39   PUSH Str 15 ; seen01001
0x00000C42   CALL jump_sce 0 (Str) ():Void
0x00000C57   POP Void
0x00000C5C   LINE 79
0x00000C61   END