macro Text{text} str_in:
	OPEN
	PUSH Int 84
	CALL refresh 0 () ():Void
	PUSH Str str_in
	TEXT [id]
end macro

macro Page{p}:
	TEXT [id]
	OPEN
	PUSH Int 14
	CALL Pause 0 () ():Void
	POP Void
	OPEN
	PUSH Int 84
	CALL refresh 0 () ():Void
end macro

macro Pause{pause}:
	OPEN
	PUSH Int 14
	CALL Pause 0 () ():Void
	POP Void
end macro

macro NewLine{nl}:
	TEXT [id]
	OPEN
	PUSH Int 0x3E
	CALL Line 0 () ():Void
	POP Void
end macro