include ini "resources/seen01001.ini"
include strings "resources/seen01001.strings.txt"
include macro "macros/mcr.asm"

; Start:
0x00000000   LINE 2

#Z00:
LABEL_0:
0x00000005   LINE 7
0x0000000A   OPEN
0x0000000B   PUSH Int 42
0x00000014   PUSH Int 0
0x0000001D   PUSH Str 57 ; bgm034
0x00000026   CALL sound_bgm.play 0 (Str) ():Void
0x0000003B   POP Void
0x00000040   LINE 8
0x00000045   OPEN
0x00000046   PUSH Int 6
0x0000004F   CALL UNK 0 () ():Void
0x00000060   POP Void
0x00000065   LINE 9
0x0000006A   OPEN
0x0000006B   PUSH Int 5
0x00000074   PUSH Str 58 ; sys20_adv00
0x0000007D   PUSH Int 1
0x00000086   PUSH Int 0
0x0000008F   PUSH Str 59 ; bg003
0x00000098   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x000000B9   POP Int
0x000000BE   LINE 10
0x000000C3   OPEN
0x000000C4   PUSH Int 6
0x000000CD   CALL UNK 0 () ():Void
0x000000DE   POP Void
0x000000E3   LINE 11
0x000000E8   OPEN
0x000000E9   PUSH Int 5
0x000000F2   PUSH Str 60 ; sys20_adv00
0x000000FB   PUSH Int 17
0x00000104   PUSH Int 0
0x0000010D   PUSH Int 0
0x00000116   PUSH Str 61 ; cgm_ys15
0x0000011F   PUSH Int 2147483647
0x00000128   PUSH Int 2147483647
0x00000131   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x0000015E   POP Int
0x00000163   LINE 12
0x00000168   OPEN
0x00000169   PUSH Int 6
0x00000172   CALL UNK 0 () ():Void
0x00000183   POP Void
0x00000188   LINE 13
0x0000018D   OPEN
0x0000018E   PUSH Int 84
0x00000197   CALL refresh 0 () ():Void
0x000001A8   OPEN
0x000001A9   PUSH Int 18
0x000001B2   PUSH Int 100100011
0x000001BB   PUSH Int 6
0x000001C4   CALL Koe 1 (Int, Int) ():Void 0
0x000001E1   POP Void
0x000001E6   LINE 13
0x000001EB   OPEN
0x000001EC   PUSH Int 84
0x000001F5   CALL refresh 0 () ():Void
0x00000206   PUSH Str 0 ; 吉野＿体験版
0x0000020F   NAME
0x00000210   LINE 13
0x00000215   OPEN
0x00000216   PUSH Int 84
0x0000021F   CALL refresh 0 () ():Void
0x00000230   PUSH Str 1 ; 「もういい加減、我慢ならねぇ…」
0x00000239   TEXT 1
0x0000023E   LINE 13
0x00000243   OPEN
0x00000244   PUSH Int 14
0x0000024D   CALL Pause 0 () ():Void
0x0000025E   POP Void
0x00000263   LINE 15
0x00000268   OPEN
0x00000269   PUSH Int 84
0x00000272   CALL refresh 0 () ():Void
0x00000283   PUSH Str 2 ; うちのクラス唯一の不良とも言える男、吉野晴彦が言った。
0x0000028C   TEXT 2
0x00000291   LINE 15
0x00000296   OPEN
0x00000297   PUSH Int 14
0x000002A0   CALL Pause 0 () ():Void
0x000002B1   POP Void
0x000002B6   LINE 17
0x000002BB   OPEN
0x000002BC   PUSH Int 5
0x000002C5   PUSH Str 62 ; sys20_adv00
0x000002CE   PUSH Int 17
0x000002D7   PUSH Int 0
0x000002E0   PUSH Int 0
0x000002E9   PUSH Str 63 ; cgm_ys19
0x000002F2   PUSH Int 2147483647
0x000002FB   PUSH Int 2147483647
0x00000304   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x00000331   POP Int
0x00000336   LINE 18
0x0000033B   OPEN
0x0000033C   PUSH Int 84
0x00000345   CALL refresh 0 () ():Void
0x00000356   OPEN
0x00000357   PUSH Int 18
0x00000360   PUSH Int 100100016
0x00000369   PUSH Int 6
0x00000372   CALL Koe 1 (Int, Int) ():Void 3
0x0000038F   POP Void
0x00000394   LINE 18
0x00000399   OPEN
0x0000039A   PUSH Int 84
0x000003A3   CALL refresh 0 () ():Void
0x000003B4   PUSH Str 3 ; 吉野＿体験版
0x000003BD   NAME
0x000003BE   LINE 18
0x000003C3   OPEN
0x000003C4   PUSH Int 84
0x000003CD   CALL refresh 0 () ():Void
0x000003DE   PUSH Str 4 ; 「天王寺、オレとデュエルしろ」
0x000003E7   TEXT 4
0x000003EC   LINE 18
0x000003F1   OPEN
0x000003F2   PUSH Int 14
0x000003FB   CALL Pause 0 () ():Void
0x0000040C   POP Void
0x00000411   LINE 19
0x00000416   OPEN
0x00000417   PUSH Int 84
0x00000420   CALL refresh 0 () ():Void
0x00000431   PUSH Str 5 ; 瑚太朗＿体験版
0x0000043A   NAME
0x0000043B   LINE 19
0x00000440   OPEN
0x00000441   PUSH Int 84
0x0000044A   CALL refresh 0 () ():Void
0x0000045B   PUSH Str 6 ; 「悪い吉野、俺カードゲームとかさっぱりで…」
0x00000464   TEXT 5
0x00000469   LINE 19
0x0000046E   OPEN
0x0000046F   PUSH Int 14
0x00000478   CALL Pause 0 () ():Void
0x00000489   POP Void
0x0000048E   LINE 21
0x00000493   OPEN
0x00000494   PUSH Int 5
0x0000049D   PUSH Str 64 ; sys20_adv00
0x000004A6   PUSH Int 17
0x000004AF   PUSH Int 0
0x000004B8   PUSH Int 0
0x000004C1   PUSH Str 65 ; cgm_ys20
0x000004CA   PUSH Int 2147483647
0x000004D3   PUSH Int 2147483647
0x000004DC   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x00000509   POP Int
0x0000050E   LINE 22
0x00000513   OPEN
0x00000514   PUSH Int 84
0x0000051D   CALL refresh 0 () ():Void
0x0000052E   OPEN
0x0000052F   PUSH Int 18
0x00000538   PUSH Int 100100020
0x00000541   PUSH Int 6
0x0000054A   CALL Koe 1 (Int, Int) ():Void 6
0x00000567   POP Void
0x0000056C   LINE 22
0x00000571   OPEN
0x00000572   PUSH Int 84
0x0000057B   CALL refresh 0 () ():Void
0x0000058C   PUSH Str 7 ; 吉野＿体験版
0x00000595   NAME
0x00000596   LINE 22
0x0000059B   OPEN
0x0000059C   PUSH Int 84
0x000005A5   CALL refresh 0 () ():Void
0x000005B6   PUSH Str 8 ; 「決闘って意味で使った！」
0x000005BF   TEXT 7
0x000005C4   LINE 22
0x000005C9   OPEN
0x000005CA   PUSH Int 14
0x000005D3   CALL Pause 0 () ():Void
0x000005E4   POP Void
0x000005E9   LINE 24
0x000005EE   OPEN
0x000005EF   PUSH Int 5
0x000005F8   PUSH Str 66 ; sys20_adv00
0x00000601   PUSH Int 17
0x0000060A   PUSH Int 0
0x00000613   PUSH Int 0
0x0000061C   PUSH Str 67 ; cgm_ys19
0x00000625   PUSH Int 2147483647
0x0000062E   PUSH Int 2147483647
0x00000637   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x00000664   POP Int
0x00000669   LINE 25
0x0000066E   OPEN
0x0000066F   PUSH Int 84
0x00000678   CALL refresh 0 () ():Void
0x00000689   PUSH Str 9 ; 本気の眼だった。
0x00000692   TEXT 8
0x00000697   LINE 25
0x0000069C   OPEN
0x0000069D   PUSH Int 14
0x000006A6   CALL Pause 0 () ():Void
0x000006B7   POP Void
0x000006BC   LINE 27
0x000006C1   OPEN
0x000006C2   PUSH Int 84
0x000006CB   CALL refresh 0 () ():Void
0x000006DC   PUSH Str 10 ; 見た目通りの一匹狼だが、普段はクールだ。
0x000006E5   TEXT 9
0x000006EA   LINE 27
0x000006EF   OPEN
0x000006F0   PUSH Int 14
0x000006F9   CALL Pause 0 () ():Void
0x0000070A   POP Void
0x0000070F   LINE 28
0x00000714   OPEN
0x00000715   PUSH Int 84
0x0000071E   CALL refresh 0 () ():Void
0x0000072F   PUSH Str 11 ; だから吉野が、漫画やゲームに出てくるようなキザな口調で話すことを知っている者は、意外に少ない。
0x00000738   TEXT 10
0x0000073D   LINE 28
0x00000742   OPEN
0x00000743   PUSH Int 14
0x0000074C   CALL Pause 0 () ():Void
0x0000075D   POP Void
0x00000762   LINE 29
0x00000767   OPEN
0x00000768   PUSH Int 84
0x00000771   CALL refresh 0 () ():Void
0x00000782   PUSH Str 12 ; こいつは、なぜだか俺を目の敵にしている。
0x0000078B   TEXT 11
0x00000790   LINE 29
0x00000795   OPEN
0x00000796   PUSH Int 14
0x0000079F   CALL Pause 0 () ():Void
0x000007B0   POP Void
0x000007B5   LINE 30
0x000007BA   OPEN
0x000007BB   PUSH Int 84
0x000007C4   CALL refresh 0 () ():Void
0x000007D5   PUSH Str 13 ; 今まで対決は避けてきたが、とうとうこういうことになってしまった。
0x000007DE   TEXT 12
0x000007E3   LINE 30
0x000007E8   OPEN
0x000007E9   PUSH Int 14
0x000007F2   CALL Pause 0 () ():Void
0x00000803   POP Void
0x00000808   LINE 31
0x0000080D   OPEN
0x0000080E   PUSH Int 84
0x00000817   CALL refresh 0 () ():Void
0x00000828   PUSH Str 14 ; 俺は休み時間ごとにヤツに気さくに話しかけ、
0x00000831   TEXT 13
0x00000836   LINE 31
0x0000083B   OPEN
0x0000083C   PUSH Int 13
0x00000845   CALL AppendWin 0 () ():Void
0x00000856   POP Void
0x0000085B   LINE 31
0x00000860   OPEN
0x00000861   PUSH Int 84
0x0000086A   CALL refresh 0 () ():Void
0x0000087B   PUSH Str 15 ; 便所に行けばついていって後ろからのぞき込み、
0x00000884   TEXT 14
0x00000889   LINE 31
0x0000088E   OPEN
0x0000088F   PUSH Int 14
0x00000898   CALL Pause 0 () ():Void
0x000008A9   POP Void
0x000008AE   LINE 32
0x000008B3   OPEN
0x000008B4   PUSH Int 84
0x000008BD   CALL refresh 0 () ():Void
0x000008CE   PUSH Str 16 ; いちいち格好良すぎる言葉づかいに爆笑することで親しみを示し、
0x000008D7   TEXT 15
0x000008DC   LINE 32
0x000008E1   OPEN
0x000008E2   PUSH Int 13
0x000008EB   CALL AppendWin 0 () ():Void
0x000008FC   POP Void
0x00000901   LINE 32
0x00000906   OPEN
0x00000907   PUSH Int 84
0x00000910   CALL refresh 0 () ():Void
0x00000921   PUSH Str 17 ; ひざかっくんなどの友情表現を絶やすことはなかったのに。
0x0000092A   TEXT 16
0x0000092F   LINE 32
0x00000934   OPEN
0x00000935   PUSH Int 14
0x0000093E   CALL Pause 0 () ():Void
0x0000094F   POP Void
0x00000954   LINE 33
0x00000959   OPEN
0x0000095A   PUSH Int 84
0x00000963   CALL refresh 0 () ():Void
0x00000974   PUSH Str 18 ; なぜ吉野が俺を鬱陶しがるか、想像もつかないのが正直なところだ。
0x0000097D   TEXT 17
0x00000982   LINE 33
0x00000987   OPEN
0x00000988   PUSH Int 14
0x00000991   CALL Pause 0 () ():Void
0x000009A2   POP Void
0x000009A7   LINE 35
0x000009AC   OPEN
0x000009AD   PUSH Int 84
0x000009B6   CALL refresh 0 () ():Void
0x000009C7   PUSH Str 19 ; 瑚太朗＿体験版
0x000009D0   NAME
0x000009D1   LINE 35
0x000009D6   OPEN
0x000009D7   PUSH Int 84
0x000009E0   CALL refresh 0 () ():Void
0x000009F1   PUSH Str 20 ; 「残念だよ吉野…親友同士で争うことになるなんてな」
0x000009FA   TEXT 18
0x000009FF   LINE 35
0x00000A04   OPEN
0x00000A05   PUSH Int 14
0x00000A0E   CALL Pause 0 () ():Void
0x00000A1F   POP Void
0x00000A24   LINE 37
0x00000A29   OPEN
0x00000A2A   PUSH Int 5
0x00000A33   PUSH Str 68 ; sys20_adv00
0x00000A3C   PUSH Int 17
0x00000A45   PUSH Int 0
0x00000A4E   PUSH Int 0
0x00000A57   PUSH Str 69 ; cgm_ys20
0x00000A60   PUSH Int 2147483647
0x00000A69   PUSH Int 2147483647
0x00000A72   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x00000A9F   POP Int
0x00000AA4   LINE 38
0x00000AA9   OPEN
0x00000AAA   PUSH Int 84
0x00000AB3   CALL refresh 0 () ():Void
0x00000AC4   OPEN
0x00000AC5   PUSH Int 18
0x00000ACE   PUSH Int 100100036
0x00000AD7   PUSH Int 6
0x00000AE0   CALL Koe 1 (Int, Int) ():Void 19
0x00000AFD   POP Void
0x00000B02   LINE 38
0x00000B07   OPEN
0x00000B08   PUSH Int 84
0x00000B11   CALL refresh 0 () ():Void
0x00000B22   PUSH Str 21 ; 吉野＿体験版
0x00000B2B   NAME
0x00000B2C   LINE 38
0x00000B31   OPEN
0x00000B32   PUSH Int 84
0x00000B3B   CALL refresh 0 () ():Void
0x00000B4C   PUSH Str 22 ; 「テメェと親友になったつもりはねぇっ！　そいつを今日、体に理解させてやる」
0x00000B55   TEXT 20
0x00000B5A   LINE 38
0x00000B5F   OPEN
0x00000B60   PUSH Int 14
0x00000B69   CALL Pause 0 () ():Void
0x00000B7A   POP Void
0x00000B7F   LINE 39
0x00000B84   OPEN
0x00000B85   PUSH Int 84
0x00000B8E   CALL refresh 0 () ():Void
0x00000B9F   PUSH Str 23 ; 瑚太朗＿体験版
0x00000BA8   NAME
0x00000BA9   LINE 39
0x00000BAE   OPEN
0x00000BAF   PUSH Int 84
0x00000BB8   CALL refresh 0 () ():Void
0x00000BC9   PUSH Str 24 ; 「どうやら本気みたいだな」
0x00000BD2   TEXT 21
0x00000BD7   LINE 39
0x00000BDC   OPEN
0x00000BDD   PUSH Int 14
0x00000BE6   CALL Pause 0 () ():Void
0x00000BF7   POP Void
0x00000BFC   LINE 40
0x00000C01   OPEN
0x00000C02   PUSH Int 84
0x00000C0B   CALL refresh 0 () ():Void
0x00000C1C   PUSH Str 25 ; 瑚太朗＿体験版
0x00000C25   NAME
0x00000C26   LINE 40
0x00000C2B   OPEN
0x00000C2C   PUSH Int 84
0x00000C35   CALL refresh 0 () ():Void
0x00000C46   PUSH Str 26 ; 「…わかった。受けて立つ」
0x00000C4F   TEXT 22
0x00000C54   LINE 40
0x00000C59   OPEN
0x00000C5A   PUSH Int 14
0x00000C63   CALL Pause 0 () ():Void
0x00000C74   POP Void
0x00000C79   LINE 42
0x00000C7E   OPEN
0x00000C7F   PUSH Int 5
0x00000C88   PUSH Str 70 ; sys20_adv00
0x00000C91   PUSH Int 17
0x00000C9A   PUSH Int 0
0x00000CA3   PUSH Int 0
0x00000CAC   PUSH Str 71 ; cgm_ys17
0x00000CB5   PUSH Int 2147483647
0x00000CBE   PUSH Int 2147483647
0x00000CC7   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x00000CF4   POP Int
0x00000CF9   LINE 43
0x00000CFE   OPEN
0x00000CFF   PUSH Int 84
0x00000D08   CALL refresh 0 () ():Void
0x00000D19   OPEN
0x00000D1A   PUSH Int 18
0x00000D23   PUSH Int 100100041
0x00000D2C   PUSH Int 6
0x00000D35   CALL Koe 1 (Int, Int) ():Void 23
0x00000D52   POP Void
0x00000D57   LINE 43
0x00000D5C   OPEN
0x00000D5D   PUSH Int 84
0x00000D66   CALL refresh 0 () ():Void
0x00000D77   PUSH Str 27 ; 吉野＿体験版
0x00000D80   NAME
0x00000D81   LINE 43
0x00000D86   OPEN
0x00000D87   PUSH Int 84
0x00000D90   CALL refresh 0 () ():Void
0x00000DA1   PUSH Str 28 ; 「放課後、校舎裏に来い。そこでジ・エンド、くれてやる」
0x00000DAA   TEXT 24
0x00000DAF   LINE 43
0x00000DB4   OPEN
0x00000DB5   PUSH Int 14
0x00000DBE   CALL Pause 0 () ():Void
0x00000DCF   POP Void
0x00000DD4   LINE 44
0x00000DD9   OPEN
0x00000DDA   PUSH Int 84
0x00000DE3   CALL refresh 0 () ():Void
0x00000DF4   PUSH Str 29 ; 瑚太朗＿体験版
0x00000DFD   NAME
0x00000DFE   LINE 44
0x00000E03   OPEN
0x00000E04   PUSH Int 84
0x00000E0D   CALL refresh 0 () ():Void
0x00000E1E   PUSH Str 30 ; 「ああ…だがひとつだけ言っておく」
0x00000E27   TEXT 25
0x00000E2C   LINE 44
0x00000E31   OPEN
0x00000E32   PUSH Int 14
0x00000E3B   CALL Pause 0 () ():Void
0x00000E4C   POP Void
0x00000E51   LINE 46
0x00000E56   OPEN
0x00000E57   PUSH Int 84
0x00000E60   CALL refresh 0 () ():Void
0x00000E71   PUSH Str 31 ; 吉野の波動にあてられた俺は、ニヒルな気分になって言う。
0x00000E7A   TEXT 26
0x00000E7F   LINE 46
0x00000E84   OPEN
0x00000E85   PUSH Int 14
0x00000E8E   CALL Pause 0 () ():Void
0x00000E9F   POP Void
0x00000EA4   LINE 48
0x00000EA9   OPEN
0x00000EAA   PUSH Int 5
0x00000EB3   PUSH Str 72 ; sys20_adv00
0x00000EBC   PUSH Int 17
0x00000EC5   PUSH Int 0
0x00000ECE   PUSH Int 0
0x00000ED7   PUSH Str 73 ; cgm_ys10
0x00000EE0   PUSH Int 2147483647
0x00000EE9   PUSH Int 2147483647
0x00000EF2   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x00000F1F   POP Int
0x00000F24   LINE 49
0x00000F29   OPEN
0x00000F2A   PUSH Int 84
0x00000F33   CALL refresh 0 () ():Void
0x00000F44   OPEN
0x00000F45   PUSH Int 18
0x00000F4E   PUSH Int 100100047
0x00000F57   PUSH Int 6
0x00000F60   CALL Koe 1 (Int, Int) ():Void 27
0x00000F7D   POP Void
0x00000F82   LINE 49
0x00000F87   OPEN
0x00000F88   PUSH Int 84
0x00000F91   CALL refresh 0 () ():Void
0x00000FA2   PUSH Str 32 ; 吉野＿体験版
0x00000FAB   NAME
0x00000FAC   LINE 49
0x00000FB1   OPEN
0x00000FB2   PUSH Int 84
0x00000FBB   CALL refresh 0 () ():Void
0x00000FCC   PUSH Str 33 ; 「なんだ？」
0x00000FD5   TEXT 28
0x00000FDA   LINE 49
0x00000FDF   OPEN
0x00000FE0   PUSH Int 14
0x00000FE9   CALL Pause 0 () ():Void
0x00000FFA   POP Void
0x00000FFF   LINE 50
0x00001004   OPEN
0x00001005   PUSH Int 84
0x0000100E   CALL refresh 0 () ():Void
0x0000101F   PUSH Str 34 ; 瑚太朗＿体験版
0x00001028   NAME
0x00001029   LINE 50
0x0000102E   OPEN
0x0000102F   PUSH Int 84
0x00001038   CALL refresh 0 () ():Void
0x00001049   PUSH Str 35 ; 「俺はそう簡単に終わる男じゃない」
0x00001052   TEXT 29
0x00001057   LINE 50
0x0000105C   OPEN
0x0000105D   PUSH Int 14
0x00001066   CALL Pause 0 () ():Void
0x00001077   POP Void
0x0000107C   LINE 52
0x00001081   OPEN
0x00001082   PUSH Int 5
0x0000108B   PUSH Str 74 ; sys20_adv00
0x00001094   PUSH Int 17
0x0000109D   PUSH Int 0
0x000010A6   PUSH Int 0
0x000010AF   PUSH Str 75 ; cgm_ys12
0x000010B8   PUSH Int 2147483647
0x000010C1   PUSH Int 2147483647
0x000010CA   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x000010F7   POP Int
0x000010FC   LINE 53
0x00001101   OPEN
0x00001102   PUSH Int 84
0x0000110B   CALL refresh 0 () ():Void
0x0000111C   OPEN
0x0000111D   PUSH Int 18
0x00001126   PUSH Int 100100051
0x0000112F   PUSH Int 6
0x00001138   CALL Koe 1 (Int, Int) ():Void 30
0x00001155   POP Void
0x0000115A   LINE 53
0x0000115F   OPEN
0x00001160   PUSH Int 84
0x00001169   CALL refresh 0 () ():Void
0x0000117A   PUSH Str 36 ; 吉野＿体験版
0x00001183   NAME
0x00001184   LINE 53
0x00001189   OPEN
0x0000118A   PUSH Int 84
0x00001193   CALL refresh 0 () ():Void
0x000011A4   PUSH Str 37 ; 「上等だ。そんなテメェの吠え面、見物だな」
0x000011AD   TEXT 31
0x000011B2   LINE 53
0x000011B7   OPEN
0x000011B8   PUSH Int 14
0x000011C1   CALL Pause 0 () ():Void
0x000011D2   POP Void
0x000011D7   LINE 55
0x000011DC   OPEN
0x000011DD   PUSH Int 5
0x000011E6   PUSH Str 76 ; sys20_adv00
0x000011EF   PUSH Int 17
0x000011F8   PUSH Int 0
0x00001201   PUSH Int 0
0x0000120A   PUSH Str 77 ; cgm_ys19
0x00001213   PUSH Int 2147483647
0x0000121C   PUSH Int 2147483647
0x00001225   CALL farcall.cg0 1 (Str, Int, Int, Int, Str, Int, Int) ():Int
0x00001252   POP Int
0x00001257   LINE 56
0x0000125C   OPEN
0x0000125D   PUSH Int 84
0x00001266   CALL refresh 0 () ():Void
0x00001277   OPEN
0x00001278   PUSH Int 18
0x00001281   PUSH Int 100100054
0x0000128A   PUSH Int 6
0x00001293   CALL Koe 1 (Int, Int) ():Void 32
0x000012B0   POP Void
0x000012B5   LINE 56
0x000012BA   OPEN
0x000012BB   PUSH Int 84
0x000012C4   CALL refresh 0 () ():Void
0x000012D5   PUSH Str 38 ; 吉野＿体験版
0x000012DE   NAME
0x000012DF   LINE 56
0x000012E4   OPEN
0x000012E5   PUSH Int 84
0x000012EE   CALL refresh 0 () ():Void
0x000012FF   PUSH Str 39 ; 「…放課後だ。忘れるんじゃねぇぞ」
0x00001308   TEXT 33
0x0000130D   LINE 56
0x00001312   OPEN
0x00001313   PUSH Int 14
0x0000131C   CALL Pause 0 () ():Void
0x0000132D   POP Void
0x00001332   LINE 57
0x00001337   OPEN
0x00001338   PUSH Int 84
0x00001341   CALL refresh 0 () ():Void
0x00001352   PUSH Str 40 ; 瑚太朗＿体験版
0x0000135B   NAME
0x0000135C   LINE 57
0x00001361   OPEN
0x00001362   PUSH Int 84
0x0000136B   CALL refresh 0 () ():Void
0x0000137C   PUSH Str 41 ; 「ああ、理解（わか）っている」
0x00001385   TEXT 34
0x0000138A   LINE 57
0x0000138F   OPEN
0x00001390   PUSH Int 14
0x00001399   CALL Pause 0 () ():Void
0x000013AA   POP Void
0x000013AF   LINE 59
0x000013B4   OPEN
0x000013B5   PUSH Int 5
0x000013BE   PUSH Str 78 ; sys20_adv00
0x000013C7   PUSH Int 17
0x000013D0   PUSH Int 0
0x000013D9   PUSH Int 0
0x000013E2   PUSH Int 2147483647
0x000013EB   PUSH Int 2147483647
0x000013F4   PUSH Int 2147483647
0x000013FD   CALL farcall_with 1 (Str, Int, Int, Int, Int, Int, Int) ():Int
0x0000142A   POP Int
0x0000142F   LINE 60
0x00001434   OPEN
0x00001435   PUSH Int 84
0x0000143E   CALL refresh 0 () ():Void
0x0000144F   PUSH Str 42 ; 狂犬とまで呼ばれる吉野との、熱い、火花散る約束。
0x00001458   TEXT 35
0x0000145D   LINE 60
0x00001462   OPEN
0x00001463   PUSH Int 14
0x0000146C   CALL Pause 0 () ():Void
0x0000147D   POP Void
0x00001482   LINE 62
0x00001487   OPEN
0x00001488   PUSH Int 42
0x00001491   PUSH Int 4
0x0000149A   PUSH Int 3000
0x000014A3   CALL sound_bgm.stop_timer 1 (Int) ():Void
0x000014B8   POP Void
0x000014BD   LINE 64
0x000014C2   OPEN
0x000014C3   PUSH Int 54
0x000014CC   PUSH Int 2000
0x000014D5   CALL TIMEWAIT 0 (Int) ():Void
0x000014EA   POP Void
0x000014EF   LINE 66
0x000014F4   OPEN
0x000014F5   PUSH Int 5
0x000014FE   PUSH Str 79 ; sys20_adv00
0x00001507   PUSH Int 1
0x00001510   PUSH Int 4
0x00001519   PUSH Str 80 ; kuro
0x00001522   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x00001543   POP Int
0x00001548   LINE 68
0x0000154D   OPEN
0x0000154E   PUSH Int 84
0x00001557   CALL refresh 0 () ():Void
0x00001568   PUSH Str 43 ; その約束をあっさり忘れて、放課後まっすぐ帰宅した。
0x00001571   TEXT 36
0x00001576   LINE 68
0x0000157B   OPEN
0x0000157C   PUSH Int 14
0x00001585   CALL Pause 0 () ():Void
0x00001596   POP Void
0x0000159B   LINE 69
0x000015A0   OPEN
0x000015A1   PUSH Int 84
0x000015AA   CALL refresh 0 () ():Void
0x000015BB   PUSH Str 44 ; 俺はあまりにもいい加減な男だった。
0x000015C4   TEXT 37
0x000015C9   LINE 69
0x000015CE   OPEN
0x000015CF   PUSH Int 14
0x000015D8   CALL Pause 0 () ():Void
0x000015E9   POP Void
0x000015EE   LINE 71
0x000015F3   OPEN
0x000015F4   PUSH Int 5
0x000015FD   PUSH Str 81 ; sys20_adv00
0x00001606   PUSH Int 1
0x0000160F   PUSH Int 20
0x00001618   PUSH Str 82 ; bg001n1
0x00001621   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x00001642   POP Int
0x00001647   LINE 72
0x0000164C   OPEN
0x0000164D   PUSH Int 42
0x00001656   PUSH Int 0
0x0000165F   PUSH Str 83 ; bgm013
0x00001668   CALL sound_bgm.play 0 (Str) ():Void
0x0000167D   POP Void
0x00001682   LINE 75
0x00001687   OPEN
0x00001688   PUSH Int 84
0x00001691   CALL refresh 0 () ():Void
0x000016A2   PUSH Str 45 ; 瑚太朗＿体験版
0x000016AB   NAME
0x000016AC   LINE 75
0x000016B1   OPEN
0x000016B2   PUSH Int 84
0x000016BB   CALL refresh 0 () ():Void
0x000016CC   PUSH Str 46 ; 「うはははは」
0x000016D5   TEXT 38
0x000016DA   LINE 75
0x000016DF   OPEN
0x000016E0   PUSH Int 14
0x000016E9   CALL Pause 0 () ():Void
0x000016FA   POP Void
0x000016FF   LINE 77
0x00001704   OPEN
0x00001705   PUSH Int 84
0x0000170E   CALL refresh 0 () ():Void
0x0000171F   PUSH Str 47 ; 約束を思い出すこともなく、夜はテレビを堪能した。
0x00001728   TEXT 39
0x0000172D   LINE 77
0x00001732   OPEN
0x00001733   PUSH Int 14
0x0000173C   CALL Pause 0 () ():Void
0x0000174D   POP Void
0x00001752   LINE 80
0x00001757   OPEN
0x00001758   PUSH Int 5
0x00001761   PUSH Str 84 ; sys20_adv00
0x0000176A   PUSH Int 1
0x00001773   PUSH Int 4
0x0000177C   PUSH Str 85 ; kuro
0x00001785   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x000017A6   POP Int
0x000017AB   LINE 82
0x000017B0   OPEN
0x000017B1   PUSH Int 5
0x000017BA   PUSH Str 86 ; sys20_adv00
0x000017C3   PUSH Int 1
0x000017CC   PUSH Int 20
0x000017D5   PUSH Str 87 ; bg011
0x000017DE   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x000017FF   POP Int
0x00001804   LINE 85
0x00001809   OPEN
0x0000180A   PUSH Int 84
0x00001813   CALL refresh 0 () ():Void
0x00001824   PUSH Str 48 ; 瑚太朗＿体験版
0x0000182D   NAME
0x0000182E   LINE 85
0x00001833   OPEN
0x00001834   PUSH Int 84
0x0000183D   CALL refresh 0 () ():Void
0x0000184E   PUSH Str 49 ; 「わはははは」
0x00001857   TEXT 40
0x0000185C   LINE 85
0x00001861   OPEN
0x00001862   PUSH Int 14
0x0000186B   CALL Pause 0 () ():Void
0x0000187C   POP Void
0x00001881   LINE 87
0x00001886   OPEN
0x00001887   PUSH Int 84
0x00001890   CALL refresh 0 () ():Void
0x000018A1   PUSH Str 50 ; 約束を思い出すこともなく、土曜の休みは町で遊んだ。
0x000018AA   TEXT 41
0x000018AF   LINE 87
0x000018B4   OPEN
0x000018B5   PUSH Int 14
0x000018BE   CALL Pause 0 () ():Void
0x000018CF   POP Void
0x000018D4   LINE 89
0x000018D9   OPEN
0x000018DA   PUSH Int 5
0x000018E3   PUSH Str 88 ; sys20_adv00
0x000018EC   PUSH Int 1
0x000018F5   PUSH Int 20
0x000018FE   PUSH Str 89 ; kuro
0x00001907   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x00001928   POP Int
0x0000192D   LINE 90
0x00001932   OPEN
0x00001933   PUSH Int 5
0x0000193C   PUSH Str 90 ; sys20_adv00
0x00001945   PUSH Int 1
0x0000194E   PUSH Int 20
0x00001957   PUSH Str 91 ; bg001n1
0x00001960   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x00001981   POP Int
0x00001986   LINE 92
0x0000198B   OPEN
0x0000198C   PUSH Int 84
0x00001995   CALL refresh 0 () ():Void
0x000019A6   PUSH Str 51 ; 約束破りに気づいたのは夜のことだった。
0x000019AF   TEXT 42
0x000019B4   LINE 92
0x000019B9   OPEN
0x000019BA   PUSH Int 14
0x000019C3   CALL Pause 0 () ():Void
0x000019D4   POP Void
0x000019D9   LINE 93
0x000019DE   OPEN
0x000019DF   PUSH Int 84
0x000019E8   CALL refresh 0 () ():Void
0x000019F9   PUSH Str 52 ; 後悔するがもう遅い。
0x00001A02   TEXT 43
0x00001A07   LINE 93
0x00001A0C   OPEN
0x00001A0D   PUSH Int 14
0x00001A16   CALL Pause 0 () ():Void
0x00001A27   POP Void
0x00001A2C   LINE 94
0x00001A31   OPEN
0x00001A32   PUSH Int 84
0x00001A3B   CALL refresh 0 () ():Void
0x00001A4C   PUSH Str 53 ; 吉野には今度あやまっておけばいいだろうと思い、寝た。
0x00001A55   TEXT 44
0x00001A5A   LINE 94
0x00001A5F   OPEN
0x00001A60   PUSH Int 14
0x00001A69   CALL Pause 0 () ():Void
0x00001A7A   POP Void
0x00001A7F   LINE 95
0x00001A84   OPEN
0x00001A85   PUSH Int 84
0x00001A8E   CALL refresh 0 () ():Void
0x00001A9F   PUSH Str 54 ; こういう人を舐めたように見えるところが、吉野に嫌われる原因なのかも知れない。
0x00001AA8   TEXT 45
0x00001AAD   LINE 95
0x00001AB2   OPEN
0x00001AB3   PUSH Int 14
0x00001ABC   CALL Pause 0 () ():Void
0x00001ACD   POP Void
0x00001AD2   LINE 97
0x00001AD7   OPEN
0x00001AD8   PUSH Int 42
0x00001AE1   PUSH Int 4
0x00001AEA   PUSH Int 2000
0x00001AF3   CALL sound_bgm.stop_timer 1 (Int) ():Void
0x00001B08   POP Void
0x00001B0D   LINE 99
0x00001B12   OPEN
0x00001B13   PUSH Int 5
0x00001B1C   PUSH Str 92 ; sys00_sys00
0x00001B25   PUSH Int 75
0x00001B2E   PUSH Int 2147483647
0x00001B37   PUSH Int 2147483647
0x00001B40   CALL farcall_with 1 (Str, Int, Int, Int) ():Int
0x00001B61   POP Int
0x00001B66   LINE 101
0x00001B6B   OPEN
0x00001B6C   PUSH Int 5
0x00001B75   PUSH Str 93 ; sys20_adv00
0x00001B7E   PUSH Int 1
0x00001B87   PUSH Int 6
0x00001B90   PUSH Str 94 ; kuro
0x00001B99   CALL farcall_with 1 (Str, Int, Int, Str) ():Int
0x00001BBA   POP Int
0x00001BBF   LINE 103
0x00001BC4   OPEN
0x00001BC5   PUSH Int 2113929358
0x00001BCE   PUSH Int 80
0x00001BD7   PUSH Str 95 ; ny_mv_tree01
0x00001BE0   PUSH Int 0
0x00001BE9   CALL $ny_set_movie 0 (Int, Str, Int) ():Int
0x00001C06   POP Int
0x00001C0B   LINE 104
0x00001C10   OPEN
0x00001C11   PUSH Int 2113929358
0x00001C1A   PUSH Int 80
0x00001C23   PUSH Str 55 ; 
0x00001C2C   PUSH Int 1
0x00001C35   CALL $ny_set_movie 0 (Int, Str, Int) ():Int
0x00001C52   POP Int
0x00001C57   LINE 104
0x00001C5C   OPEN
0x00001C5D   PUSH Int 55
0x00001C66   PUSH Int 2000
0x00001C6F   CALL TIMEWAIT_KEY 0 (Int) ():Int
0x00001C84   POP Int
0x00001C89   LINE 107
0x00001C8E   OPEN
0x00001C8F   PUSH Int 4
0x00001C98   PUSH Str 96 ; seen01003
0x00001CA1   CALL jump_sce 0 (Str) ():Void
0x00001CB6   POP Void
0x00001CBB   LINE 109
0x00001CC0   END