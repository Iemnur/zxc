include ini "resources/sys10_su00.ini"
include strings "resources/sys10_su00.strings.txt"

; Start:
0x00000000   LINE 16

#Z00:
LABEL_0:
0x00000005   ;LINE 27
0x0000000A   ;OPEN
0x0000000B   ;PUSH Int 92
0x00000014   ;PUSH Int 2
0x0000001D   ;PUSH Str 0 ; dummy
0x00000026   ;PUSH Int 76
0x0000002F   ;PUSH Str 1 ; R9n1QJLP
0x00000038   ;CALL func_system.disc_check 0 (Str, Int, Str) ():Void
0x00000055   ;POP Void
0x0000005A   LINE 30
0x0000005F   OPEN
0x00000060   PUSH Int 31
0x00000069   PUSH Int 4294967295
0x00000072   PUSH Int 1000
0x0000007B   CLOSE
0x0000007C   PUSH Int 0
0x00000085   BEXPR Int Int EQ
0x0000008F   JZ LABEL_2
0x00000094   LINE 31
0x00000099   OPEN
0x0000009A   PUSH Int 31
0x000000A3   PUSH Int 4294967295
0x000000AC   PUSH Int 1000
0x000000B5   PUSH Int 1
0x000000BE   MOV 13 Int 1
0x000000CB   LINE 33
0x000000D0   PUSH Int 1
0x000000D9   JZ LABEL_4
0x000000DE   LINE 35
0x000000E3   OPEN
0x000000E4   PUSH Int 5
0x000000ED   PUSH Str 3 ; sys10_ginit00
0x000000F6   PUSH Int 0
0x000000FF   CALL farcall 1 (Str, Int) ():Int
0x00000118   POP Int
0x0000011D   JMP LABEL_3
LABEL_3:
LABEL_4:
0x00000122   LINE 38
0x00000127   PUSH Int 1
0x00000130   JZ LABEL_6
0x00000135   LINE 40
0x0000013A   OPEN
0x0000013B   PUSH Int 5
0x00000144   PUSH Str 4 ; sys40_mp00
0x0000014D   PUSH Int 0
0x00000156   CALL farcall 1 (Str, Int) ():Int
0x0000016F   POP Int
0x00000174   JMP LABEL_5
LABEL_5:
LABEL_6:
0x00000179   LINE 43
0x0000017E   PUSH Int 1
0x00000187   JZ LABEL_8
0x0000018C   LINE 45
0x00000191   OPEN
0x00000192   PUSH Int 5
0x0000019B   PUSH Str 5 ; sys50_ef00_ginit00
0x000001A4   PUSH Int 0
0x000001AD   CALL farcall 1 (Str, Int) ():Int
0x000001C6   POP Int
0x000001CB   JMP LABEL_7
LABEL_7:
LABEL_8:
0x000001D0   JMP LABEL_1
LABEL_1:
LABEL_2:
0x000001D5   LINE 50
0x000001DA   PUSH Int 1
0x000001E3   JZ LABEL_10
0x000001E8   LINE 52
0x000001ED   PUSH Int 1
0x000001F6   JZ LABEL_12
0x000001FB   LINE 54
0x00000200   OPEN
0x00000201   PUSH Int 5
0x0000020A   PUSH Str 6 ; sys10_ginit00
0x00000213   PUSH Int 1
0x0000021C   CALL farcall 1 (Str, Int) ():Int
0x00000235   POP Int
0x0000023A   JMP LABEL_11
LABEL_11:
LABEL_12:
0x0000023F   JMP LABEL_9
LABEL_9:
LABEL_10:
0x00000244   LINE 59
0x00000249   OPEN
0x0000024A   PUSH Int 4
0x00000253   PUSH Str 7 ; sys10_tt00
0x0000025C   CALL jump_sce 0 (Str) ():Void
0x00000271   POP Void
0x00000276   LINE 61
0x0000027B   RET ()

0x00000280   LINE 62
0x00000285   END